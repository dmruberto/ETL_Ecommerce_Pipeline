import pandas as pd
import os
import logging

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), "../outputs/logs/transform_data.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to the original Excel file
file_path = os.path.join(os.path.dirname(__file__), "../data/raw/online_retail_II.xlsx")

# Read data from the specific sheet
logging.info("Reading data from Excel...")
df = pd.read_excel(file_path, sheet_name="Year 2009-2010")

# Remove all spaces from column names
df.columns = df.columns.str.replace(" ", "")

# Filter records with non-numeric 6-digit Invoice
df = df[df["Invoice"].astype(str).str.match(r"^\d{6}$")]

# Remove records with nulls in key columns
df = df.dropna(subset=["Invoice", "Description", "CustomerID", "Country"])

# Standardize the Description column to uppercase
df["Description"] = df["Description"].str.upper()

# Validate and remove invalid or negative values in Quantity
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df = df[df["Quantity"] > 0]

# Validate and remove invalid prices (non-numeric, zero or negative)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df = df[df["Price"] > 0]

# Validate that CustomerID contains only valid numeric values
df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
df = df.dropna(subset=["CustomerID"])

# Remove duplicates
df = df.drop_duplicates()

# Create 'ProductCategory' column with the value 'Other'
df["ProductCategory"] = "Other"

# Create 'TotalPrice' column
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Create Year-Month column for grouping
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()

# KPI: Revenue per customer (by CustomerID)
revenue_per_customer = df.groupby("CustomerID")["TotalPrice"].sum()

# KPI: Average ticket (average TotalPrice per transaction)
average_ticket = df["TotalPrice"].mean()

# Extended dictionary (you can edit it as needed)
keywords = {
    # Season
    "CHRISTMAS": "Seasonal",
    "EASTER": "Seasonal",
    "VALENTINE": "Seasonal",
    "HALLOWEEN": "Seasonal",

    # Gift
    "TRINKET": "Gift",
    "PRESENT": "Gift",
    "GIFT": "Gift",
    "JUMPER": "Gift",
    "HEART": "Gift",

    # Home
    "FRAME": "Home",
    "CUSHION": "Home",
    "LAMP": "Home",
    "MUG": "Home",
    "PLATE": "Home",
    "BOWL": "Home",

    # Decoration
    "BOX": "Decoration",
    "SIGN": "Decoration",
    "POSTER": "Decoration",
    "GARLAND": "Decoration",
    "ORNAMENT": "Decoration",

    # Kitchen
    "TEA": "Kitchen",
    "CUP": "Kitchen",
    "COASTER": "Kitchen",
    "NAPKIN": "Kitchen",

    # Office / Stationery
    "PEN": "Stationery",
    "PENCIL": "Stationery",
    "NOTEBOOK": "Stationery",
    "CARD": "Stationery",
    "STICKER": "Stationery",

    # Scents
    "CANDLE": "Candles & Scents",
    "SCENT": "Candles & Scents",

    # Kids
    "TOY": "Kids",
    "GAME": "Kids",

    # Organization
    "BASKET": "Storage",
    "TOTE": "Storage"
}

# Function to assign category based on keywords if it's 'Other'
def classify_product(row):
    if row["ProductCategory"] != "Other":
        return row["ProductCategory"]
    description_upper = row["Description"].upper()
    for keyword, category in keywords.items():
        if keyword in description_upper:
            return category
    return "Other"

# Apply the function
df["ProductCategory"] = df.apply(classify_product, axis=1)

# Validation: ensure 'InvoiceDate' is of type datetime
assert df['InvoiceDate'].dtype == 'datetime64[ns]', "InvoiceDate was not properly converted."

# Validation: ensure there are no negative values in TotalPrice
assert df['TotalPrice'].min() >= 0, "There are negative values in TotalPrice"

# Save the cleaned file
output_path = os.path.join(os.path.dirname(__file__), "../data/processed/cleaned_sales.csv")
df.to_csv(output_path, index=False, encoding="utf-8", lineterminator="\n")

# Log information about the saved cleaned dataset
logging.info("✅ Clean dataset saved at: %s", output_path)

# 7. Run as a standalone module
if __name__ == "__main__":
    print("✅ Clean dataset saved at:", output_path)
    print("🔍 First rows of the clean dataset:")
    print(df.head())

    # Display KPIs
    print("\n📊 KPI - Revenue per customer:")
    print(revenue_per_customer.head())
    print("\n📊 KPI - Average ticket:", average_ticket)
    
    # Log the KPIs
    logging.info("📊 KPI - Revenue per customer:\n%s", revenue_per_customer.head())
    logging.info("📊 KPI - Average ticket: %s", average_ticket)
