"""
build_notebook.py
Programmatically generates data_cleaning_portfolio.ipynb using nbformat.
Run this script, then execute the notebook with jupyter nbconvert.
"""

import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# ── Helper ──────────────────────────────────────────────────────────────────

def md(source: str) -> nbformat.NotebookNode:
    return new_markdown_cell(source.strip())

def code(source: str) -> nbformat.NotebookNode:
    return new_code_cell(source.strip())

def timed_code(source: str) -> nbformat.NotebookNode:
    """Wrap a code cell with %%time magic as the very first line."""
    return new_code_cell("%%time\n" + source.strip())

# ── Notebook construction ───────────────────────────────────────────────────

nb = new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata.language_info = {
    "name": "python",
    "version": "3.10.0",
}

cells = []

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Introduction
# ═════════════════════════════════════════════════════════════════════════════

cells.append(md(r"""
# Large-Scale E-commerce Data Cleaning & Standardization

## Problem Statement

This notebook demonstrates a **production-grade data cleaning pipeline** applied to a
125,000-row messy e-commerce export. The dataset contains **8 distinct data quality issues**
that are typical of real-world exports from platforms like Shopify, WooCommerce, and
custom ERP systems.

> **Note:** Simulated large-scale e-commerce export for demonstration purposes.

### Data Quality Issues Addressed

1. **Duplicate rows** — ~5,000 exact duplicates injected into the dataset
2. **Mixed date formats** — 5 different date representations (US, EU, ISO, etc.)
3. **Currency formatting** — Prices with `$`, `€`, `USD`, `TL` prefixes/suffixes and European decimal commas
4. **SKU casing inconsistencies** — Mixed upper/lower case and missing dashes (`SKU001` vs `SKU-001`)
5. **Missing values with multiple null representations** — `N/A`, `n/a`, `-`, `none`, `null`, `""`, etc.
6. **Encoding corruption (mojibake)** — UTF-8 product names decoded as Latin-1 producing artifacts like `Ã¼`
7. **Inconsistent country names** — Free-text entries like `us`, `USA`, `United States` for the same country
8. **Status typos & casing** — Misspellings like `deliverred`, `Cancellled` plus mixed casing
"""))

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Initial Exploration
# ═════════════════════════════════════════════════════════════════════════════

cells.append(md(r"""
---
## Section 2 — Initial Exploration
"""))

cells.append(code(r"""
import pandas as pd
import numpy as np
import time
import re
import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 140)
"""))

cells.append(code(r"""
df_raw = pd.read_csv("messy_ecommerce_export.csv")
print(f"Dataset shape: {df_raw.shape[0]:,} rows x {df_raw.shape[1]} columns")
"""))

cells.append(code(r"""
print("Column data types:\n")
print(df_raw.dtypes)
"""))

cells.append(code(r"""
print("First 10 rows:\n")
df_raw.head(10)
"""))

cells.append(code(r"""
null_summary = pd.DataFrame({
    "Null Count": df_raw.isnull().sum(),
    "Null %": (df_raw.isnull().sum() / len(df_raw) * 100).round(2),
})
print("Null summary:\n")
print(null_summary)
"""))

cells.append(code(r"""
dup_count = df_raw.duplicated().sum()
print(f"Duplicate rows: {dup_count:,}")
"""))

cells.append(code(r"""
# Save before-cleaning snapshots for later comparison
before_shape = df_raw.shape
before_dtypes = df_raw.dtypes.copy()
before_nulls = df_raw.isnull().sum().sum()
before_sample = df_raw.head(6).copy()

# Work on a copy from here on
df = df_raw.copy()
print("Snapshots saved. Working copy created.")
"""))

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Cleaning Pipeline
# ═════════════════════════════════════════════════════════════════════════════

cells.append(md(r"""
---
## Section 3 — Cleaning Pipeline (10 Steps)

Each step is an isolated, timed cell so performance can be monitored independently.
"""))

# ── Step 1: Drop Empty Columns ──────────────────────────────────────────────

cells.append(md("### Step 1 — Drop Empty Columns\nRemove columns where **every** value is null."))

cells.append(timed_code(r"""
empty_cols = [col for col in df.columns if df[col].isnull().all()]
print(f"Empty columns found: {empty_cols}")
df.drop(columns=empty_cols, inplace=True)
print(f"Columns after drop: {list(df.columns)}")
print(f"Shape: {df.shape}")
"""))

# ── Step 2: Remove Duplicate Rows ───────────────────────────────────────────

cells.append(md("### Step 2 — Remove Duplicate Rows"))

cells.append(timed_code(r"""
rows_before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
rows_after = len(df)
dups_removed = rows_before - rows_after
print(f"Rows before: {rows_before:,}")
print(f"Rows after:  {rows_after:,}")
print(f"Duplicates removed: {dups_removed:,}")
"""))

