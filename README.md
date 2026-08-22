# Financial Data Analysis Internship

## Week 1 — Data Acquisition & Preliminary Analysis

This repository contains my work for the Financial Data Analysis Internship.

The Week 1 task focuses on acquiring publicly available financial market data, storing it in a structured format, and performing preliminary data inspection using Python.

## Project Objectives

The main objectives of this project are to:

- Identify publicly accessible financial data sources.
- Acquire historical financial market data using Python.
- Store acquired data in a structured and reusable format.
- Inspect the dataset for structure, completeness, and consistency.
- Prepare the dataset for data cleaning and exploratory analysis.
- Develop a reproducible Python-based financial data analysis workflow.
- Establish a foundation for subsequent financial analysis and visualization.

## Data Source

### Yahoo Finance

The Week 1 analysis uses historical market data for Apple Inc. (AAPL), obtained through the `yfinance` Python library.

The dataset covers the period from January 2, 2020 to December 31, 2024.

The dataset contains the following market variables:

- Open price
- High price
- Low price
- Close price
- Trading volume

The downloaded dataset is stored locally in:

`data/AAPL.csv`

## Technologies & Libraries

| Technology / Library | Purpose |
|---|---|
| Python | Primary programming language for data acquisition and analysis |
| pandas | Data loading, cleaning, manipulation, and analysis |
| NumPy | Numerical operations and analytical calculations |
| Matplotlib | Data visualization and plotting |
| yfinance | Retrieval of historical financial market data from Yahoo Finance |
| Jupyter Notebook | Interactive analysis, documentation, and presentation of results |
| Git | Version control and project tracking |
| GitHub | Project repository and version-controlled collaboration |

## Repository Structure

