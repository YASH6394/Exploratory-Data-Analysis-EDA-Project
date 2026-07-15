# Business Sales — Exploratory Data Analysis

An EDA project on a synthetic 3-year business sales dataset (9,800 orders), exploring
sales, profitability, discounting behavior, and regional/segment patterns.

## Contents

| File | Description |
|---|---|
| `business_sales_data.csv` | The dataset — 9,800 order-level records (Jan 2023–Dec 2025) |
| `generate_data.py` | Script that generated the synthetic dataset |
| `eda_analysis.py` | Full analysis pipeline: statistical summaries, correlations, and chart generation |
| `EDA_Report.docx` | Structured written report with findings, charts, and recommendations |
| `summary_stats.json` | Key headline metrics in machine-readable form |
| `correlation_matrix.csv` | Correlation matrix of core numeric variables |
| `charts/` | All generated visualizations (PNG) |

## Dataset Overview

Each row is one order line item with the following fields:

- **Order ID, Order Date, Ship Date, Ship Mode**
- **Segment**: Consumer, Corporate, Home Office
- **Region / State**
- **Category / Sub-Category**
- **Quantity, Discount, Sales, Profit**

## Key Findings

- Discount depth is the strongest driver of profitability (r ≈ -0.74 with profit margin) —
  deep discounts consistently push orders into a loss.
- ~26.5% of orders were sold at a loss.
- Furniture (especially Tables) is high-revenue but low/negative margin; Paper is the
  most efficient sub-category by margin.
- Clear Q4 seasonality — November/December alone account for ~15.5% of annual sales.
- The West region leads in total sales, driven mainly by the Consumer segment.

See `EDA_Report.docx` for the full write-up with visuals and recommendations.

## Reproducing the Analysis

```bash
pip install pandas numpy matplotlib seaborn

python generate_data.py    # regenerates business_sales_data.csv
python eda_analysis.py     # runs the EDA, prints stats, saves charts/ and summary_stats.json
```

## Methodology

1. **Data inspection** — shape, dtypes, missing values, duplicates
2. **Descriptive statistics** — summary stats for numeric fields, frequency counts for categoricals
3. **Correlation analysis** — Pearson correlation across Quantity, Discount, Sales, Profit, Profit Margin
4. **Visualization** — distributions, time trends, category/sub-category breakdowns, discount-vs-margin
   scatter, correlation heatmap, region×segment heatmap
5. **Insight synthesis** — translating statistical patterns into business recommendations
