"""
generate_messy_data.py
Generates a ~125,000-row messy CSV simulating a Shopify e-commerce export.
Used for Upwork portfolio demo — LOCAL ONLY, not shown to clients.
"""

import random
import numpy as np
import pandas as pd

# ── reproducibility ──────────────────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

NUM_BASE_ROWS = 120_000
NUM_DUPLICATE_ROWS = 5_000
OUTPUT_FILE = "messy_ecommerce_export.csv"

# ── reference pools ──────────────────────────────────────────────────────────

BASE_SKUS = [
    "SKU-001", "SKU-002", "SKU-003", "SKU-004", "SKU-005",
    "SKU-006", "SKU-007", "SKU-008", "SKU-009", "SKU-010",
]

PRODUCT_NAMES = [
    "Grüner Tee",
    "Türkçe Klavye Seti",
    "Ölçü Aleti Premium",
    "Café Blend Dark Roast",
    "Naïve Art Print Set",
    "Résumé Template Pro",
    "Crème Brûlée Torch Kit",
    "Piñata Party Pack",
    "Über Comfort Pillow",
    "El Niño Weather Station",
]

DATE_FORMATS = [
    "%m/%d/%Y",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%b %d, %Y",
    "%d.%m.%Y",
]

PRICE_FORMATS = [
    lambda v: f"${v:.2f}",
    lambda v: f"{v:.2f}",
    lambda v: f"€{v:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","),  # €19,99
    lambda v: f"USD {v:.2f}",
    lambda v: f"{v:.2f} TL",
]

CUSTOMER_EMAILS = [
    "alice.johnson@gmail.com",
    "bob.smith@yahoo.com",
    "carol.white@outlook.com",
    "dave.brown@hotmail.com",
    "eve.davis@protonmail.com",
    "frank.miller@icloud.com",
    "grace.wilson@aol.com",
    "hank.moore@mail.com",
]

NULL_EMAIL_VARIANTS = [None, "N/A", "n/a", "-", ""]

PHONE_FORMATS = [
    lambda: f"+1-555-{random.randint(1000,9999)}",
    lambda: f"555{random.randint(1000,9999)}",
    lambda: f"(555) {random.randint(100,999)}-{random.randint(1000,9999)}",
    lambda: f"555.{random.randint(100,999)}.{random.randint(1000,9999)}",
]

NULL_PHONE_VARIANTS = [None, "N/A", ""]

SHIPPING_COUNTRIES = [
    "US", "USA", "United States", "us",
    "CA", "Canada", "canada",
    "GB", "UK", "United Kingdom",
    "DE", "Germany", "germany",
    "FR", "France",
    "AU", "Australia",
]

STATUS_VARIANTS = [
    "shipped", "Shipped", "SHIPPED",
    "delivered", "Delivered", "deliverred",
    "processing", "Processing",
    "cancelled", "Cancellled",
    "pending", "Pending",
]


# ── helper functions ─────────────────────────────────────────────────────────

def messy_sku(base_sku: str) -> str:
    """Apply random casing/formatting to a SKU."""
    choice = random.randint(0, 3)
    if choice == 0:
        return base_sku              # original: SKU-001
    elif choice == 1:
        return base_sku.lower()      # sku-001
    elif choice == 2:
        return base_sku.capitalize() # Sku-001
    else:
        return base_sku.replace("-", "")  # SKU001


def messy_product_name(name: str) -> str:
    """Corrupt encoding ~30%, add trailing whitespace ~20%."""
    result = name
    if random.random() < 0.30:
        # encode as UTF-8 then decode as Latin-1 → mojibake
        try:
            result = name.encode("utf-8").decode("latin-1")
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    if random.random() < 0.20:
        result = result + "   "
    return result


def messy_date(dt) -> str:
    """Format a datetime with a randomly chosen format."""
    fmt = random.choice(DATE_FORMATS)
    return dt.strftime(fmt)


def messy_price(value: float) -> str:
    """Format a price with random currency/locale style."""
    formatter = random.choice(PRICE_FORMATS)
    return formatter(value)


def messy_quantity(qty: int):
    """Return quantity as str, int, or float randomly."""
    choice = random.randint(0, 2)
    if choice == 0:
        return str(qty)
    elif choice == 1:
        return qty
    else:
        return float(qty)


def messy_email() -> str:
    """Pick a real email ~70% of the time, null variant ~30%."""
    if random.random() < 0.70:
        return random.choice(CUSTOMER_EMAILS)
    else:
        return random.choice(NULL_EMAIL_VARIANTS)


def messy_phone():
    """Pick a formatted phone ~65% of the time, null variant ~35%."""
    if random.random() < 0.65:
        formatter = random.choice(PHONE_FORMATS)
        return formatter()
    else:
        return random.choice(NULL_PHONE_VARIANTS)


# ── main generation ──────────────────────────────────────────────────────────

def generate_dataset() -> pd.DataFrame:
    print("Generating base rows...")

    # pre-generate random dates
    start = pd.Timestamp("2023-01-01")
    end = pd.Timestamp("2024-12-31")
    date_range_seconds = int((end - start).total_seconds())
    random_offsets = np.random.randint(0, date_range_seconds, size=NUM_BASE_ROWS)
    random_dates = [start + pd.Timedelta(seconds=int(s)) for s in random_offsets]

    # pre-generate random prices
    random_prices = np.random.uniform(4.99, 299.99, size=NUM_BASE_ROWS)

    # pre-generate random quantities
    random_quantities = np.random.randint(1, 21, size=NUM_BASE_ROWS)

    rows = []
    for i in range(NUM_BASE_ROWS):
        base_sku = random.choice(BASE_SKUS)
        base_name = PRODUCT_NAMES[BASE_SKUS.index(base_sku)]

        row = {
            "order_id": f"ORD-{10001 + i}",
            "sku": messy_sku(base_sku),
            "product_name": messy_product_name(base_name),
            "order_date": messy_date(random_dates[i]),
            "price": messy_price(random_prices[i]),
            "quantity": messy_quantity(int(random_quantities[i])),
            "customer_email": messy_email(),
            "customer_phone": messy_phone(),
            "shipping_country": random.choice(SHIPPING_COUNTRIES),
            "status": random.choice(STATUS_VARIANTS),
            "_unnamed_1": None,
            "_unnamed_2": None,
            "notes": None,
        }
        rows.append(row)

        if (i + 1) % 30_000 == 0:
            print(f"  ...generated {i + 1:,} rows")

    df = pd.DataFrame(rows)

    # ── inject duplicate rows ────────────────────────────────────────────────
    print(f"Injecting {NUM_DUPLICATE_ROWS:,} duplicate rows...")
    duplicates = df.sample(n=NUM_DUPLICATE_ROWS, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    # ── shuffle ──────────────────────────────────────────────────────────────
    print("Shuffling...")
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


# ── entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = generate_dataset()

    # save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved to {OUTPUT_FILE}")

    # summary
    mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"Row count:    {len(df):,}")
    print(f"Column count: {len(df.columns)}")
    print(f"Memory usage: ~{mem_mb:.1f} MB")
