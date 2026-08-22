from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "AAPL.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    DATA_PATH,
    skiprows=3,
    names=["Date", "Close", "High", "Low", "Open", "Volume"]
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
for col in ["Open", "High", "Low", "Close", "Volume"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values("Date").reset_index(drop=True)

missing_dates = int(df["Date"].isna().sum())
exact_duplicates = int(df.duplicated().sum())
duplicate_date_rows = int(df["Date"].duplicated(keep=False).sum())

negative_mask = (df[["Open","High","Low","Close","Volume"]] < 0).any(axis=1)
ohlc_inconsistent = (
    (df["High"] < df["Low"]) |
    (df["High"] < df[["Open","Close"]].max(axis=1)) |
    (df["Low"] > df[["Open","Close"]].min(axis=1))
)

clean = df.dropna(subset=["Date"]).dropna(
    subset=["Open","High","Low","Close","Volume"]
).drop_duplicates().copy()

clean["Daily_Return"] = clean["Close"].pct_change()
clean["Log_Return"] = np.log(clean["Close"] / clean["Close"].shift(1))
clean["Intraday_Range_Pct"] = (clean["High"] - clean["Low"]) / clean["Close"] * 100
clean["Volume_Change_Pct"] = clean["Volume"].pct_change()
clean["Rolling_Volatility_20D"] = clean["Log_Return"].rolling(20).std() * np.sqrt(252)
clean["Year"] = clean["Date"].dt.year
clean["Log_Volume"] = np.log1p(clean["Volume"])

q1 = clean["Daily_Return"].quantile(.25)
q3 = clean["Daily_Return"].quantile(.75)
iqr = q3 - q1
clean["Return_Outlier_IQR"] = (
    (clean["Daily_Return"] < q1 - 1.5*iqr) |
    (clean["Daily_Return"] > q3 + 1.5*iqr)
)

mean_ret = clean["Daily_Return"].mean()
std_ret = clean["Daily_Return"].std()
clean["Return_ZScore"] = (clean["Daily_Return"] - mean_ret) / std_ret
clean["Return_Outlier_Z"] = clean["Return_ZScore"].abs() >= 3

clean.to_csv(PROCESSED_DIR / "AAPL_cleaned.csv", index=False)

quality = pd.DataFrame({
    "metric": [
        "raw_loaded_rows", "raw_columns", "missing_dates",
        "exact_duplicate_rows", "duplicate_date_rows",
        "negative_value_rows", "ohlc_consistency_violations",
        "cleaned_rows", "IQR_return_outlier_flags",
        "Z_return_outlier_flags"
    ],
    "value": [
        len(df), len(df.columns), missing_dates,
        exact_duplicates, duplicate_date_rows,
        int(negative_mask.sum()), int(ohlc_inconsistent.sum()),
        len(clean), int(clean["Return_Outlier_IQR"].sum()),
        int(clean["Return_Outlier_Z"].sum())
    ]
})
quality.to_csv(REPORT_DIR / "week2_quality_summary.csv", index=False)

print(quality.to_string(index=False))
this is 
