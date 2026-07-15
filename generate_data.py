import numpy as np
import pandas as pd
from datetime import timedelta

rng = np.random.default_rng(42)

N = 9800

regions = ["West", "East", "Central", "South"]
region_weights = [0.32, 0.29, 0.24, 0.15]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.51, 0.30, 0.19]

categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels", "Fasteners"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}

ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
ship_weights = [0.60, 0.19, 0.16, 0.05]

states_by_region = {
    "West": ["California", "Washington", "Oregon", "Nevada", "Arizona"],
    "East": ["New York", "Pennsylvania", "New Jersey", "Massachusetts", "Virginia"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan", "Minnesota"],
    "South": ["Florida", "Georgia", "North Carolina", "Tennessee", "Alabama"],
}

# base unit price and margin characteristics per sub-category (creates realistic correlations)
subcat_profile = {
    "Chairs": (110, 0.12), "Tables": (270, -0.02), "Bookcases": (180, 0.03), "Furnishings": (45, 0.18),
    "Binders": (18, 0.28), "Paper": (9, 0.32), "Storage": (55, 0.15), "Art": (12, 0.25),
    "Labels": (6, 0.30), "Fasteners": (5, 0.22),
    "Phones": (320, 0.14), "Machines": (450, 0.05), "Accessories": (60, 0.24), "Copiers": (900, 0.10),
}

start_date = pd.Timestamp("2023-01-01")
end_date = pd.Timestamp("2025-12-31")
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    region = rng.choice(regions, p=region_weights)
    state = rng.choice(states_by_region[region])
    segment = rng.choice(segments, p=segment_weights)
    category = rng.choice(list(categories.keys()), p=[0.21, 0.60, 0.19])
    subcat = rng.choice(categories[category])
    base_price, base_margin = subcat_profile[subcat]

    # seasonality: boost sales probability in Nov/Dec (Q4)
    day_offset = int(rng.triangular(0, date_range_days * 0.85, date_range_days))
    order_date = start_date + timedelta(days=day_offset)
    if order_date.month in (11, 12) and rng.random() < 0.4:
        order_date = order_date.replace(day=min(order_date.day, 28))

    ship_mode = rng.choice(ship_modes, p=ship_weights)
    ship_days = {"Same Day": 0, "First Class": 2, "Second Class": 4, "Standard Class": 6}[ship_mode]
    ship_date = order_date + timedelta(days=int(rng.integers(ship_days, ship_days + 3)))

    quantity = int(rng.integers(1, 11))
    # discount more common on Home Office / Corporate bulk orders
    discount = rng.choice([0.0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5],
                           p=[0.42, 0.18, 0.13, 0.12, 0.08, 0.05, 0.02])

    unit_price = max(2, rng.normal(base_price, base_price * 0.25))
    sales = round(unit_price * quantity * (1 - discount * 0.3), 2)  # discount partially eats list price too
    # profit erodes sharply as discount rises; margin varies by subcategory
    margin = base_margin - discount * 0.9 + rng.normal(0, 0.04)
    profit = round(sales * margin, 2)

    rows.append({
        "Order ID": f"ORD-{100000+i}",
        "Order Date": order_date.date().isoformat(),
        "Ship Date": ship_date.date().isoformat(),
        "Ship Mode": ship_mode,
        "Segment": segment,
        "Region": region,
        "State": state,
        "Category": category,
        "Sub-Category": subcat,
        "Quantity": quantity,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# sprinkle a few missing values to make the EDA realistic
missing_idx = rng.choice(df.index, size=25, replace=False)
df.loc[missing_idx, "Ship Mode"] = np.nan

df.to_csv("business_sales_data.csv", index=False)
print(df.shape)
print(df.head())
print(df.isna().sum())
