# Importing necessary modules
import os                      # For handling file paths
import subprocess              # For running external Python scripts

# This function is responsible for running a given script and showing status messages
def run_script(script_name):
    print(f"\nRunning {script_name}...")  # Informational message
    script_path = os.path.join("scripts", script_name)  # Full path of the script inside the 'scripts' folder

    try:
        # Running the script with Python. If something goes wrong, it raises an exception.
        subprocess.run(["python", script_path], check=True)
        print(f"{script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        # If an error occurs during execution, print an error message
        print(f"Error running {script_name}: {e}")

# Main function of the program that orchestrates the entire ETL pipeline
def main():
    print("🚀 Starting the Ecommerce ETL Pipeline...")

    # List of scripts to execute in order (Extract -> Transform -> Load)
    scripts = [
        "01_extract_data.py",
        "02_transform_data.py",
        "03_load_data.py"
    ]

    # Loop through the list and run each script with the previously defined function
    for script in scripts:
        run_script(script)

    print("\n✅ The ETL Pipeline completed successfully.")

# Entry point of the script: if this file is run directly, execute the main() function
if __name__ == "__main__":
    main()
