import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
PALETTE = ["#2E4374", "#4C7EA8", "#7FB2C9", "#D9A441", "#C1502E"]
sns.set_palette(PALETTE)

df = pd.read_csv("business_sales_data.csv", parse_dates=["Order Date", "Ship Date"])
df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["Year"] = df["Order Date"].dt.year
df["Profit Margin"] = df["Profit"] / df["Sales"]

print("=== SHAPE ===")
print(df.shape)
print("\n=== DTYPES ===")
print(df.dtypes)
print("\n=== MISSING VALUES ===")
print(df.isna().sum()[df.isna().sum() > 0])
print("\n=== DUPLICATES ===")
print(df.duplicated().sum())
print("\n=== NUMERIC SUMMARY ===")
print(df[["Quantity", "Discount", "Sales", "Profit", "Profit Margin"]].describe().round(2))
print("\n=== CATEGORICAL COUNTS ===")
for col in ["Region", "Segment", "Category", "Sub-Category", "Ship Mode"]:
    print(f"\n{col}:\n", df[col].value_counts())

# ---------- Correlation matrix ----------
corr_cols = ["Quantity", "Discount", "Sales", "Profit", "Profit Margin"]
corr = df[corr_cols].corr()
print("\n=== CORRELATION MATRIX ===")
print(corr.round(3))
corr.round(3).to_csv("correlation_matrix.csv")

# ==================== CHARTS ====================

# 1. Distribution of Sales & Profit
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.histplot(df["Sales"], bins=50, kde=True, ax=axes[0], color=PALETTE[0])
axes[0].set_title("Distribution of Order Sales")
axes[0].set_xlabel("Sales ($)")
sns.histplot(df["Profit"], bins=50, kde=True, ax=axes[1], color=PALETTE[3])
axes[1].set_title("Distribution of Order Profit")
axes[1].set_xlabel("Profit ($)")
plt.tight_layout()
plt.savefig("charts/01_distributions.png", dpi=150)
plt.close()

# 2. Monthly Sales & Profit trend
monthly = df.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
fig, ax1 = plt.subplots(figsize=(13, 5.5))
ax1.plot(monthly["Month"], monthly["Sales"], color=PALETTE[0], linewidth=2.2, label="Sales")
ax1.set_ylabel("Total Sales ($)", color=PALETTE[0])
ax1.tick_params(axis='y', labelcolor=PALETTE[0])
ax2 = ax1.twinx()
ax2.plot(monthly["Month"], monthly["Profit"], color=PALETTE[4], linewidth=2.2, label="Profit")
ax2.set_ylabel("Total Profit ($)", color=PALETTE[4])
ax2.tick_params(axis='y', labelcolor=PALETTE[4])
ax1.set_title("Monthly Sales & Profit Trend (2023\u20132025)")
ax1.grid(True, alpha=0.3)
fig.tight_layout()
plt.savefig("charts/02_monthly_trend.png", dpi=150)
plt.close()

