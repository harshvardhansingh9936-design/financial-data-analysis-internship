from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_PATH = Path("data/processed/AAPL_cleaned.csv")
FIG_DIR = Path("figures/week3")
REPORT_DIR = Path("reports")
FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["Date"]).set_index("Date").sort_index()

# Validation
print("Shape:", df.shape)
print("Date range:", df.index.min(), "to", df.index.max())
print("Duplicate rows:", int(df.duplicated().sum()))
print("Duplicate dates:", int(df.index.duplicated().sum()))
print(df.isna().sum()[lambda s: s > 0])

neg_mask = (df[["Open","High","Low","Close","Volume"]] < 0).any(axis=1)
ohlc_bad = ((df["High"] < df["Low"]) |
            (df["High"] < df[["Open","Close"]].max(axis=1)) |
            (df["Low"] > df[["Open","Close"]].min(axis=1)))
print("Negative-value rows:", int(neg_mask.sum()))
print("OHLC consistency violations:", int(ohlc_bad.sum()))

# Week 2 feature definitions
df["Daily_Return"] = df["Close"].pct_change()
df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
df["Intraday_Range_Pct"] = (df["High"] - df["Low"]) / df["Close"] * 100
df["Volume_Change_Pct"] = df["Volume"].pct_change()
df["Rolling_Volatility_20D"] = df["Log_Return"].rolling(20).std() * np.sqrt(252)
df["Year"] = df.index.year
df["Log_Volume"] = np.log1p(df["Volume"])

# Descriptive statistics
core = ["Open","High","Low","Close","Volume"]
desc = df[core].describe(percentiles=[.25,.5,.75]).T
desc["Mode"] = df[core].mode().iloc[0]
desc = desc[["count","mean","50%","Mode","std","min","25%","75%","max"]]
desc.columns = ["Count","Mean","Median","Mode","Std Dev","Min","Q1","Q3","Max"]
print("\nCORE STATISTICS\n", desc.round(4))

ret = df["Daily_Return"].dropna()
print("\nRETURN STATISTICS\n", ret.describe(percentiles=[.25,.5,.75]))
print("Skew:", ret.skew(), "Excess kurtosis:", ret.kurt())
print("Positive days:", int((ret>0).sum()))
print("Negative days:", int((ret<0).sum()))
print("Largest gain:", ret.max(), ret.idxmax().date())
print("Largest loss:", ret.min(), ret.idxmin().date())

vol = df["Rolling_Volatility_20D"].dropna()
print("\nVOLATILITY\n", vol.describe(percentiles=[.25,.5,.75]))
print("Most volatile:", vol.idxmax().date(), vol.max())
print("Calmest:", vol.idxmin().date(), vol.min())

print("\nVOLUME")
print("Average:", df["Volume"].mean())
print("Highest:", df["Volume"].idxmax().date(), df["Volume"].max())
print("Lowest:", df["Volume"].idxmin().date(), df["Volume"].min())

# Figure 1
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df.index, df["Close"], linewidth=1.1)
ax.set_title("Figure 1. AAPL Closing Price vs. Date (Jan 2020–Dec 2024)")
ax.set_xlabel("Date"); ax.set_ylabel("Close Price (USD)")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig1_close_price.png", dpi=150); plt.close(fig)

# Figure 2
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(df["Daily_Return"].dropna(), bins=60, edgecolor="white")
ax.axvline(0, linewidth=.8)
ax.set_title("Figure 2. Distribution of AAPL Daily Returns (2020–2024)")
ax.set_xlabel("Daily Return (fraction)"); ax.set_ylabel("Frequency")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig2_return_hist.png", dpi=150); plt.close(fig)

# Figure 3
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df.index, df["Rolling_Volatility_20D"], linewidth=1.1)
ax.set_title("Figure 3. AAPL 20-Day Rolling Annualized Volatility")
ax.set_xlabel("Date"); ax.set_ylabel("Annualized Volatility (fraction)")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig3_rolling_volatility.png", dpi=150); plt.close(fig)

# Figure 4
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df.index, df["Volume"], linewidth=.7)
ax.set_title("Figure 4. AAPL Trading Volume vs. Date")
ax.set_xlabel("Date"); ax.set_ylabel("Volume (shares)")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig4_volume.png", dpi=150); plt.close(fig)

# Figure 5
abs_ret = df["Daily_Return"].abs()
plot_df = pd.DataFrame({"Volume":df["Volume"], "Abs_Return":abs_ret}).dropna()
fig, ax = plt.subplots(figsize=(10,5))
ax.scatter(plot_df["Abs_Return"], plot_df["Volume"], s=10, alpha=.45)
ax.set_title("Figure 5. Trading Volume vs. Absolute Daily Return")
ax.set_xlabel("|Daily Return| (fraction)"); ax.set_ylabel("Volume (shares)")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig5_volume_vs_absreturn.png", dpi=150); plt.close(fig)
print("Pearson r:", plot_df["Volume"].corr(plot_df["Abs_Return"]))
print("Spearman rho:", plot_df["Volume"].corr(plot_df["Abs_Return"], method="spearman"))

# Figure 6
annual = df.groupby("Year")["Close"].agg(start="first", end="last")
annual["Annual_Return_Pct"] = (annual["end"]/annual["start"] - 1)*100
print("\nANNUAL PERFORMANCE\n", annual.round(2))
fig, ax = plt.subplots(figsize=(10,5))
bar_colors = ["#1F3864" if v >= 0 else "#8A1C1C" for v in annual["Annual_Return_Pct"]]
ax.bar(annual.index.astype(str), annual["Annual_Return_Pct"], color=bar_colors)
ax.axhline(0, color="#333333", linewidth=.9)
ax.set_title("Figure 6. AAPL Year-wise Closing-Price Performance")
ax.set_xlabel("Year"); ax.set_ylabel("Annual Return (%)")
fig.tight_layout(); fig.savefig(FIG_DIR/"fig6_annual_return.png", dpi=150); plt.close(fig)

# Week 2 outlier methodology
q1,q3 = ret.quantile(.25), ret.quantile(.75)
iqr = q3-q1
lower, upper = q1-1.5*iqr, q3+1.5*iqr
iqr_flag = (df["Daily_Return"] < lower) | (df["Daily_Return"] > upper)
z = (df["Daily_Return"]-df["Daily_Return"].mean())/df["Daily_Return"].std()
z_flag = z.abs() >= 3
out = df.loc[iqr_flag | z_flag, ["Daily_Return","Close","Volume","Year"]].copy()
out["IQR_Flag"] = iqr_flag.loc[out.index]
out["Z_Flag"] = z_flag.loc[out.index]
out.sort_values("Daily_Return").to_csv(REPORT_DIR/"week3_outlier_dates.csv", index_label="Date")
print("\nIQR bounds:", lower, upper)
print("IQR flagged:", int(iqr_flag.sum()))
print("Z-score flagged:", int(z_flag.sum()))
print("Both:", int((iqr_flag & z_flag).sum()))
