import pandas as pd
import numpy as np

# ==========================================================
# 1. LOAD DATASET FROM CSV FILE
# ==========================================================

# Dataframe
df = pd.read_csv("C:/Users/nanda/OneDrive/Desktop/DW-project/Python project/datasets/retail_store_sales.csv")

df1 = df.copy()

# Initial raw datatset info.
print("=" * 60)
print("INITIAL DATASET OVERVIEW")
print("=" * 60)
print(df1.head())
print(f"\nShape : {df1.shape}")
print("\nData Types")
print("Column" + " "*15 + "Data Type")
print("______" + " "*15 + "_________")
print(df1.dtypes)

# ==========================================================
# 2. COLUMN NAMES STANDARDIZATION
# ==========================================================

# remove trailing whitespaces and convert to snake_case
df1.columns = ( df1.columns
                .str.strip()
                .str.lower()
                .str.replace(r"\s+", "_", regex=True)
)

print("\nColumn Names")
print(df1.columns.tolist())

# ==========================================================
# 3. CHECK DUPLICATES
# ==========================================================

print("\n" + "=" * 60)
print("DUPLICATE CHECKS")
print("=" * 60)

# Check for duplicate transaction IDs
df1["transaction_id"] = df1["transaction_id"].astype("string")

duplicate_ids = df1[df1["transaction_id"].duplicated(keep=False)]

print(f"Duplicate Transaction IDs : {len(duplicate_ids)}")

if not duplicate_ids.empty:
    print(duplicate_ids.head())

# Check for duplicate rows in DataFrame
duplicate_rows = df1[df1.duplicated()]

print(f"Duplicate Rows : {len(duplicate_rows)}")

# ==========================================================
# 4. CLEAN TEXT / CATEGORICAL COLUMNS
# ==========================================================

text_columns = [
                    "category",
                    "item",
                    "payment_method",
                    "location"
]

# Regular expression to clean columns from null or nan and empty string values
null_pattern = r"(?i)^\s*(nan|none|null|na|n/a|-)\s*$"

for col in text_columns:

    if col in df1.columns:
        df1[col] = (
                    df1[col]
                    .replace(null_pattern, np.nan, regex=True)
                    .replace("", np.nan)
                    .str.strip()
                    .str.title()
                    .astype("category")
        )

print("\n---Categorical columns cleaned---")

# ==========================================================
# 5. CLEANING TRANSACTION DATE
# ==========================================================

# Change to datetime format
if "transaction_date" in df1.columns:

    df1["transaction_date"] = pd.to_datetime(
        df1["transaction_date"],
        errors="coerce"
    )

    invalid_dates = df1["transaction_date"].isna().sum()

    print(f"Invalid Dates Converted to NaT : {invalid_dates}")
    df1 = df1.sort_values("transaction_date")  # sorting data in ascending dates

# ==========================================================
# 6. NUMERIC COLUMNS DATA VALIDATION
# ==========================================================

numeric_columns = [
                    "price_per_unit",
                    "quantity",
                    "total_spent"
]

for col in numeric_columns:
    df1[col] = pd.to_numeric(df1[col], errors="coerce")  # converting datatype to numeric

# Check for negative values in numeric columns
sub_head = "---Negative Values---"
print(f"\n{sub_head}\n" + "_"*len(sub_head))

for col in numeric_columns:
    negatives = (df1[col] < 0).sum()
    print(f"{col} : {negatives}")

print("---\nZero Quantities :", (df1["quantity"] == 0).sum())

# ==========================================================
# 7. FILL MISSING PRICE USING ITEM MEDIAN
# ==========================================================

print("\n" + "=" * 60)
print("PRICE IMPUTATION")
print("=" * 60)

missing_before = df1["price_per_unit"].isna().sum()

# A lookup map for item and median price
item_price_lookup = (
        df1.groupby("item", observed= False)["price_per_unit"]
           .median()
)

