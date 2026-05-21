"""Create clean daily SMPS geometric averages using fixed UTC-6 local time."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


EXPECTED_SAMPLES_PER_DAY = 288
LOCAL_UTC_OFFSET_HOURS = -6
MIN_VALID_FRACTION = 0.95


def find_input_dir(input_dir: Path) -> Path:
    if input_dir.exists():
        return input_dir
    fallback = Path("data")
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"Input directory not found: {input_dir}")


def load_samples(input_dir: Path, pattern: str) -> pd.DataFrame:
    rows = []
    files = sorted(input_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files matched {input_dir / pattern}")

    for path in files:
        with xr.open_dataset(path, engine="scipy") as ds:
            utc_time = pd.to_datetime(ds["time"].values)
            local_time = utc_time + pd.Timedelta(hours=LOCAL_UTC_OFFSET_HOURS)
            geometric_mean = np.asarray(ds["geometric_mean"].values, dtype=float)
            geometric_std = np.asarray(ds["geometric_std"].values, dtype=float)

            valid = np.isfinite(geometric_mean) & np.isfinite(geometric_std)
            if "qc_total_N_conc" in ds:
                valid &= np.asarray(ds["qc_total_N_conc"].values) == 0

            rows.append(
                pd.DataFrame(
                    {
                        "local_date": local_time.normalize().date,
                        "geometric_mean": geometric_mean,
                        "geometric_std": geometric_std,
                        "valid": valid,
                    }
                )
            )

    return pd.concat(rows, ignore_index=True)


def make_daily_average(samples: pd.DataFrame) -> pd.DataFrame:
    valid_samples = samples.loc[samples["valid"]].copy()
    valid_counts = valid_samples.groupby("local_date").size()
    valid_dates = valid_counts[valid_counts / EXPECTED_SAMPLES_PER_DAY >= MIN_VALID_FRACTION].index
    valid_day_samples = valid_samples.loc[valid_samples["local_date"].isin(valid_dates)]

    def lower_fraction_mean(values: pd.Series, fraction: float) -> float:
        threshold = values.quantile(fraction)
        return values.loc[values <= threshold].mean()

    daily = (
        valid_day_samples.groupby("local_date")
        .agg(
            geometric_mean_daily_mean_nm=("geometric_mean", "mean"),
            geometric_std_daily_mean_nm=("geometric_std", "mean"),
            geometric_mean_smallest_25pct_daily_mean_nm=(
                "geometric_mean",
                lambda values: lower_fraction_mean(values, 0.25),
            ),
            geometric_mean_smallest_50pct_daily_mean_nm=(
                "geometric_mean",
                lambda values: lower_fraction_mean(values, 0.50),
            ),
            geometric_mean_smallest_75pct_daily_mean_nm=(
                "geometric_mean",
                lambda values: lower_fraction_mean(values, 0.75),
            ),
            geometric_std_smallest_25pct_daily_mean_nm=(
                "geometric_std",
                lambda values: lower_fraction_mean(values, 0.25),
            ),
            geometric_std_smallest_50pct_daily_mean_nm=(
                "geometric_std",
                lambda values: lower_fraction_mean(values, 0.50),
            ),
            geometric_std_smallest_75pct_daily_mean_nm=(
                "geometric_std",
                lambda values: lower_fraction_mean(values, 0.75),
            ),
        )
        .reset_index()
    )
    return daily[
        [
            "local_date",
            "geometric_mean_daily_mean_nm",
            "geometric_std_daily_mean_nm",
            "geometric_mean_smallest_25pct_daily_mean_nm",
            "geometric_mean_smallest_50pct_daily_mean_nm",
            "geometric_mean_smallest_75pct_daily_mean_nm",
            "geometric_std_smallest_25pct_daily_mean_nm",
            "geometric_std_smallest_50pct_daily_mean_nm",
            "geometric_std_smallest_75pct_daily_mean_nm",
        ]
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/raw/smps"))
    parser.add_argument("--pattern", default="sgpaossmpsE13.b1.*.nc")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/smps_daily_geometric_local_utc_minus6.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = find_input_dir(args.input_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    samples = load_samples(input_dir, args.pattern)
    daily = make_daily_average(samples)
    daily.to_csv(args.output, index=False)

    print(f"Input directory: {input_dir}")
    print(f"Valid local days: {len(daily)}")
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
