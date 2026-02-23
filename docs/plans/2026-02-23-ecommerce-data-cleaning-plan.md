# Large-Scale E-commerce Data Cleaning & Standardization — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an Upwork portfolio demo — a 125K-row messy dataset, a Jupyter Notebook that cleans it, and a visual HTML case study for PDF conversion.

**Architecture:** A Python script generates a synthetic messy CSV. A Jupyter Notebook loads, explores, cleans, and validates the data step-by-step. A separate HTML file presents the results as a polished, code-free case study. The notebook is built programmatically via `nbformat` so Claude can create it without a running Jupyter kernel.

**Tech Stack:** Python 3.12, Pandas, NumPy, nbformat (notebook creation), Jinja2 (HTML case study), nbconvert (notebook execution)

---

## Task 1: Generate the Messy Dataset

**Files:**
- Create: `generate_messy_data.py`
- Output: `messy_ecommerce_export.csv`

**Step 1: Write `generate_messy_data.py`**

This script produces ~125,000 rows with all the messy patterns from the design doc. Key implementation details:

```python
import pandas as pd
import numpy as np
import random
import string

random.seed(42)
np.random.seed(42)

ROWS = 120_000

# --- order_id: incrementing ORD-10001... ---
order_ids = [f"ORD-{10001 + i}" for i in range(ROWS)]

# --- sku: inconsistent casing ---
sku_base = ["SKU-001", "SKU-002", "SKU-003", "SKU-004", "SKU-005",
            "SKU-010", "SKU-015", "SKU-020", "SKU-025", "SKU-030"]
sku_variants = []
for _ in range(ROWS):
    base = random.choice(sku_base)
    variant = random.choice([base, base.lower(), base.capitalize(), base.replace("-", "")])
    sku_variants.append(variant)

# --- product_name: encoding corruption + trailing whitespace ---
products_clean = [
    "Wireless Bluetooth Headphones",
    "Ergonomic Office Chair",
    "Stainless Steel Water Bottle",
    "Organic Green Tea (Grüner Tee)",
    "Türkçe Klavye Seti",
    "Ölçü Aleti Premium",
    "USB-C Charging Cable",
    "Bamboo Cutting Board",
    "LED Desk Lamp",
    "Cotton Throw Pillow",
]

def corrupt_encoding(text):
    """Simulate Latin-1 misread of UTF-8"""
    try:
        return text.encode("utf-8").decode("latin-1")
    except:
        return text

product_names = []
for _ in range(ROWS):
    name = random.choice(products_clean)
    r = random.random()
    if r < 0.3:
        name = corrupt_encoding(name)
    if random.random() < 0.2:
        name = name + "   "  # trailing whitespace
    product_names.append(name)

# --- order_date: 5 mixed formats ---
from datetime import datetime, timedelta
base_date = datetime(2023, 1, 1)
dates = []
for _ in range(ROWS):
    d = base_date + timedelta(days=random.randint(0, 730))
    fmt = random.choice([
        d.strftime("%m/%d/%Y"),       # 01/02/2024
        d.strftime("%Y-%m-%d"),       # 2024-02-01
        d.strftime("%d-%m-%Y"),       # 02-01-2024
        d.strftime("%b %d, %Y"),      # Feb 01, 2024
        d.strftime("%d.%m.%Y"),       # 01.02.2024
    ])
    dates.append(fmt)

# --- price: mixed currency formats ---
price_values = np.round(np.random.uniform(4.99, 299.99, ROWS), 2)
prices = []
for p in price_values:
    fmt = random.choice([
        f"${p:.2f}",
        f"{p:.2f}",
        f"€{str(p).replace('.', ',')}",
        f"USD {p:.2f}",
        f"{p:.2f} TL",
    ])
    prices.append(fmt)

# --- quantity: mixed types ---
quantities = []
for _ in range(ROWS):
    q = random.randint(1, 20)
    fmt = random.choice([str(q), q, float(q)])
    quantities.append(fmt)

# --- customer_email: various null representations ---
emails_pool = [
    "alice.johnson@gmail.com", "bob.smith@yahoo.com", "carol@outlook.com",
    "dave.wilson@company.co", "emma.brown@email.com", "frank@startup.io",
    "grace.lee@university.edu", "henry.taylor@mail.com",
    None, "N/A", "n/a", "-", "",
]
emails = [random.choice(emails_pool) for _ in range(ROWS)]

# --- customer_phone: mixed formats ---
phone_pool = [
    "+1-555-{:04d}", "555{:04d}", "(555) {:03d}-{:04d}",
    "555.{:03d}.{:04d}", None, "N/A", "",
]
phones = []
for _ in range(ROWS):
    fmt = random.choice(phone_pool)
    if fmt is None or fmt in ("N/A", ""):
        phones.append(fmt)
    elif "{:04d}" in fmt and "{:03d}" not in fmt:
        phones.append(fmt.format(random.randint(1000, 9999)))
    else:
        phones.append(fmt.format(random.randint(100, 999), random.randint(1000, 9999)))

# --- shipping_country: inconsistent ---
country_pool = ["US", "USA", "United States", "us", "CA", "Canada", "canada",
                "GB", "UK", "United Kingdom", "DE", "Germany", "germany",
                "FR", "France", "AU", "Australia"]
countries = [random.choice(country_pool) for _ in range(ROWS)]

# --- status: inconsistent casing + typos ---
status_pool = ["shipped", "Shipped", "SHIPPED", "delivered", "Delivered",
               "deliverred", "processing", "Processing", "cancelled",
               "Cancellled", "pending", "Pending"]
statuses = [random.choice(status_pool) for _ in range(ROWS)]

# --- Build DataFrame ---
df = pd.DataFrame({
    "order_id": order_ids,
    "sku": sku_variants,
    "product_name": product_names,
    "order_date": dates,
    "price": prices,
    "quantity": quantities,
    "customer_email": emails,
    "customer_phone": phones,
    "shipping_country": countries,
    "status": statuses,
    "_unnamed_1": [None] * ROWS,
    "_unnamed_2": [None] * ROWS,
    "notes": [None] * ROWS,
})

# --- Inject ~5000 exact duplicate rows ---
duplicates = df.sample(n=5000, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle

df.to_csv("messy_ecommerce_export.csv", index=False)
print(f"Generated {len(df)} rows, {len(df.columns)} columns")
print(f"File size: {round(df.memory_usage(deep=True).sum() / 1024 / 1024, 1)} MB in memory")
```