```text
financial-data-analysis-internship/
│
├── data/
│   └── AAPL.csv
│
├── figures/
│
├── notebooks/
│   └── 01_week1_data_acquisition_and_eda.ipynb
│
├── reports/
│
├── src/
│
├── .gitignore
├── README.md
└── requirements.txt
Week 1 Progress
Completed
Created and configured the GitHub repository.
Established a structured project directory.
Set up the Python development environment in VS Code.
Created a project-specific Python virtual environment.
Installed the required Python libraries.
Configured the Jupyter Notebook environment.
Created the Week 1 analysis notebook.
Retrieved historical AAPL market data using yfinance.
Saved the downloaded dataset as data/AAPL.csv.
Reloaded the saved dataset using pandas.
Inspected the dataset dimensions and column structure.
Established a reproducible workflow for future analysis.
Dataset Summary

The current AAPL dataset contains:

1,260 observations
5 market variables
Daily historical market data
Date-based observations
Open, High, Low, Close, and Volume information

The dataset was successfully downloaded, saved locally, and loaded again using Python for validation.

Preliminary Analysis Plan

The next stages of the project will focus on:

Checking data types and data quality.
Identifying missing or invalid values.
Cleaning and preprocessing the dataset.
Calculating daily percentage returns.
Examining historical price trends.
Measuring and visualizing market volatility.
Exploring relationships between price and trading volume.
Creating informative financial visualizations.
Identifying potential risk factors and market patterns.
Summarizing the preliminary findings.
Key Questions for Analysis

The planned analysis will investigate questions such as:

How has the AAPL stock price changed over the selected period?
What major trends can be observed in the historical price data?
How volatile has the stock been over time?
What periods show unusually large price movements?
How are daily returns distributed?
Is there any observable relationship between trading volume and price movements?
What preliminary risk factors can be identified from the historical data?
Data Acquisition Approach

The planned data acquisition workflow is:

Identify a reliable and publicly accessible financial data source.
Select the financial instrument and required historical period.
Use Python and yfinance to retrieve the historical market data.
Store the downloaded data in CSV format.
Load the saved data using pandas.
Validate the dataset structure and dimensions.
Prepare the dataset for cleaning and exploratory analysis.

This approach is designed to make the analysis reproducible and easy to extend to additional financial instruments in later stages.

Data Cleaning Approach

The planned data cleaning process will include:

Checking for missing values.
Checking for duplicate observations.
Verifying data types.
Ensuring dates are correctly formatted.
Checking numerical columns for invalid values.
Reviewing the consistency of the dataset.
Preparing clean variables for further analysis.
Preliminary Analysis Approach

After data cleaning, the analysis will include:

Descriptive statistics.
Historical price trend analysis.
Daily return calculations.
Volatility analysis.
Trading volume analysis.
Time-series visualizations.
Identification of unusual movements and potential risk periods.

The analysis will use pandas and NumPy for numerical and tabular operations and Matplotlib for visualization.

Reproducibility

To reproduce the analysis:

Clone this repository from GitHub.
Create a Python virtual environment.
Activate the virtual environment.
Install the dependencies listed in requirements.txt.
Open the Week 1 Jupyter Notebook.
Run the notebook cells sequentially.

The project structure and dependency file are maintained to support reproducibility.

Project Status

Current Stage: Week 1 — Data Acquisition & Preliminary Analysis

Status: In Progress

Current Deliverables
GitHub repository setup
Python environment setup
Historical AAPL dataset
Data acquisition notebook
Initial dataset inspection
Project documentation
Upcoming Deliverables
Data cleaning
Exploratory data analysis
Financial return calculations
Volatility analysis
Data visualizations
Analytical findings and conclusions
Future Development

The project may later be extended to include:

Analysis of additional stocks or financial instruments.
Comparative performance analysis.
Portfolio-level analysis.
Risk and return metrics.
Advanced financial visualizations.
Additional statistical analysis.

This repository is maintained as part of my Financial Data Analysis Internship and documents the development of the project from data acquisition through exploratory and financial analysis.
## Week 2 — Data Wrangling & Processing

Week 2 extends the Week 1 AAPL market-data acquisition workflow into a reproducible data-cleaning and processing pipeline.

### Dataset

- Security: Apple Inc. (AAPL)
- Period: January 2, 2020 to December 31, 2024
- Raw observations: 1,258
- Variables: Date, Open, High, Low, Close, Volume

### Data Quality Results

The Week 2 workflow performed structural and financial-domain validation on the raw AAPL dataset.

| Quality Check | Result |
|---|---:|
| Raw observations | 1,258 |
| Columns | 6 |
| Missing dates | 0 |
| Exact duplicate rows | 0 |
| Duplicate dates | 0 |
| Negative OHLCV values | 0 |
| OHLC consistency violations | 0 |
| Cleaned observations | 1,258 |

No observations were removed during the documented basic cleaning stage because the dataset passed the missing-value, duplicate, date, and financial-domain checks.

### Feature Engineering

The following analysis-ready features were created:

- Daily percentage return
- Log return
- Intraday range percentage
- Volume change percentage
- 20-day rolling annualized volatility
- Year
- Log-transformed trading volume

### Outlier Detection

Two return-based screening methods were applied:

- IQR method: 52 observations flagged
- Z-score method (|z| ≥ 3): 18 observations flagged
- IQR lower bound: approximately -3.90%
- IQR upper bound: approximately +4.26%

Outliers were flagged for investigation rather than automatically removed because unusually large financial returns may represent genuine market events.

For example, March 16, 2020 recorded a daily return of approximately -12.86% with a z-score of approximately -6.51, while March 13, 2020 recorded approximately +11.98% with a z-score of approximately +5.94.

### Week 2 Files

- `notebooks/02_week2_data_wrangling_and_processing.ipynb`
- `src/week2_data_wrangling.py`
- `data/processed/AAPL_cleaned.csv`
- `reports/week2_quality_summary.csv`

### Reproducibility

The raw AAPL dataset is preserved in `data/AAPL.csv`. The cleaned dataset is stored separately in `data/processed/AAPL_cleaned.csv`, while the quality-control metrics are saved in `reports/week2_quality_summary.csv`.

The Week 2 workflow uses Python, pandas, NumPy, and Matplotlib and can be reproduced through the Jupyter notebook or the reusable processing script.
