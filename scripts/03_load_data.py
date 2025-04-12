import pandas as pd
import os
from sqlalchemy import create_engine
import logging

# Set up logging
log_file_path = os.path.join(os.path.dirname(__file__), "../outputs/logs/load_data.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to the clean CSV file
output_path = os.path.join(os.path.dirname(__file__), "../data/processed/cleaned_sales.csv")

# Read CSV file
try:
    df = pd.read_csv(output_path)
    logging.info("✅ Dataset successfully loaded from CSV.")
except FileNotFoundError:
    logging.error("⚠️ The CSV file was not found at the specified path.")
    raise

# Remove invisible spaces in column names
df.columns = df.columns.str.strip()

# Validation: ensure the file was saved correctly
assert os.path.exists(output_path), "The file was not saved correctly."

# Confirm final column names
logging.info("🧾 Final column names: %s", list(df.columns))

# Create the connection to the MySQL database using SQLAlchemy
user = 'root'
password = '123456789'
host = 'localhost'
database = 'ecommerce_data'

# MySQL connection URL
try:
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
    # Check if connection is successful
    with engine.connect() as conn:
        logging.info("✅ Successfully connected to MySQL.")
except Exception as e:
    logging.error(f"⚠️ Failed to connect to the MySQL database: {e}")
    raise

# Load the dataframe into MySQL
try:
    df.to_sql('cleaned_sales', con=engine, if_exists='replace', index=False)
    logging.info("✅ Data loaded into MySQL.")
except Exception as e:
    logging.error(f"⚠️ Error loading data into MySQL: {e}")
    raise

# Show number of records and first rows (nicely aligned)
logging.info("📊 Number of records: %d", len(df))
logging.info("🔍 First rows of the dataset:\n%s", df.head().to_string(index=False))

# 7. Run as a standalone module
if __name__ == "__main__":
    print("📊 Number of records:", len(df))
    print("\n🔍 First rows (properly aligned):")
    print(df.head().to_string(index=False))
