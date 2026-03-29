# Design: Large-Scale E-commerce Data Cleaning & Standardization (125K Rows)

**Date:** 2026-02-23
**Purpose:** Upwork portfolio demo — prove ability to clean large, messy datasets.

## Goal

Create a convincing portfolio piece that demonstrates data cleaning expertise on a 125K-row simulated Shopify export. The deliverable is a visual PDF case study (5–7 pages) backed by a reproducible Jupyter Notebook.

## Project Structure

```
demo_1/
├── generate_messy_data.py              # LOCAL ONLY — not included in portfolio
├── messy_ecommerce_export.csv          # Generated 125K+ row messy dataset
├── data_cleaning_portfolio.ipynb       # Technical reference notebook
├── cleaned_ecommerce_data.csv          # Cleaned output
├── case_study.html                     # Visual case study → browser Print to PDF
```

## Dataset Design

~125,000 rows (120K base + ~5K injected duplicates). 12 columns including 3 empty ones.

### Columns and Messy Patterns

| Column | Messy Patterns |
|--------|---------------|
| `order_id` | Incrementing IDs (ORD-10001...) |
| `sku` | Inconsistent casing: `SKU-001`, `sku-001`, `Sku-001` |
| `product_name` | Encoding corruption: `Ã¼` instead of `ü`, `Ã¶` instead of `ö`. Trailing whitespace. |
| `order_date` | 5 formats: `01/02/2024`, `2024-02-01`, `02-01-2024`, `Feb 1, 2024`, `1.02.2024` |
| `price` | `$19.99`, `19.99`, `€19,99`, `USD 19.99`, `19.99 TL` |
| `quantity` | Mixed types: string `"3"`, int `3`, float `3.0` |
| `customer_email` | `None`, `N/A`, `n/a`, `-`, `""`, valid emails |
| `customer_phone` | `+1-555-0123`, `5550123`, `(555) 012-3456`, `555.012.3456` |
| `shipping_country` | `US`, `USA`, `United States`, `us` |
| `status` | `shipped`, `Shipped`, `SHIPPED`, `deliverred` (typo) |
| `_unnamed_1`, `_unnamed_2`, `notes` | Completely empty columns |

Plus ~5,000 exact duplicate rows injected.

## Notebook Flow

### Section 1 — Introduction
- Problem statement
- Dataset description: "Simulated large-scale e-commerce export for demonstration purposes."

### Section 2 — Initial Exploration
- `df.shape`, `df.dtypes`, `df.head(10)`, `df.describe()`
- `df.isnull().sum()` summary
- `df.duplicated().sum()`
- "Before" snapshot

### Section 3 — Cleaning Pipeline (each step = separate cell with `%%time`)
1. Drop empty columns (`_unnamed_1`, `_unnamed_2`, `notes`)
2. Remove exact duplicate rows
3. Standardize dates to ISO 8601 (`YYYY-MM-DD`)
4. Normalize prices to float (strip currency symbols and format differences)
5. Clean SKU casing (all → `SKU-XXX`)
6. Handle missing values (email/phone: coerce nulls from `N/A`, `n/a`, `-`, `""`)
7. Fix encoding issues in product names (Latin-1 artifacts → UTF-8)
8. Standardize phone formats
9. Normalize country names → ISO country codes
10. Fix status typos and casing

### Section 4 — Validation & Summary
- **Cleaning Summary Table** (dynamically computed):
  | Issue | Rows Affected | Action Taken |
  |-------|--------------|--------------|
  | Duplicate rows | 5,214 | Removed |
  | Mixed date formats | 125,000 | Standardized to ISO |
  | Currency formatting | 118,230 | Converted to float |
  | ... | ... | ... |
- **Data Type Audit**: before/after dtype comparison table
- **Schema Comparison**: column names, types, null rates — before vs after
- **Processing Time**: total pipeline execution time
- **Automation note**: "The cleaning pipeline is modular and reusable for future dataset updates."

### Section 5 — Export
- Save to `cleaned_ecommerce_data.csv`

## PDF Case Study (case_study.html)

5–7 page visual document. No code. Results and tables only.

| Page | Content |
|------|---------|
| 1 | Title + problem statement + "125K rows, 12 columns, 8 data quality issues" |
| 2 | Before snapshot — messy data sample table (5–6 rows) + issue list |
| 3 | Cleaning Summary Table (Issue / Rows Affected / Action Taken) |
| 4 | After snapshot — cleaned data sample + schema comparison |
| 5 | Validation results + data type audit |
| 6 | Performance metric + automation note + tech stack |
| 7 | Disclaimer: "Simulated large-scale e-commerce export for demonstration purposes." |

Generated as HTML, converted to PDF via browser Print > Save as PDF.

## Key Strategic Decisions

1. `generate_messy_data.py` is NOT included in portfolio — prevents "this isn't real data" perception
2. Title is "Large-Scale E-commerce Data Cleaning & Standardization (125K Rows)" — not just "data cleaning"
3. Processing time is displayed prominently — signals performance awareness
4. Cleaning summary table is the centerpiece — this is what converts clients
5. All notebook text is in English — international Upwork audience