**Step 2: Run it and verify the output**

Run: `python generate_messy_data.py`
Expected: prints row count (~125,000) and column count (13). Creates `messy_ecommerce_export.csv`.

Verify: `python -c "import pandas as pd; df=pd.read_csv('messy_ecommerce_export.csv'); print(df.shape); print(df.dtypes); print(df.head(3))"`
Expected: (125000, 13), mixed dtypes, visibly messy data.

**Step 3: Commit**

```bash
git add generate_messy_data.py
git commit -m "feat: add messy dataset generator (125K rows, 13 cols, 8 data quality issues)"
```

Note: Do NOT commit the CSV (it's large and generated).

---

## Task 2: Build the Jupyter Notebook — Sections 1 & 2 (Intro + Exploration)

**Files:**
- Create: `data_cleaning_portfolio.ipynb` (via nbformat)

**Step 1: Write the notebook programmatically**

Use `nbformat` to create the notebook. Build a Python script `build_notebook.py` that constructs all cells. This task covers Sections 1-2 only.

```python
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}

cells = []

# ===== SECTION 1: INTRODUCTION =====
cells.append(nbf.v4.new_markdown_cell("""# Large-Scale E-commerce Data Cleaning & Standardization

## Problem Statement

E-commerce platforms frequently export data with inconsistent formatting, duplicate records, encoding errors, and mixed data types. This notebook demonstrates a systematic approach to cleaning and standardizing a **125,000-row dataset** with **8 distinct data quality issues**.

Simulated large-scale e-commerce export for demonstration purposes.

### Issues Identified
1. **Duplicate records** (~5,000 exact duplicates)
2. **Mixed date formats** (5 different formats)
3. **Currency formatting** (embedded symbols: $, €, TL, USD)
4. **SKU casing inconsistencies** (SKU-001, sku-001, Sku-001)
5. **Missing values** (multiple null representations: None, N/A, -, "")
6. **Encoding corruption** (UTF-8 → Latin-1 artifacts)
7. **Inconsistent country names** (US, USA, United States, us)
8. **Status field typos** (deliverred, Cancellled)
"""))

# ===== SECTION 2: INITIAL EXPLORATION =====
cells.append(nbf.v4.new_markdown_cell("## 1. Initial Data Exploration"))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

df_raw = pd.read_csv("messy_ecommerce_export.csv")
print(f"Dataset shape: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")
"""))

cells.append(nbf.v4.new_code_cell("""# Data types overview
df_raw.dtypes
"""))

cells.append(nbf.v4.new_code_cell("""# First 10 rows — notice the messy patterns
df_raw.head(10)
"""))

cells.append(nbf.v4.new_code_cell("""# Missing values summary
null_summary = df_raw.isnull().sum().to_frame("null_count")
null_summary["null_pct"] = (null_summary["null_count"] / len(df_raw) * 100).round(1)
null_summary[null_summary["null_count"] > 0]
"""))

cells.append(nbf.v4.new_code_cell("""# Duplicate rows
dup_count = df_raw.duplicated().sum()
print(f"Exact duplicate rows: {dup_count:,}")
"""))

cells.append(nbf.v4.new_code_cell("""# Save before-cleaning snapshot for comparison
before_shape = df_raw.shape
before_dtypes = df_raw.dtypes.to_dict()
before_nulls = df_raw.isnull().sum().to_dict()
before_sample = df_raw.head(6).copy()
print("Before-snapshot saved.")
"""))

nb.cells = cells
```

This is the first part of `build_notebook.py`. Continue in Task 3.

**Step 2: (no separate run yet — notebook is built across Tasks 2–5)**

---

## Task 3: Build the Notebook — Section 3 (Cleaning Pipeline)

**Files:**
- Modify: `build_notebook.py` (append cleaning cells)

**Step 1: Append all cleaning pipeline cells**

Continue appending to the `cells` list:

```python
# ===== SECTION 3: CLEANING PIPELINE =====
cells.append(nbf.v4.new_markdown_cell("""## 2. Data Cleaning Pipeline

Each step is timed independently. The pipeline is modular — steps can be reordered or extended.
"""))

# --- Step 1: Drop empty columns ---
cells.append(nbf.v4.new_markdown_cell("### Step 1: Drop Empty Columns"))
cells.append(nbf.v4.new_code_cell("""%%time
empty_cols = [col for col in df_raw.columns if df_raw[col].isnull().all()]
print(f"Dropping {len(empty_cols)} empty columns: {empty_cols}")
df = df_raw.drop(columns=empty_cols).copy()
print(f"Shape after: {df.shape}")
"""))

# --- Step 2: Remove duplicates ---
cells.append(nbf.v4.new_markdown_cell("### Step 2: Remove Duplicate Rows"))
cells.append(nbf.v4.new_code_cell("""%%time
before_dedup = len(df)
df = df.drop_duplicates()
removed = before_dedup - len(df)
print(f"Removed {removed:,} duplicate rows")
print(f"Shape after: {df.shape}")
"""))

# --- Step 3: Standardize dates ---
cells.append(nbf.v4.new_markdown_cell("### Step 3: Standardize Date Formats → ISO 8601"))
cells.append(nbf.v4.new_code_cell("""%%time
print("Before — sample date values:")
print(df["order_date"].value_counts().head(10))
print()

def parse_date(val):
    if pd.isna(val):
        return val
    val = str(val).strip()
    for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y", "%b %d, %Y", "%d.%m.%Y"]:
        try:
            return pd.to_datetime(val, format=fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return val

df["order_date"] = df["order_date"].apply(parse_date)
date_issues = df["order_date"].apply(lambda x: len(str(x)) != 10 if pd.notna(x) else False).sum()
print(f"After — unparseable dates remaining: {date_issues}")
print(f"Sample: {df['order_date'].head()}")
"""))

# --- Step 4: Normalize prices ---
cells.append(nbf.v4.new_markdown_cell("### Step 4: Normalize Price Column → Float"))
cells.append(nbf.v4.new_code_cell("""%%time
print("Before — sample price values:")
print(df["price"].value_counts().head(10))
print()

def clean_price(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip()
    # Remove currency symbols and words
    for remove in ["$", "€", "USD", "TL"]:
        val = val.replace(remove, "")
    val = val.strip()
    # Handle European comma decimal separator
    if "," in val and "." not in val:
        val = val.replace(",", ".")
    elif "," in val and "." in val:
        val = val.replace(",", "")
    try:
        return round(float(val), 2)
    except ValueError:
        return np.nan

df["price"] = df["price"].apply(clean_price)
print(f"After — dtype: {df['price'].dtype}")
print(f"Price range: ${df['price'].min():.2f} — ${df['price'].max():.2f}")
print(f"Null prices: {df['price'].isna().sum()}")
"""))

# --- Step 5: SKU standardization ---
cells.append(nbf.v4.new_markdown_cell("### Step 5: Standardize SKU Format"))
cells.append(nbf.v4.new_code_cell("""%%time
print("Before — unique SKU variants:")
print(df["sku"].value_counts().head(15))
print()

def clean_sku(val):
    if pd.isna(val):
        return val
    val = str(val).strip().upper()
    if not val.startswith("SKU-"):
        # Handle cases like "SKU001" -> "SKU-001"
        val = val.replace("SKU", "SKU-") if "SKU" in val else val
    # Remove double dashes
    val = val.replace("--", "-")
    return val

df["sku"] = df["sku"].apply(clean_sku)
print(f"After — unique SKUs: {df['sku'].nunique()}")
print(df["sku"].value_counts())
"""))

# --- Step 6: Handle missing values ---
cells.append(nbf.v4.new_markdown_cell("### Step 6: Normalize Missing Values"))
cells.append(nbf.v4.new_code_cell("""%%time
null_representations = ["N/A", "n/a", "na", "NA", "-", "--", ".", "none", "None", "null", "NULL", ""]

for col in ["customer_email", "customer_phone"]:
    mask = df[col].isin(null_representations)
    count = mask.sum()
    df.loc[mask, col] = np.nan
    print(f"{col}: coerced {count:,} fake nulls to NaN")

print(f"\\nTotal nulls after normalization:")
print(df[["customer_email", "customer_phone"]].isnull().sum())
"""))

# --- Step 7: Fix encoding ---
cells.append(nbf.v4.new_markdown_cell("### Step 7: Fix Encoding Corruption in Product Names"))
cells.append(nbf.v4.new_code_cell("""%%time
print("Before — sample corrupted names:")
corrupted = df[df["product_name"].str.contains("Ã", na=False)]
print(f"Found {len(corrupted):,} rows with encoding artifacts")
print(corrupted["product_name"].value_counts().head(5))
print()

def fix_encoding(val):
    if pd.isna(val):
        return val
    val = str(val).strip()
    try:
        return val.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return val

df["product_name"] = df["product_name"].apply(fix_encoding)
remaining = df[df["product_name"].str.contains("Ã", na=False)]
print(f"After — remaining encoding issues: {len(remaining)}")
print(df["product_name"].value_counts().head(10))
"""))

# --- Step 8: Phone standardization ---
cells.append(nbf.v4.new_markdown_cell("### Step 8: Standardize Phone Numbers"))
cells.append(nbf.v4.new_code_cell("""%%time
import re

print("Before — sample phone formats:")
print(df["customer_phone"].dropna().value_counts().head(10))
print()

def clean_phone(val):
    if pd.isna(val):
        return val
    digits = re.sub(r"\\D", "", str(val))
    if len(digits) == 0:
        return np.nan
    if len(digits) == 7:
        return f"555-{digits[:3]}-{digits[3:]}"
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits[0] == "1":
        return f"{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    return val

df["customer_phone"] = df["customer_phone"].apply(clean_phone)
print("After — sample cleaned phones:")
print(df["customer_phone"].dropna().value_counts().head(5))
"""))

# --- Step 9: Country normalization ---
cells.append(nbf.v4.new_markdown_cell("### Step 9: Normalize Country Names → ISO Codes"))
cells.append(nbf.v4.new_code_cell("""%%time
country_map = {
    "us": "US", "usa": "US", "united states": "US",
    "ca": "CA", "canada": "CA",
    "gb": "GB", "uk": "GB", "united kingdom": "GB",
    "de": "DE", "germany": "DE",
    "fr": "FR", "france": "FR",
    "au": "AU", "australia": "AU",
}

print("Before — country variants:")
print(df["shipping_country"].value_counts())
print()

df["shipping_country"] = df["shipping_country"].str.strip().str.lower().map(country_map).fillna(df["shipping_country"])
print("After — standardized:")
print(df["shipping_country"].value_counts())
"""))

# --- Step 10: Status cleanup ---
cells.append(nbf.v4.new_markdown_cell("### Step 10: Fix Status Typos & Casing"))
cells.append(nbf.v4.new_code_cell("""%%time
status_map = {
    "shipped": "shipped",
    "delivered": "delivered",
    "deliverred": "delivered",
    "processing": "processing",
    "cancelled": "cancelled",
    "cancellled": "cancelled",
    "pending": "pending",
}

print("Before:")
print(df["status"].value_counts())
print()

df["status"] = df["status"].str.strip().str.lower().map(status_map).fillna(df["status"])
print("After:")
print(df["status"].value_counts())
"""))
```

---

## Task 4: Build the Notebook — Section 4 (Validation & Summary)

**Files:**
- Modify: `build_notebook.py` (append validation cells)

**Step 1: Append validation and summary cells**

```python
# ===== SECTION 4: VALIDATION & SUMMARY =====
cells.append(nbf.v4.new_markdown_cell("## 3. Validation & Results"))

# --- Cleaning Summary Table ---
cells.append(nbf.v4.new_markdown_cell("### Cleaning Summary"))
cells.append(nbf.v4.new_code_cell("""summary_data = {
    "Issue": [
        "Empty columns",
        "Duplicate rows",
        "Mixed date formats",
        "Currency formatting",
        "SKU casing inconsistencies",
        "Fake null values (email/phone)",
        "Encoding corruption",
        "Phone format inconsistencies",
        "Country name variants",
        "Status typos & casing",
    ],
    "Rows Affected": [
        f"{before_shape[0]:,} (3 columns)",
        f"{before_shape[0] - len(df):,}",
        f"{before_shape[0]:,}",
        f"{before_shape[0]:,}",
        f"{sum(1 for s in df_raw['sku'] if s != str(s).upper()):,}",
        f"{sum(df_raw[col].isin(['N/A','n/a','-','']).sum() for col in ['customer_email','customer_phone']):,}",
        f"{len(df_raw[df_raw['product_name'].str.contains('Ã', na=False)]):,}",
        f"{df_raw['customer_phone'].dropna().apply(lambda x: bool(re.search(r'[^0-9]', str(x)))).sum():,}",
        f"{sum(1 for c in df_raw['shipping_country'] if str(c).lower() != str(c)):,}",
        f"{sum(1 for s in df_raw['status'] if str(s).lower() != str(s) or str(s).lower() in ['deliverred','cancellled']):,}",
    ],
    "Action Taken": [
        "Dropped",
        "Removed",
        "Standardized to ISO 8601",
        "Converted to float",
        "Normalized to SKU-XXX",
        "Coerced to NaN",
        "Re-encoded Latin-1 → UTF-8",
        "Standardized to XXX-XXX-XXXX",
        "Mapped to ISO country codes",
        "Corrected typos, lowercased",
    ],
}

summary_df = pd.DataFrame(summary_data)
summary_df.style.set_properties(**{"text-align": "left"}).hide(axis="index")
"""))

# --- Data Type Audit ---
cells.append(nbf.v4.new_markdown_cell("### Data Type Audit"))
cells.append(nbf.v4.new_code_cell("""dtype_comparison = pd.DataFrame({
    "Column": [c for c in df.columns],
    "Before": [str(before_dtypes.get(c, "N/A")) for c in df.columns],
    "After": [str(df[c].dtype) for c in df.columns],
})
dtype_comparison["Changed"] = dtype_comparison["Before"] != dtype_comparison["After"]
dtype_comparison.style.applymap(
    lambda v: "background-color: #d4edda" if v == True else "",
    subset=["Changed"]
).hide(axis="index")
"""))

# --- Schema Comparison ---
cells.append(nbf.v4.new_markdown_cell("### Schema Comparison (Before → After)"))
cells.append(nbf.v4.new_code_cell("""schema = pd.DataFrame({
    "Metric": ["Rows", "Columns", "Total null cells", "Duplicate rows", "Numeric columns"],
    "Before": [
        f"{before_shape[0]:,}",
        f"{before_shape[1]}",
        f"{sum(before_nulls.values()):,}",
        f"{df_raw.duplicated().sum():,}",
        f"{sum(1 for d in before_dtypes.values() if 'float' in str(d) or 'int' in str(d))}",
    ],
    "After": [
        f"{len(df):,}",
        f"{len(df.columns)}",
        f"{df.isnull().sum().sum():,}",
        f"{df.duplicated().sum():,}",
        f"{sum(1 for d in df.dtypes if 'float' in str(d) or 'int' in str(d))}",
    ],
})
schema.style.hide(axis="index")
"""))

# --- Before/After Sample ---
cells.append(nbf.v4.new_markdown_cell("### Before / After — Sample Data"))
cells.append(nbf.v4.new_code_cell("""print("=== BEFORE (raw data) ===")
before_sample
"""))
cells.append(nbf.v4.new_code_cell("""print("=== AFTER (cleaned data) ===")
df.head(6)
"""))

# --- Processing Time ---
cells.append(nbf.v4.new_markdown_cell("### Performance"))
cells.append(nbf.v4.new_code_cell("""# This cell measures total pipeline time when run end-to-end
print(f"Dataset: {before_shape[0]:,} rows × {before_shape[1]} columns")
print(f"Cleaned: {len(df):,} rows × {len(df.columns)} columns")
print(f"Records removed: {before_shape[0] - len(df):,}")
print()
print("The cleaning pipeline is modular and reusable for future dataset updates.")
print("Each step can be independently configured or extended for different data sources.")
"""))
```

---

## Task 5: Build the Notebook — Section 5 (Export) + Write & Execute

**Files:**
- Modify: `build_notebook.py` (append export cell, write notebook)
- Output: `data_cleaning_portfolio.ipynb`

**Step 1: Append export cells and save notebook**

```python
# ===== SECTION 5: EXPORT =====
cells.append(nbf.v4.new_markdown_cell("## 4. Export"))
cells.append(nbf.v4.new_code_cell("""df.to_csv("cleaned_ecommerce_data.csv", index=False)
print(f"Exported {len(df):,} rows to cleaned_ecommerce_data.csv")
print(f"Columns: {list(df.columns)}")
"""))

# === ASSEMBLE AND WRITE ===
nb.cells = cells

with open("data_cleaning_portfolio.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook written: data_cleaning_portfolio.ipynb")
```

**Step 2: Run `build_notebook.py`**

Run: `python build_notebook.py`
Expected: Creates `data_cleaning_portfolio.ipynb`

**Step 3: Execute the notebook**

Run: `jupyter nbconvert --to notebook --execute data_cleaning_portfolio.ipynb --output data_cleaning_portfolio.ipynb --ExecutePreprocessor.timeout=120`
Expected: Notebook executes all cells, outputs are embedded. Creates `cleaned_ecommerce_data.csv`.

**Step 4: Verify outputs**

Run: `python -c "import pandas as pd; df=pd.read_csv('cleaned_ecommerce_data.csv'); print(df.shape); print(df.dtypes); print(df.head(3))"`
Expected: ~120,000 rows, 10 columns (3 empty ones dropped), clean dtypes, no messy patterns visible.

**Step 5: Commit**

```bash
git add build_notebook.py data_cleaning_portfolio.ipynb
git commit -m "feat: add data cleaning notebook with full pipeline and validation"
```

---

## Task 6: Build the HTML Case Study

**Files:**
- Create: `build_case_study.py`
- Output: `case_study.html`

**Step 1: Write `build_case_study.py`**

This script reads both CSVs (messy + cleaned) and the executed notebook to extract stats, then generates a polished HTML case study. Uses inline CSS for styling — no external dependencies.

The HTML should be structured as 7 visual "pages" (sections with page-break-after for print):

**Page 1 — Title**
- "Large-Scale E-commerce Data Cleaning & Standardization"
- Subtitle: "125,000 Rows | 12 Columns | 8 Data Quality Issues"
- Brief problem statement (3 sentences)

**Page 2 — The Problem (Before)**
- Table: 5-6 rows of raw messy data
- Sidebar list of issues found

**Page 3 — Cleaning Summary Table**
- The full Issue / Rows Affected / Action Taken table
- This is THE centerpiece

**Page 4 — The Result (After)**
- Table: 5-6 rows of cleaned data
- Schema comparison (before/after metrics)

**Page 5 — Validation**
- Data type audit table
- Null analysis before/after

**Page 6 — Performance & Approach**
- Processing time callout
- Tech stack (Python, Pandas, NumPy)
- "The cleaning pipeline is modular and reusable..."

**Page 7 — Footer**
- "Simulated large-scale e-commerce export for demonstration purposes."
- Contact info placeholder

Key implementation detail: read the actual CSV files to get real numbers, don't hardcode.

```python
import pandas as pd
import re
import numpy as np

# Load data
df_raw = pd.read_csv("messy_ecommerce_export.csv")
df_clean = pd.read_csv("cleaned_ecommerce_data.csv")

# Compute stats
raw_rows, raw_cols = df_raw.shape
clean_rows, clean_cols = df_clean.shape
duplicates_removed = raw_rows - clean_rows
# ... (compute all summary stats from the actual data)

# Build HTML with inline CSS
html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Large-Scale E-commerce Data Cleaning & Standardization</title>
<style>
  @page {{ size: A4; margin: 2cm; }}
  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; ... }}
  .page {{ page-break-after: always; min-height: 90vh; padding: 40px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th {{ background: #2c3e50; color: white; padding: 12px; }}
  td {{ padding: 10px; border-bottom: 1px solid #eee; }}
  .metric-card {{ background: #f8f9fa; border-left: 4px solid #3498db; padding: 20px; margin: 10px 0; }}
  .highlight {{ color: #e74c3c; font-weight: bold; }}
  ...
</style>
</head>
<body>
  <!-- Page 1: Title -->
  <div class="page"> ... </div>
  <!-- Page 2: Before -->
  <div class="page"> ... </div>
  <!-- ... etc ... -->
</body>
</html>"""

with open("case_study.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Case study written: case_study.html")
```

Full implementation code goes here (the complete HTML template with f-string interpolation for all dynamic values).

**Step 2: Run it**

Run: `python build_case_study.py`
Expected: Creates `case_study.html`

**Step 3: Verify**

Open `case_study.html` in browser. Verify 7 sections render properly. Print > Save as PDF to verify page breaks.

**Step 4: Commit**

```bash
git add build_case_study.py case_study.html
git commit -m "feat: add visual HTML case study for PDF portfolio"
```

---

## Task 7: Final Verification & Cleanup

**Files:**
- Verify: all outputs exist and are correct

**Step 1: Verify all files exist**

```bash
ls -la messy_ecommerce_export.csv cleaned_ecommerce_data.csv data_cleaning_portfolio.ipynb case_study.html
```

**Step 2: Verify notebook executes cleanly**

Run: `jupyter nbconvert --to notebook --execute data_cleaning_portfolio.ipynb --output /dev/null --ExecutePreprocessor.timeout=120`
Expected: exits 0, no errors.

**Step 3: Verify cleaned data is actually clean**

```python
python -c "
import pandas as pd
df = pd.read_csv('cleaned_ecommerce_data.csv')
assert df.duplicated().sum() == 0, 'Still has duplicates'
assert df['price'].dtype == 'float64', 'Price not float'
assert all(len(str(d)) == 10 for d in df['order_date'].dropna()), 'Dates not ISO'
assert not df['product_name'].str.contains('Ã', na=False).any(), 'Encoding issues remain'
assert all(s == s.lower() for s in df['status'].dropna()), 'Status not lowercase'
print('All validations passed!')
"
```

**Step 4: Add .gitignore**

```
messy_ecommerce_export.csv
cleaned_ecommerce_data.csv
```

**Step 5: Final commit**

```bash
git add .gitignore
git commit -m "chore: add gitignore for generated CSV files"
```

---

## Execution Summary

| Task | What | Approx Time |
|------|------|-------------|
| 1 | Generate messy dataset | 3 min |
| 2 | Notebook sections 1-2 | 3 min |
| 3 | Notebook section 3 (cleaning) | 5 min |
| 4 | Notebook section 4 (validation) | 3 min |
| 5 | Notebook section 5 + execute | 3 min |
| 6 | HTML case study | 5 min |
| 7 | Final verification | 2 min |
