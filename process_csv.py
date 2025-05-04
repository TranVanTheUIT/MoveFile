import csv
import os
import argparse
import sys

def process_csv(input_file, output_dir, rows_per_file=1000):
    """
    Process a CSV file, extract specific columns, and split into multiple text files.
    
    Args:
        input_file: Path to the input CSV file
        output_dir: Directory where output files will be stored
        rows_per_file: Number of rows per output file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Rows per file: {rows_per_file}")
    
    # Open and process the CSV file
    with open(input_file, 'r', encoding='utf-8') as file:
        # Skip comment lines if any
        header_line = None
        for line in file:
            if not line.strip().startswith('//'):
                header_line = line
                break
        
        if header_line is None:
            print("Error: No header line found in CSV file.")
            return
        
        # Parse header to find column indices
        reader = csv.reader([header_line])
        headers = next(reader)
        try:
            email_index = headers.index("Email Address [Required]")
            password_index = headers.index("Password [Required]")
            recovery_email_index = headers.index("Recovery Email")
        except ValueError as e:
            print(f"Error finding columns in CSV header: {e}")
            return
        
        # Create a CSV reader for the rest of the file
        csv_reader = csv.reader(file)
        
        # Process data
        file_counter = 1
        row_counter = 0
        output_file = None
        total_rows = 0
        
        for row in csv_reader:
            # Skip rows that don't have enough columns
            if len(row) <= max(email_index, password_index):
                continue
            
            # Extract data from row
            email = row[email_index]
            password = row[password_index]
            recovery_email = row[recovery_email_index] if recovery_email_index < len(row) and row[recovery_email_index] else ""
            
            # Start a new output file if needed
            if row_counter % rows_per_file == 0:
                if output_file is not None:
                    output_file.close()
                    print(f"Created file: {output_path} with {min(rows_per_file, row_counter)} rows.")
                
                output_path = os.path.join(output_dir, f"processed_{file_counter:03d}.txt")
                output_file = open(output_path, 'w', encoding='utf-8')
                file_counter += 1
                row_counter = 0
            
            # Write the formatted data - only include the second separator if recovery_email exists
            if recovery_email:
                output_file.write(f"{email}|{password}|{recovery_email}\n")
            else:
                output_file.write(f"{email}|{password}\n")
            
            row_counter += 1
            total_rows += 1
        
        # Close the last output file
        if output_file is not None:
            output_file.close()
            print(f"Created file: {output_path} with {row_counter} rows.")
        
        print(f"Total rows processed: {total_rows}")
        print(f"Total files created: {file_counter - 1}")

def main():
    parser = argparse.ArgumentParser(description='Process a CSV file and split it into multiple output files.')
    parser.add_argument('input_file', nargs='?', default=None, 
                        help='Path to the input CSV file')
    parser.add_argument('--output-dir', default='processed', help='Output directory for processed files')
    parser.add_argument('--rows', type=int, default=1000, help='Number of rows per output file')
    
    args = parser.parse_args()
    
    # If no input file is provided, use a default path
    if args.input_file is None:
        args.input_file = os.path.join('data', 'origin', '5k-mht3sc.csv')
    
    # Verify that the input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Process the CSV file
    process_csv(args.input_file, args.output_dir, args.rows)

if __name__ == "__main__":
    main()