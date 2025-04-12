import os
import pandas as pd
import logging

# Set up logging configuration
log_file_path = os.path.join(os.path.dirname(__file__), "../outputs/logs/extract_data.log")
logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,  # Log level to capture info, warning, and error messages
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Excel file (relative to this script)
file_path = os.path.join(os.path.dirname(__file__), "../data/raw/online_retail_II.xlsx")

# Log the start of the process
logging.info("Starting the data extraction process.")

try:
    # Read Excel file
    logging.info("Reading the Excel file from: %s", file_path)
    df = pd.read_excel(file_path, sheet_name="Year 2009-2010")

    # Validation: ensure the data is not empty
    if df.empty:
        logging.error("The input file is empty!")
        raise ValueError("The input file is empty!")

    # Log successful data load
    logging.info("File loaded successfully. The dataset contains %d rows and %d columns.", len(df), len(df.columns))
    
    # Display the first few rows of the dataset
    print("✅ Reading data from Excel...")
    print("📄 File loaded:", file_path)
    print("📊 First rows of the dataset:")
    print(df.head())

except Exception as e:
    logging.error("An error occurred while extracting data: %s", e)
    print(f"❌ Error occurred: {e}")