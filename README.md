# Financial Data Analysis Internship

This repository documents a four-week financial data analysis project using historical Apple Inc. (AAPL) daily market data. The workflow progresses from planning and acquisition through cleaning, exploratory analysis, visualization, and predictive modeling.

## Project Dataset

- **Security:** Apple Inc. (AAPL), Nasdaq
- **Period:** January 2, 2020 – December 31, 2024
- **Primary variables:** Open, High, Low, Close, Volume
- **Processed dataset:** `data/processed/AAPL_cleaned.csv`
- **Workflow:** Python, pandas, NumPy, Matplotlib, scikit-learn, Jupyter Notebook, Git/GitHub

## Week 1 — Data Acquisition & Preliminary Analysis

Week 1 established the project scope, research questions, data source, reproducible Python workflow, and initial AAPL dataset. Historical AAPL OHLCV data was acquired using `yfinance` and saved as `data/AAPL.csv`.

**Main deliverables**
- `notebooks/01_week1_data_acquisition_and_eda.ipynb`
- `reports/Week_1_Financial_Analytics_Project_Plan_Final.docx`
- `data/AAPL.csv`

## Week 2 — Data Wrangling & Processing

Week 2 transformed the raw AAPL data into a validated analysis-ready dataset. The workflow checked missing dates, duplicates, negative values, and OHLC consistency, then engineered returns, log returns, intraday range, volume change, rolling volatility, year, and log-transformed volume.

The processed dataset contains 1,258 observations after the documented validation workflow. Return-based IQR and Z-score methods were used to flag potential outliers for investigation rather than automatic deletion.

**Main deliverables**
- `notebooks/02_week2_data_wrangling_and_processing.ipynb`
- `src/week2_data_wrangling.py`
- `data/processed/AAPL_cleaned.csv`
- `reports/week2_quality_summary.csv`

## Week 3 — Exploratory Data Analysis & Visualization

Week 3 performed descriptive statistical analysis and six computed visualizations using the validated processed dataset. It examined price trends, return distribution, rolling volatility, trading volume, volume versus absolute return, and year-wise performance. Outlier periods were also investigated in context.

**Main deliverables**
- `notebooks/03_week3_eda_and_visualization.ipynb`
- `src/week3_eda.py`
- `reports/Week_3_AAPL_EDA_Visualization_Report.docx`
- `figures/week3/fig1_close_price.png`
- `figures/week3/fig2_return_hist.png`
- `figures/week3/fig3_rolling_volatility.png`
- `figures/week3/fig4_volume.png`
- `figures/week3/fig5_volume_vs_absreturn.png`
- `figures/week3/fig6_annual_return.png`

## Week 4 — Predictive Modeling & Performance Evaluation

Week 4 extends the same AAPL project into predictive modeling. The unchanged processed dataset is used to construct modeling-specific features and next-day targets. The primary target is next-day closing price; a secondary model predicts next-day return as a harder test of forecasting signal.

### Modeling approach

- Modeling features: Close, Volume, Rolling_Volatility_20D, Intraday_Range_Pct, Daily_Return, SMA_5, SMA_10
- Return-model features: Volume, Rolling_Volatility_20D, Intraday_Range_Pct, Daily_Return, Volume_Change_Pct
- Target: next-day Close using `shift(-1)`
- Secondary target: next-day Daily_Return using `shift(-1)`
- Split: chronological 80/20 train/test split; no random shuffling
- Test period: 2024
- Models: naive persistence baseline, Close-only Linear Regression, multivariate Linear Regression, and next-day return Linear Regression
- Metrics: R², MSE, RMSE, MAE

### Week 4 test-set results

| Model | Test R² | Test RMSE | Test MAE |
|---|---:|---:|---:|
| Naive persistence | 0.9873 | $2.870 | $2.111 |
| Close-only Linear Regression | 0.9871 | $2.894 | $2.155 |
| Multivariate Linear Regression | 0.9868 | $2.932 | $2.204 |

The multivariate model does not outperform the naive persistence baseline on the held-out 2024 test period. The secondary next-day return model achieves test R² of approximately -0.057, indicating little useful linear predictive signal from the selected price/volume-derived features.

### Week 4 deliverables

- `notebooks/04_week4_predictive_modeling.ipynb`
- `src/week4_predictive_modeling.py`
- `reports/Week_4_AAPL_Predictive_Modeling_Report.docx`
- `reports/model2_test_predictions.csv`
- `reports/model3_test_predictions.csv`
- `figures/week4/figA_actual_vs_predicted.png`
- `figures/week4/figB_predicted_vs_actual.png`
- `figures/week4/figC_residuals.png`
- `figures/week4/figD_rmse_comparison.png`
- `figures/week4/figE_return_prediction.png`

## Final Project Structure

```text
financial-data-analysis-internship/
├── data/
│   ├── AAPL.csv
│   └── processed/
│       └── AAPL_cleaned.csv
├── figures/
│   ├── week3/
│   └── week4/
├── notebooks/
│   ├── 01_week1_data_acquisition_and_eda.ipynb
│   ├── 02_week2_data_wrangling_and_processing.ipynb
│   ├── 03_week3_eda_and_visualization.ipynb
│   └── 04_week4_predictive_modeling.ipynb
├── reports/
│   ├── Week_1_Financial_Analytics_Project_Plan_Final.docx
│   ├── Week_3_AAPL_EDA_Visualization_Report.docx
│   ├── Week_4_AAPL_Predictive_Modeling_Report.docx
│   ├── week2_quality_summary.csv
│   ├── model2_test_predictions.csv
│   └── model3_test_predictions.csv
├── src/
│   ├── week2_data_wrangling.py
│   ├── week3_eda.py
│   └── week4_predictive_modeling.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Reproducibility

The analysis is organized as sequential weekly stages. The Week 4 modeling script reads the processed Week 2/3 dataset and regenerates the predictive-model outputs.

From the repository root:

```bash
python src/week4_predictive_modeling.py
```

No investment recommendation is intended. The project evaluates forecasting difficulty and demonstrates a reproducible financial-data-analysis workflow.