df1["price_per_unit"] = df1["price_per_unit"].fillna(
    df1["item"].map(item_price_lookup)
)

missing_after = df1["price_per_unit"].isna().sum()

print(f"Missing Before : {missing_before}")
print(f"Missing After Median Mapping : {missing_after}")

if missing_after > 0:
    print("\nCALCULATE REMAINING MISSING PRICES\n...\n")

    # ==========================================================
    # 8. CALCULATE REMAINING MISSING PRICES
    # ==========================================================

    # After mapping back available prices, calculate remaining cells with quantity and total_spent
    # Filter for missing prices that have valid quantity and spend data

    mask = (
        df1["price_per_unit"].isna()
        & df1["quantity"].notna()
        & df1["total_spent"].notna()
        & (df1["quantity"] > 0)
        & (df1["total_spent"] >= 0)
    )

    # Compute price by dividing total_spent by quantity only for the masked rows
    df1.loc[mask, "price_per_unit"] = (
        df1.loc[mask, "total_spent"]/
        df1.loc[mask, "quantity"]
    )

    print(
        "Remaining Missing Prices :",
        df1["price_per_unit"].isna().sum()
    )

# ==========================================================
# 9. SAFE ITEM IMPUTATION - FILLING MISSING ITEMS
# ==========================================================

# Fill missing items by cross-checking category and price
print("\n" + "=" * 60)
print("ITEM IMPUTATION")
print("=" * 60)


# lookup using category and price
item_lookup = (
    df1.dropna(subset=["item"])
    .drop_duplicates(subset=["category", "price_per_unit"])
    .set_index(["category", "price_per_unit"])["item"]
)

missing_items_before = df1["item"].isna().sum()

item_mask = (
    df1["item"].isna()
    & df1["category"].notna()
    & df1["price_per_unit"].notna()
)

# Fill missing items with mask and item_lookup
df1.loc[item_mask, "item"] = (
    df1.loc[item_mask, ["category", "price_per_unit"]]
    .apply(tuple, axis = 1)
    .map(item_lookup)
)

missing_items_after = df1["item"].isna().sum()

print(f"Missing Items Before : {missing_items_before}")
print(f"Missing Items After  : {missing_items_after}")


# ==========================================================
# 10. ERROR LOG
# ==========================================================

# Isolating unrecoverable records lacking primary analytical value
error_log_df = df1[
    df1[["quantity","total_spent"]].isna().all(axis=1)
].copy()

print("\nRows saved to Error Log :", len(error_log_df))

# ==========================================================
# 11. REMOVE INVALID TRANSACTIONS
# ==========================================================

print("\n" + "=" * 60)
print("REMOVING INVALID TRANSACTIONS")
print("=" * 60)

rows_before = len(df1)

df1 = df1.dropna(
    subset=["quantity", "total_spent"],
    how="all"
)

rows_after = len(df1)

print(f"Rows Before : {rows_before}")
print(f"Rows After  : {rows_after}")
print(f"Rows Removed: {rows_before - rows_after}")

# ==========================================================
# 12. TOTAL SPENT VALIDATION
# ==========================================================

print("\n" + "=" * 60)
print("VALIDATING TOTAL SPENT")
print("=" * 60)

expected_total = (
    df1["quantity"] * df1["price_per_unit"]
)

# Boolean mask satisfying both conditions
mask_valid = (
    expected_total.notna()
    &
    df1["total_spent"].notna()
)

# Stores incorrect totals as boolean flags
incorrect_total = (
    abs( expected_total - df1["total_spent"] ) > 0.01
)

# Check for mathematical correctness
incorrect_total &= mask_valid
print(
    "\n"
)

print(
    "Transactions with Incorrect Total :",
    incorrect_total.sum()
)

# ==========================================================
# 13. CORRECT INCORRECT TOTALS
# ==========================================================

print("\n" + "=" * 60)
print("CORRECT INCORRECT TOTALS")
print("=" * 60)

