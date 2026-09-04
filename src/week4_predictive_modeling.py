"""Week 4: Predictive Modeling & Performance Evaluation for AAPL."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "AAPL_cleaned.csv"
FIG = ROOT / "figures" / "week4"
REP = ROOT / "reports"
FIG.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

def metrics(y, p):
    mse = mean_squared_error(y, p)
    return {"R2": r2_score(y, p), "MSE": mse, "RMSE": np.sqrt(mse),
            "MAE": mean_absolute_error(y, p)}

df = pd.read_csv(DATA, parse_dates=["Date"]).set_index("Date").sort_index()
df["SMA_5"] = df["Close"].rolling(5).mean()
df["SMA_10"] = df["Close"].rolling(10).mean()
df["Target_Close_Next"] = df["Close"].shift(-1)
df["Target_Return_Next"] = df["Daily_Return"].shift(-1)

FEATURES = ["Close", "Volume", "Rolling_Volatility_20D", "Intraday_Range_Pct",
            "Daily_Return", "SMA_5", "SMA_10"]
RETURN_FEATURES = ["Volume", "Rolling_Volatility_20D", "Intraday_Range_Pct",
                   "Daily_Return", "Volume_Change_Pct"]
model = df.dropna(subset=FEATURES + ["Target_Close_Next", "Target_Return_Next"])
split = int(len(model) * 0.8)
train, test = model.iloc[:split], model.iloc[split:]

ytr, yte = train["Target_Close_Next"].to_numpy(), test["Target_Close_Next"].to_numpy()

# Naive persistence baseline
a_train = metrics(ytr, train["Close"].to_numpy())
a_test = metrics(yte, test["Close"].to_numpy())

# Model 1: Close only
m1 = LinearRegression().fit(train[["Close"]], ytr)
p1tr, p1te = m1.predict(train[["Close"]]), m1.predict(test[["Close"]])
m1_train, m1_test = metrics(ytr, p1tr), metrics(yte, p1te)

# Model 2: multivariate next-day Close
m2 = LinearRegression().fit(train[FEATURES], ytr)
p2tr, p2te = m2.predict(train[FEATURES]), m2.predict(test[FEATURES])
m2_train, m2_test = metrics(ytr, p2tr), metrics(yte, p2te)

pred2 = test[["Close", "Target_Close_Next"]].copy()
pred2["Predicted_Close_Next"] = p2te
pred2["Residual"] = pred2["Target_Close_Next"] - pred2["Predicted_Close_Next"]
pred2.to_csv(REP / "model2_test_predictions.csv")

# Model 3: next-day return
rtr, rte = train["Target_Return_Next"].to_numpy(), test["Target_Return_Next"].to_numpy()
m3 = LinearRegression().fit(train[RETURN_FEATURES], rtr)
p3tr, p3te = m3.predict(train[RETURN_FEATURES]), m3.predict(test[RETURN_FEATURES])
m3_train, m3_test = metrics(rtr, p3tr), metrics(rte, p3te)

pred3 = test[["Target_Return_Next"]].copy()
pred3["Predicted_Return_Next"] = p3te
pred3.to_csv(REP / "model3_test_predictions.csv")

# Diagnostic figures
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(test.index, yte, label="Actual next-day Close")
ax.plot(test.index, p2te, "--", label="Predicted (Model 2)")
ax.set(title="Actual vs. Predicted Next-Day Close — Test Set (2024)", xlabel="Date", ylabel="Close Price (USD)")
ax.legend(); fig.tight_layout(); fig.savefig(FIG / "figA_actual_vs_predicted.png", dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 5.8))
ax.scatter(yte, p2te, s=14, alpha=.55)
lims = [min(yte.min(), p2te.min()) - 3, max(yte.max(), p2te.max()) + 3]
ax.plot(lims, lims, "--", label="Perfect prediction")
ax.set(xlim=lims, ylim=lims, title="Predicted vs. Actual Next-Day Close — Test Set", xlabel="Actual Close (USD)", ylabel="Predicted Close (USD)")
ax.legend(); fig.tight_layout(); fig.savefig(FIG / "figB_predicted_vs_actual.png", dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(test.index, pred2["Residual"])
ax.axhline(0, linestyle="--")
ax.set(title="Model 2 Prediction Residuals Over Time — Test Set", xlabel="Date", ylabel="Residual: Actual − Predicted (USD)")
fig.tight_layout(); fig.savefig(FIG / "figC_residuals.png", dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 4.3))
labels = ["Naive\n(persistence)", "Model 1\n(Close only)", "Model 2\n(multivariate)"]
vals = [a_test["RMSE"], m1_test["RMSE"], m2_test["RMSE"]]
ax.bar(labels, vals)
for i, v in enumerate(vals): ax.text(i, v, f"{v:.3f}", ha="center", va="bottom")
ax.set(title="Test-Set RMSE by Model (Lower Is Better)", ylabel="RMSE")
fig.tight_layout(); fig.savefig(FIG / "figD_rmse_comparison.png", dpi=170); plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(test.index, rte, label="Actual next-day return")
ax.plot(test.index, p3te, "--", label="Predicted return")
ax.axhline(0, linestyle=":")
ax.set(title="Next-Day Return Prediction — Test Set (2024)", xlabel="Date", ylabel="Daily Return")
ax.legend(); fig.tight_layout(); fig.savefig(FIG / "figE_return_prediction.png", dpi=170); plt.close(fig)

print("Train rows:", len(train), "Test rows:", len(test))
print("Naive test:", a_test)
print("Model 1 test:", m1_test)
print("Model 2 test:", m2_test)
print("Model 3 return test:", m3_test)
print("Week 4 outputs written to figures/week4 and reports/")
