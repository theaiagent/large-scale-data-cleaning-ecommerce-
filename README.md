# Large-Scale E-commerce Data Cleaning & Standardization

End-to-end data cleaning pipeline for a **125,000-row** simulated e-commerce dataset with **8 distinct data quality issues**.

## The Problem

E-commerce data exports often arrive with:

| Issue | Rows Affected |
|-------|--------------|
| Duplicate records | ~5,000 |
| Mixed date formats (5 variants) | 99,933 |
| Currency symbols in prices ($, EUR, TL) | 74,901 |
| UTF-8 encoding corruption (mojibake) | 37,978 |
| SKU casing inconsistencies | 31,147 |
| Inconsistent country names | 73,483 |
| Status field typos & casing | 62,294 |
| Placeholder strings as nulls (N/A, -, "") | multiple columns |

## The Solution

A reproducible Python pipeline that:

1. **Drops** 3 empty columns
2. **Removes** 5,000 duplicate rows
3. **Standardizes** dates to ISO 8601 (`YYYY-MM-DD`)
4. **Normalizes** prices to float (strips `$`, `EUR`, `TL`, fixes comma decimals)
5. **Cleans** SKU format to `SKU-XXX`
6. **Coerces** fake null values (`N/A`, `n/a`, `-`, `""`) to proper `NaN`
7. **Repairs** encoding corruption (Latin-1 artifacts to UTF-8)
8. **Standardizes** phone numbers to `XXX-XXX-XXXX`
9. **Maps** country names to ISO alpha-2 codes
10. **Fixes** status typos and casing

**Result:** 120,000 clean rows, 10 columns, zero duplicates, consistent formats.

## Project Structure

```
.
├── generate_messy_data.py           # Generates the synthetic messy dataset
├── build_notebook.py                # Builds the Jupyter notebook programmatically
├── data_cleaning_portfolio.ipynb    # Full cleaning pipeline with outputs
├── build_case_study.py              # Generates the HTML case study
├── case_study.html                  # Visual case study (print to PDF)
└── docs/plans/                      # Design & implementation docs
```

## Quick Start

```bash
# 1. Generate the messy dataset
python generate_messy_data.py

# 2. Build and execute the notebook
python build_notebook.py
jupyter nbconvert --to notebook --execute data_cleaning_portfolio.ipynb \
  --output data_cleaning_portfolio.ipynb --ExecutePreprocessor.timeout=300

# 3. Generate the case study
python build_case_study.py
# Open case_study.html in browser → Print → Save as PDF
```

## Requirements

- Python 3.10+
- pandas
- numpy
- jupyter / nbformat / nbconvert

```bash
pip install pandas numpy jupyter nbformat nbconvert
```

## Dataset Details

The synthetic dataset simulates a Shopify e-commerce export with realistic messy patterns:

- **120,000 base rows** + **5,000 injected duplicates** = 125,000 total
- **13 columns** including 3 intentionally empty ones
- **10 product names** with Turkish/German characters (Grüner Tee, Türkçe Klavye Seti)
- **5 date formats:** `MM/DD/YYYY`, `YYYY-MM-DD`, `DD-MM-YYYY`, `Mon DD, YYYY`, `DD.MM.YYYY`
- **5 currency formats:** `$19.99`, `19.99`, `EUR19,99`, `USD 19.99`, `19.99 TL`
- Deterministic output via `random.seed(42)` and `np.random.seed(42)`

## Tech Stack

Python 3 | Pandas | NumPy | nbformat | Jinja2

---

*Simulated large-scale e-commerce export for demonstration purposes. All data is synthetically generated.*
