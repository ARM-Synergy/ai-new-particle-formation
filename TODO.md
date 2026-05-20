# NPF Detection Project Todo

Goal: build a reproducible machine-learning workflow to recognize new particle formation (NPF) events using ARM SGP particle measurements, with SMPS as the core dataset.

## 1. Define Study Scope

- [ ] Choose study period for SGP data.
- [ ] Decide the working time resolution, such as 5 min, 10 min, 30 min, or hourly.
- [ ] Define daily classes: NPF event, non-event, and unclear/undefined.
- [ ] Decide whether unclear days are excluded from training or kept as a third class.
- [ ] Document the final NPF event definition used for labeling.

## 2. Download Data

- [ ] Download SGP SMPS data.
- [ ] Download SGP CPCF data.
- [ ] Download SGP CPCUF data.
- [ ] Record data product names, versions, date ranges, and download commands or URLs.
- [ ] Save raw data in a read-only/raw-data folder structure.

## 3. Combine and Clean Data

- [ ] Standardize timestamps and timezone handling.
- [ ] Align SMPS, CPCF, and CPCUF data to the same time grid.
- [ ] Apply available quality-control flags.
- [ ] Remove or mark missing, invalid, and suspicious measurements.
- [ ] Check units for particle concentration and diameter.
- [ ] Confirm SMPS diameter bin centers and bin widths.
- [ ] Create a cleaned analysis-ready dataset.

## 4. Create Event Labels

- [ ] Generate daily SMPS time-diameter contour plots.
- [ ] Manually label days as NPF event, non-event, or unclear.
- [ ] Save labels in a separate table with date, label, confidence, and notes.
- [ ] Review ambiguous days twice for consistency.
- [ ] Keep example plots for event, non-event, and unclear days.

## 5. Extract SMPS-Based Features

- [ ] Calculate total particle number concentration.
- [ ] Calculate size-range concentrations, for example 3-10 nm, 10-25 nm, 25-50 nm, 50-100 nm, and 100+ nm.
- [ ] Calculate daytime and nighttime concentration differences.
- [ ] Calculate morning burst strength for the smallest particles.
- [ ] Estimate geometric mean diameter.
- [ ] Estimate mode diameter through the day.
- [ ] Calculate mode diameter shift from morning to afternoon.
- [ ] Calculate simple slope features for nucleation and growth modes.
- [ ] Calculate particle fractions in each size range.
- [ ] Keep the first feature set compact and physically interpretable.

## 6. Train Model

- [ ] Start with Random Forest as the baseline model.
- [ ] Split training and testing by time period to avoid information leakage.
- [ ] Compare against a simple baseline, such as always predicting non-event.
- [ ] Tune Random Forest settings only after the basic workflow works.
- [ ] Save model inputs, labels, parameters, and trained model output.

## 7. Evaluate Model

- [ ] Report precision, recall, F1 score, and confusion matrix.
- [ ] Check event recall carefully so true NPF days are not missed.
- [ ] Manually inspect false positives and false negatives.
- [ ] Test whether feature importance agrees with physical expectations.
- [ ] Evaluate reproducibility across seasons or years if enough data are available.

## 8. Polish Figures and Presentation

- [ ] Make workflow diagram from raw data to labels, features, model, and evaluation.
- [ ] Make example SMPS contour plots for NPF and non-event days.
- [ ] Make feature importance plot.
- [ ] Make confusion matrix figure.
- [ ] Make prediction examples for correct and incorrect classifications.
- [ ] Prepare final PowerPoint slides.

## Open Questions

- [ ] Which exact SGP date range should we use first?
- [ ] Should CPCF and CPCUF be used only for validation, or also as model inputs?
- [ ] What minimum data completeness should a day need to be included?
- [ ] Should the first model use only SMPS features for better reproducibility?
- [ ] How should unclear days be handled during model training?
