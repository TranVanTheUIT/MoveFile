# CSV Processing Script for Email Data

I'll create a Python script that processes your CSV file, extracts the required columns, and formats the output as requested, with special handling for the empty Recovery Email field.

## Features
- Extracts Email Address, Password, and Recovery Email from CSV
- Only includes the second delimiter ("|") for Recovery Email if it contains data
- Splits data into multiple files with customizable number of rows
- Default output is 1000 rows per file
- Saves output files in a "processed" directory


Data directory will be like this: the data file will placed in data/origin folder
├───data
│   └───origin
├───output
└───processed

## How to Use

1. Save the script as `process_csv.py`

2. Run with default settings (1000 rows per file):
   ```bash
   python process_csv.py
   ```

3. Or specify parameters:
   ```bash
   python process_csv.py path/to/your/file.csv --output-dir processed --rows 500
   ```

## Example Output

The script will create files like processed_001.txt in the specified output directory.

Each line in the output files will be formatted as:
- With recovery email: `email|password|recovery_email`
- Without recovery email: `email|password` (no trailing separator)

The script provides progress updates as it processes the data and handles potential errors like missing columns in the CSV.