# Introducing the Model Fidelity Metric (MFM) for robust and diagnostic hydrological evaluation

> A robust, reliable, and normalized metric for model evaluation and scoring.

Metrics calculation and case studies generating.

```
Model Fidelity Metric/
├── data/                  # Runoff data and metrics results
├── temp/                  # Temporary files path
├── case1.py               # Case 1: Error compensation
├── case2.py               # Case 2: Stability in near-constant conditions
├── case3.py               # Case 3: Phase and error decoupling
├── case4.py               # Performance in real-world catchments
├── case5.py               # Sensitivity to hyperparameters
├── example.py             # Example of generating all figures
├── mfm.py                 # Metrics (MFM, NSE, KGE, mKGE, RMSE, NRMSE) calculation
├── read_file.py           # Read CAMELS data
└── README.md              # README file
```

## Metrics calculation

- Function `model_fidelity_metric` calculates MFM. The hyperparameters `p=1, bins_suse=10, bins_phi=10, c=4` is the default setting in paper.

- Function `standard_metrics` calculates NSE, KGE, mKGE, RMSE, NRMSE.

## Run case studies

Run `example.py` to generate all figures. Turn on `write_option=True` option to save all figures in the folder `temp/`.

## Data availability

Runoff data is from Daymet dataset in CAMELS dataset <https://zenodo.org/records/15529996> (Newman, A. J., Sampson, K., Clark, M., Bock, A., Viger, R., Blodgett, D., Addor, N., & Mizukami, M. (2022). CAMELS: Catchment Attributes and MEteorology for Large-sample Studies (1.2) [Data set]. Zenodo. https://doi.org/10.5065/D6MW2F4D).