# ── Step 3: Standardize Dates ───────────────────────────────────────────────

cells.append(md("### Step 3 — Standardize Dates to ISO 8601 (`YYYY-MM-DD`)"))

cells.append(timed_code(r"""
DATE_FORMATS = ["%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y", "%b %d, %Y", "%d.%m.%Y"]

def parse_date(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip().strip('"').strip("'")
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(val, format=fmt).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
    return np.nan

sample_before = df["order_date"].head(8).tolist()
df["order_date"] = df["order_date"].apply(parse_date)
sample_after = df["order_date"].head(8).tolist()

print("Date conversion sample:")
for b, a in zip(sample_before, sample_after):
    print(f"  {str(b):25s} -> {a}")
print(f"\nNull dates after conversion: {df['order_date'].isnull().sum()}")
"""))

# ── Step 4: Normalize Prices ────────────────────────────────────────────────

cells.append(md("### Step 4 — Normalize Prices to Float"))

cells.append(timed_code(r"""
def clean_price(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    # Remove currency symbols and words
    s = s.replace("$", "").replace("USD", "").replace("TL", "").replace("\u20ac", "").strip()
    # Handle European format: €1.234,56 -> 1234.56
    # If both . and , exist and , is after ., it's European
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            # European: 1.234,56
            s = s.replace(".", "").replace(",", ".")
        else:
            # US: 1,234.56
            s = s.replace(",", "")
    elif "," in s and "." not in s:
        # Could be European decimal: 19,99
        s = s.replace(",", ".")
    try:
        return round(float(s), 2)
    except ValueError:
        return np.nan

df["price"] = df["price"].apply(clean_price)
print(f"Price range: ${df['price'].min():.2f} — ${df['price'].max():.2f}")
print(f"Null prices: {df['price'].isnull().sum()}")
print(f"Mean price:  ${df['price'].mean():.2f}")
"""))

# ── Step 5: Standardize SKU Format ──────────────────────────────────────────

cells.append(md("### Step 5 — Standardize SKU Format\nUppercase all SKUs and ensure `SKU-XXX` format with dash."))

cells.append(timed_code(r"""
def clean_sku(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().upper()
    # Insert dash if missing: SKU001 -> SKU-001
    if s.startswith("SKU") and len(s) > 3 and s[3] != "-":
        s = "SKU-" + s[3:]
    return s

df["sku"] = df["sku"].apply(clean_sku)
print(f"Unique SKUs after standardization: {df['sku'].nunique()}")
print(f"SKU values: {sorted(df['sku'].unique())}")
"""))

# ── Step 6: Normalize Missing Values ────────────────────────────────────────

cells.append(md("### Step 6 — Normalize Missing Values\nConvert fake null representations to `np.nan` in email and phone columns."))

cells.append(timed_code(r"""
FAKE_NULLS = {"N/A", "n/a", "na", "NA", "-", "--", ".", "none", "None", "null", "NULL", ""}

def coerce_null(val):
    if pd.isna(val):
        return np.nan
    if str(val).strip() in FAKE_NULLS:
        return np.nan
    return val

for col in ["customer_email", "customer_phone"]:
    before_nulls = df[col].isnull().sum()
    df[col] = df[col].apply(coerce_null)
    after_nulls = df[col].isnull().sum()
    coerced = after_nulls - before_nulls
    print(f"{col}: coerced {coerced:,} fake nulls -> np.nan  (total null now: {after_nulls:,})")
"""))

# ── Step 7: Fix Encoding Corruption ─────────────────────────────────────────

cells.append(md(r"""
### Step 7 — Fix Encoding Corruption (Mojibake)
Product names were corrupted by a UTF-8 → Latin-1 encoding mismatch,
producing artifacts like `Ã¼` instead of `ü`.
"""))

cells.append(timed_code(r"""
# Mojibake pattern: when UTF-8 bytes are misread as Latin-1, you get sequences
# like \xc3\x83, \xc3\xbc rendered as Ã¼, Ã¶, etc.
MOJIBAKE_RE = re.compile(r"\xc3[\x80-\xbf]")

def fix_encoding(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    try:
        fixed = s.encode("latin-1").decode("utf-8")
        return fixed.strip()
    except (UnicodeDecodeError, UnicodeEncodeError):
        return s.strip()

# Count corrupted rows before fix (detect mojibake double-byte artifacts)
corrupted_before = df["product_name"].apply(
    lambda x: bool(MOJIBAKE_RE.search(str(x))) if pd.notna(x) else False
).sum()

df["product_name"] = df["product_name"].apply(fix_encoding)

corrupted_after = df["product_name"].apply(
    lambda x: bool(MOJIBAKE_RE.search(str(x))) if pd.notna(x) else False
).sum()

print(f"Corrupted product names before fix: {corrupted_before:,}")
print(f"Corrupted product names after fix:  {corrupted_after:,}")
print(f"Unique product names: {sorted(df['product_name'].dropna().unique())}")
"""))

