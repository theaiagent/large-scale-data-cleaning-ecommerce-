# Large-Scale E-commerce Data Cleaning & Standardization

**125,000 rows | 8 data quality issues | Fully automated pipeline**

An end-to-end data cleaning solution that transforms a messy, real-world-style e-commerce export into analysis-ready data — in under 30 seconds.

---

## Problem

A Shopify-style e-commerce export with **125K rows** arrives riddled with quality issues that block reporting and analytics:

| Issue | Scale |
|-------|-------|
| Duplicate records | 5,000 rows |
| Mixed date formats (5 variants) | 99,933 rows |
| Currency symbols & locale formats ($, EUR, TL) | 74,901 rows |
| UTF-8 encoding corruption (mojibake) | 37,978 rows |
| Inconsistent country names | 73,483 rows |
| Status field typos & casing | 62,294 rows |
| SKU casing inconsistencies | 31,147 rows |
| Placeholder nulls (N/A, -, empty strings) | multiple columns |

Manual cleaning would take **days**. Errors would be inevitable.

## Solution

A **10-step Python pipeline** that handles everything automatically:

```
Dates        → ISO 8601 (YYYY-MM-DD)
Prices       → Clean float (strips $, EUR, TL, fixes comma decimals)
SKUs         → Uppercase SKU-XXX
Countries    → ISO alpha-2 codes
Phone numbers → XXX-XXX-XXXX
Encoding     → Latin-1 artifacts repaired to UTF-8
Nulls        → Fake values (N/A, -, "") coerced to proper NaN
Statuses     → Typos fixed, casing standardized
Duplicates   → Removed
Empty columns → Dropped
```

## Result

| Metric | Before | After |
|--------|--------|-------|
| Rows | 125,000 | 120,000 |
| Columns | 13 | 10 |
| Duplicates | 5,000 | 0 |
| Date formats | 5 | 1 |
| Currency formats | 5 | 1 |
| Encoding errors | 37,978 | 0 |
| Null representations | 4+ variants | Standard NaN |

**Processing time: ~15 seconds** on a standard machine.

---

## Quick Start

```bash
pip install pandas numpy jupyter nbformat nbconvert

# 1 — Generate the messy dataset
python generate_messy_data.py

# 2 — Build and execute the cleaning notebook
python build_notebook.py
jupyter nbconvert --to notebook --execute data_cleaning_portfolio.ipynb \
  --output data_cleaning_portfolio.ipynb --ExecutePreprocessor.timeout=300
```

## Project Structure

```
├── data_cleaning_portfolio.ipynb  # Full pipeline with outputs (start here)
├── messy_ecommerce_export.csv     # Raw dataset (125K rows)
├── generate_messy_data.py         # Synthetic data generator
├── build_notebook.py              # Notebook builder (nbformat)
├── build_case_study.py            # HTML/PDF case study generator
└── case_study.html                # Visual case study
```

## Tech Stack

Python 3 | Pandas | NumPy | nbformat

---

## Screenshots

> *Visual walkthrough of the cleaning pipeline and results.*

| | |
|---|---|
| **Before: Raw Data Sample** | **After: Cleaned Output** |
| ![Before](screenshots/before_raw_data.png) | ![After](screenshots/after_cleaned_data.png) |
| **Cleaning Summary** | **Schema Comparison** |
| ![Summary](screenshots/cleaning_summary.png) | ![Schema](screenshots/schema_comparison.png) |

<!--
  HOW TO ADD SCREENSHOTS:
  1. Create a "screenshots" folder in this repo
  2. Take screenshots from the notebook or case study PDF
  3. Recommended screenshots:
     - before_raw_data.png      → first few rows of messy data
     - after_cleaned_data.png   → first few rows of cleaned data
     - cleaning_summary.png     → the cleaning summary table
     - schema_comparison.png    → before/after schema comparison
  4. Push the screenshots folder to GitHub
-->

---

*Synthetic e-commerce dataset for demonstration purposes. All data is programmatically generated.*