# 3. Sales & Profit by Category
cat_summary = df.groupby("Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.barplot(x=cat_summary.index, y=cat_summary["Sales"], ax=axes[0], color=PALETTE[1])
axes[0].set_title("Total Sales by Category")
axes[0].set_ylabel("Sales ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
colors = [PALETTE[2] if v >= 0 else PALETTE[4] for v in cat_summary["Profit"]]
sns.barplot(x=cat_summary.index, y=cat_summary["Profit"], ax=axes[1], palette=colors)
axes[1].set_title("Total Profit by Category")
axes[1].set_ylabel("Profit ($)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
plt.tight_layout()
plt.savefig("charts/03_category_sales_profit.png", dpi=150)
plt.close()

# 4. Sub-category profitability (profit margin)
subcat_summary = df.groupby("Sub-Category").agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum")
)
subcat_summary["Margin"] = subcat_summary["Profit"] / subcat_summary["Sales"]
subcat_summary = subcat_summary.sort_values("Margin")
fig, ax = plt.subplots(figsize=(11, 7))
colors = [PALETTE[4] if v < 0 else PALETTE[0] for v in subcat_summary["Margin"]]
ax.barh(subcat_summary.index, subcat_summary["Margin"] * 100, color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Profit Margin (%)")
ax.set_title("Profit Margin by Sub-Category")
plt.tight_layout()
plt.savefig("charts/04_subcategory_margin.png", dpi=150)
plt.close()

# 5. Discount vs Profit Margin scatter
fig, ax = plt.subplots(figsize=(9, 6.5))
sample = df.sample(min(2500, len(df)), random_state=1)
sns.scatterplot(data=sample, x="Discount", y="Profit Margin", hue="Category",
                 palette=PALETTE[:3], alpha=0.5, ax=ax, s=35)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Discount Level vs. Profit Margin")
ax.set_xlabel("Discount")
ax.set_ylabel("Profit Margin")
plt.tight_layout()
plt.savefig("charts/05_discount_vs_margin.png", dpi=150)
plt.close()

# 6. Correlation heatmap
fig, ax = plt.subplots(figsize=(7.5, 6.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax,
            linewidths=0.5, cbar_kws={"label": "Correlation"})
ax.set_title("Correlation Matrix: Key Numeric Variables")
plt.tight_layout()
plt.savefig("charts/06_correlation_heatmap.png", dpi=150)
plt.close()

# 7. Region x Segment sales heatmap
pivot = df.pivot_table(index="Region", columns="Segment", values="Sales", aggfunc="sum")
fig, ax = plt.subplots(figsize=(8.5, 6))
sns.heatmap(pivot / 1000, annot=True, fmt=".0f", cmap="Blues", ax=ax,
            cbar_kws={"label": "Sales ($K)"})
ax.set_title("Total Sales ($K) by Region & Customer Segment")
plt.tight_layout()
plt.savefig("charts/07_region_segment_heatmap.png", dpi=150)
plt.close()

# 8. Ship mode distribution
fig, ax = plt.subplots(figsize=(8.5, 5.5))
order = df["Ship Mode"].value_counts().index
sns.countplot(data=df, y="Ship Mode", order=order, color=PALETTE[1], ax=ax)
ax.set_title("Order Volume by Shipping Mode")
ax.set_xlabel("Number of Orders")
plt.tight_layout()
plt.savefig("charts/08_ship_mode.png", dpi=150)
plt.close()

print("\nAll charts saved to charts/")

# ---------- Key numeric takeaways for the report ----------
summary = {
    "total_orders": len(df),
    "total_sales": df["Sales"].sum(),
    "total_profit": df["Profit"].sum(),
    "overall_margin": df["Profit"].sum() / df["Sales"].sum(),
    "avg_order_value": df["Sales"].mean(),
    "corr_discount_margin": df["Discount"].corr(df["Profit Margin"]),
    "corr_sales_profit": df["Sales"].corr(df["Profit"]),
    "corr_quantity_sales": df["Quantity"].corr(df["Sales"]),
    "best_category_sales": cat_summary["Sales"].idxmax(),
    "worst_margin_subcat": subcat_summary["Margin"].idxmin(),
    "worst_margin_value": subcat_summary["Margin"].min(),
    "best_margin_subcat": subcat_summary["Margin"].idxmax(),
    "best_margin_value": subcat_summary["Margin"].max(),
    "top_region": df.groupby("Region")["Sales"].sum().idxmax(),
    "q4_share": df[df["Month"].dt.month.isin([11,12])]["Sales"].sum() / df["Sales"].sum(),
    "pct_discounted_orders": (df["Discount"] > 0).mean(),
    "loss_making_orders_pct": (df["Profit"] < 0).mean(),
}
import json
with open("summary_stats.json", "w") as f:
    json.dump({k: (round(v,4) if isinstance(v,float) else v) for k,v in summary.items()}, f, indent=2)
print(json.dumps(summary, indent=2, default=str))