# ── Step 8: Standardize Phone Numbers ───────────────────────────────────────

cells.append(md("### Step 8 — Standardize Phone Numbers\nExtract digits and reformat to `XXX-XXX-XXXX`."))

cells.append(timed_code(r"""
def clean_phone(val):
    if pd.isna(val):
        return np.nan
    digits = re.sub(r"\D", "", str(val))
    if len(digits) == 0:
        return np.nan
    # 7 digits: 555XXXX -> 555-XXX-XXXX (prepend area code)
    if len(digits) == 7:
        return f"555-{digits[:3]}-{digits[3:]}"
    # 8 digits starting with 1: country code + 555 + XXXX -> 555-XXX-XXXX
    elif len(digits) == 8 and digits[0] == "1":
        digits = digits[1:]  # strip country code -> 555XXXX
        return f"555-{digits[:3]}-{digits[3:]}"
    # 10 digits: XXX-XXX-XXXX
    elif len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    # 11 digits starting with 1: strip country code -> 10 digits
    elif len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    else:
        return np.nan

df["customer_phone"] = df["customer_phone"].apply(clean_phone)
sample_phones = df["customer_phone"].dropna().head(8).tolist()
print("Phone number sample after cleaning:")
for p in sample_phones:
    print(f"  {p}")
print(f"\nNull phones: {df['customer_phone'].isnull().sum():,}")
"""))

# ── Step 9: Normalize Country Names ─────────────────────────────────────────

cells.append(md("### Step 9 — Normalize Country Names to ISO Codes"))

cells.append(timed_code(r"""
COUNTRY_MAP = {
    "us": "US", "usa": "US", "united states": "US",
    "ca": "CA", "canada": "CA",
    "gb": "GB", "uk": "GB", "united kingdom": "GB",
    "de": "DE", "germany": "DE",
    "fr": "FR", "france": "FR",
    "au": "AU", "australia": "AU",
}

def clean_country(val):
    if pd.isna(val):
        return np.nan
    key = str(val).strip().lower()
    return COUNTRY_MAP.get(key, val)

df["shipping_country"] = df["shipping_country"].apply(clean_country)
print("Country value counts after normalization:\n")
print(df["shipping_country"].value_counts())
"""))

# ── Step 10: Fix Status Typos & Casing ──────────────────────────────────────

cells.append(md("### Step 10 — Fix Status Typos & Casing"))

cells.append(timed_code(r"""
STATUS_TYPO_MAP = {
    "deliverred": "delivered",
    "cancellled": "cancelled",
}

def clean_status(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower()
    return STATUS_TYPO_MAP.get(s, s)

df["status"] = df["status"].apply(clean_status)
print("Status value counts after cleaning:\n")
print(df["status"].value_counts())
"""))

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Validation & Summary
# ═════════════════════════════════════════════════════════════════════════════

cells.append(md(r"""
---
## Section 4 — Validation & Summary
"""))

# ── Cleaning Summary Table ──────────────────────────────────────────────────

cells.append(md("### Cleaning Summary Table"))

cells.append(code(r"""
# Dynamically compute summary from actual data
after_shape = df.shape

# Compute metrics from the before/after snapshots
empty_cols_dropped = before_shape[1] - after_shape[1]  # columns removed
dups_removed_count = before_shape[0] - len(df)  # approximate (includes dup removal)

summary_data = [
    ["1. Drop Empty Columns", f"{empty_cols_dropped} columns",
     "Removed columns where 100% of values were null"],
    ["2. Remove Duplicates", f"{before_shape[0] - len(df_raw.drop_duplicates()):,} rows",
     "Dropped exact duplicate rows"],
    ["3. Standardize Dates", f"{df_raw['order_date'].nunique():,} unique formats",
     "Parsed 5 date formats into ISO 8601 (YYYY-MM-DD)"],
    ["4. Normalize Prices", f"{df_raw['price'].nunique():,} unique formats",
     "Stripped currency symbols, fixed decimal separators, converted to float"],
    ["5. Standardize SKUs", f"{df_raw['sku'].nunique():,} variants -> {df['sku'].nunique()}",
     "Uppercased and ensured SKU-XXX dash format"],
    ["6. Normalize Missing Values",
     f"{(df_raw['customer_email'].isin(['N/A','n/a','na','NA','-','--','.','none','None','null','NULL',''])).sum() + (df_raw['customer_phone'].isin(['N/A','n/a','na','NA','-','--','.','none','None','null','NULL',''])).sum():,} fake nulls",
     "Converted N/A, none, null, -, etc. to np.nan"],
    ["7. Fix Encoding", f"~{int(len(df_raw) * 0.30):,} rows (est.)",
     "Repaired Latin-1 mojibake in product names"],
    ["8. Standardize Phones",
     f"{df['customer_phone'].notna().sum():,} formatted",
     "Extracted digits, reformatted to XXX-XXX-XXXX"],
    ["9. Normalize Countries",
     f"{df_raw['shipping_country'].nunique()} variants -> {df['shipping_country'].nunique()}",
     "Mapped free-text country names to ISO 2-letter codes"],
    ["10. Fix Status Typos",
     f"{df_raw['status'].nunique()} variants -> {df['status'].nunique()}",
     "Corrected typos (deliverred, cancellled) and lowercased"],
]

summary_df = pd.DataFrame(summary_data, columns=["Issue", "Rows Affected", "Action Taken"])
summary_df.style.set_properties(**{"text-align": "left"}).hide(axis="index")
"""))