df1.loc[
    incorrect_total,
    "total_spent"
] = expected_total[incorrect_total]

print(
    "\n"
)

print(
    "___Incorrect totals corrected___"
)

# ==========================================================
# 14. FILL REMAINING CATEGORICAL COLUMN VALUES
# ==========================================================

print("\n" + "=" * 60)
print("FILL REMAINING CATEGORICAL COLUMN VALUES")
print("=" * 60)

# Handling missing values in categorical fields by expanding the allowed categories
df1["payment_method"] = (
    df1["payment_method"]
        .cat.add_categories("Unknown")
        .fillna("Unknown")
)

df1["location"] = (
    df1["location"]
        .cat.add_categories("Unknown")
        .fillna("Unknown")
)

print(
    "\n"
)

print(
    "---Remaining categorical columns are filled safely___"
)

# ==========================================================
# 15. CLEAN BOOLEAN COLUMN
# ==========================================================

print("\n" + "=" * 60)
print("CLEAN BOOLEAN COLUMN")
print("=" * 60)

# -- discount_applied column
print("\nCleaning Boolean Column...")

bool_map = {
    "true": True,
    "false": False,
    "yes": True,
    "no": False,
    "1": True,
    "0": False
}

# Handles irregular text and missing values at the same type
df1["discount_applied"] = (
    df1["discount_applied"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(bool_map)
     == True
)

print(
    df1["discount_applied"].value_counts(dropna=False)
)

# ==========================================================
# 16. FINAL DATA VALIDATION
# ==========================================================

print("\n" + "=" * 60)
print("FINAL DATA VALIDATION")
print("=" * 60)

print("\n___Missing Values___")

print(df1.isna().sum())

print("\n___Negative Values___")

for col in [
    "price_per_unit",
    "quantity",
    "total_spent"
]:

    print(
        f"{col}:", (df1[col] < 0).sum()
    )

print(
    "\nZero Quantity :", (df1["quantity"] == 0).sum()
)

print(
    "Duplicate Transaction IDs :",
    df1["transaction_id"].duplicated().sum()
)

print(
    "Duplicate Rows :",
    df1.duplicated().sum()
)

# ==========================================================
# 17. CATEGORY VALIDATION
# ==========================================================

print("\n" + "=" * 60)
print("UNIQUE CATEGORY VALUES")
print("=" * 60)

for col in [
    "category",
    "payment_method",
    "location"
]:
    print(f"\n{col.upper()}")

    print(
        sorted(
            df1[col]
            .dropna()
            .unique()
            .tolist()
        )
    )

# ==========================================================
# 18. DATA QUALITY SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("DATA QUALITY SUMMARY")
print("=" * 60)

summary = pd.DataFrame({
    "Metric":[
        "Original Rows",
        "Clean Rows",
        "Rows Removed",
        "Duplicate IDs",
        "Duplicate Rows",
        "Missing Prices",
        "Missing Items",
        "Invalid Dates"
    ],

    "Value":[
        len(df),
        len(df1),
        len(df)-len(df1),
        df1["transaction_id"].duplicated().sum(),
        df1.duplicated().sum(),
        df1["price_per_unit"].isna().sum(),
        df1["item"].isna().sum(),
        df1["transaction_date"].isna().sum()
    ]
})

print(summary)

# ==========================================================
# 19. EXPORT FILES
# ==========================================================

df1.to_csv(
    "retail_store_sales_clean.csv",
    index=False
)

error_log_df.to_csv(
    "retail_store_sales_error_log.csv",
    index=False
)

print("\nClean dataset exported successfully.")
print("Error log exported successfully.")

# ==========================================================
# 20. CLEAN DATA PREVIEW
# ==========================================================

print("\n" + "=" * 60)
print("FINAL CLEAN DATA")
print("=" * 60)

print(df1.head())

print("\nFinal Shape :", df1.shape)

print("\nData Types")

print(df1.dtypes)