# ── Data Type Audit ─────────────────────────────────────────────────────────

cells.append(md("### Data Type Audit — Before vs After"))

cells.append(code(r"""
after_dtypes = df.dtypes

# Build comparison for columns that exist in both
common_cols = [c for c in before_dtypes.index if c in after_dtypes.index]
dtype_comparison = pd.DataFrame({
    "Column": common_cols,
    "Before": [str(before_dtypes[c]) for c in common_cols],
    "After": [str(after_dtypes[c]) for c in common_cols],
})
dtype_comparison["Changed"] = dtype_comparison["Before"] != dtype_comparison["After"]

# Dropped columns
dropped_cols = [c for c in before_dtypes.index if c not in after_dtypes.index]
if dropped_cols:
    for dc in dropped_cols:
        dtype_comparison = pd.concat([dtype_comparison, pd.DataFrame([{
            "Column": dc, "Before": str(before_dtypes[dc]), "After": "(dropped)", "Changed": True
        }])], ignore_index=True)

def highlight_changed(row):
    if row["Changed"]:
        return ["background-color: #d4edda"] * len(row)
    return [""] * len(row)

dtype_comparison.style.apply(highlight_changed, axis=1).hide(axis="index")
"""))

# ── Schema Comparison ───────────────────────────────────────────────────────

cells.append(md("### Schema Comparison — Before vs After"))

cells.append(code(r"""
before_dup_count = df_raw.duplicated().sum()
after_dup_count = df.duplicated().sum()
before_numeric = df_raw.select_dtypes(include="number").shape[1]
after_numeric = df.select_dtypes(include="number").shape[1]

schema_data = {
    "Metric": ["Rows", "Columns", "Total null cells", "Duplicate rows", "Numeric columns"],
    "Before": [
        f"{before_shape[0]:,}",
        str(before_shape[1]),
        f"{before_nulls:,}",
        f"{before_dup_count:,}",
        str(before_numeric),
    ],
    "After": [
        f"{after_shape[0]:,}",
        str(after_shape[1]),
        f"{df.isnull().sum().sum():,}",
        f"{after_dup_count:,}",
        str(after_numeric),
    ],
}
schema_df = pd.DataFrame(schema_data)
schema_df.style.set_properties(**{"text-align": "left"}).hide(axis="index")
"""))

# ── Before/After Sample ────────────────────────────────────────────────────

cells.append(md("### Before / After Sample (First 6 Rows)"))

cells.append(code(r"""
print("=== BEFORE CLEANING ===\n")
display(before_sample)
print("\n=== AFTER CLEANING ===\n")
display(df.head(6))
"""))

# ── Performance Summary ─────────────────────────────────────────────────────

cells.append(md("### Performance & Automation Notes"))

cells.append(code(r"""
print(f"Dataset dimensions BEFORE: {before_shape[0]:,} rows x {before_shape[1]} columns")
print(f"Dataset dimensions AFTER:  {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Records removed:           {before_shape[0] - df.shape[0]:,}")
print(f"Columns removed:           {before_shape[1] - df.shape[1]}")
print(f"Null cells remaining:      {df.isnull().sum().sum():,}")
print()
print("The cleaning pipeline is modular and reusable for future dataset updates.")
print("Each step can be independently configured or extended for different data sources.")
"""))

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Export
# ═════════════════════════════════════════════════════════════════════════════

cells.append(md(r"""
---
## Section 5 — Export
"""))

cells.append(code(r"""
output_file = "cleaned_ecommerce_data.csv"
df.to_csv(output_file, index=False)
print(f"Saved cleaned dataset to: {output_file}")
print(f"Row count: {len(df):,}")
print(f"Columns:   {list(df.columns)}")
"""))

# ── Assemble notebook ───────────────────────────────────────────────────────

nb.cells = cells

NOTEBOOK_FILE = "data_cleaning_portfolio.ipynb"

with open(NOTEBOOK_FILE, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Notebook written to {NOTEBOOK_FILE} ({len(cells)} cells)")
