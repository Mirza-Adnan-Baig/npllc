import os
import pandas as pd
import re

# Step 1: Extract emails from multiple XLSX files and merge into one CSV
def extract_and_merge_emails(input_folder, merged_folder, merged_filename):
    try:
        all_emails = set()  # Use a set to avoid duplicate emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Regex for email addresses

        # Create the merged folder if it doesn't exist
        os.makedirs(merged_folder, exist_ok=True)

        # Process each XLSX file in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.xlsx'):  # Only process .xlsx files
                filepath = os.path.join(input_folder, filename)
                print(f"Processing file: {filename}")

                # Load the Excel file
                df = pd.read_excel(filepath, sheet_name=None)  # Load all sheets into a dictionary

                # Iterate through all sheets
                for sheet_name, sheet_data in df.items():
                    for column in sheet_data.columns:
                        # Convert each column to a string and scan for email matches
                        column_data = sheet_data[column].astype(str).fillna("")
                        emails = column_data.apply(lambda x: re.findall(email_pattern, x))
                        for email_list in emails:
                            all_emails.update(email_list)  # Add found emails to the set

        # Prepare a DataFrame
        trimmed_emails = [email.strip() for email in all_emails]
        email_df = pd.DataFrame({"email": trimmed_emails})

        # Save merged emails to CSV
        merged_file_path = os.path.join(merged_folder, merged_filename)
        email_df.to_csv(merged_file_path, index=False)
        print(f"Merged {len(trimmed_emails)} unique email(s) into {merged_file_path}")

        return merged_file_path  # Return the path of the merged file for the next step

    except Exception as e:
        print(f"An error occurred: {e}")

# Step 2: Split the merged CSV into chunks of 400 emails
def split_csv_into_chunks(merged_csv, output_folder, chunk_size=400):
    try:
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Load the merged CSV file
        df = pd.read_csv(merged_csv)
        total_rows = len(df)
        print(f"Total emails to split: {total_rows}")

        # Split the data into chunks
        for i in range(0, total_rows, chunk_size):
            chunk = df[i:i + chunk_size]  # Get the current chunk
            chunk_filename = os.path.join(output_folder, f"emails_{i + 1}_to_{i + len(chunk)}.csv")
            chunk.to_csv(chunk_filename, index=False)
            print(f"Saved chunk: {chunk_filename}")

        print(f"Split complete. Files saved in {output_folder}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_folder = 'Areeb_client_sheet'  # Folder containing the input XLSX files
merged_folder = 'Areeb_client_sheet_merged'  # Folder to save the merged CSV
merged_filename = 'Areeb_client_sheet.csv'  # Name of the merged CSV file
output_folder = 'split_Areeb_client_sheet'  # Folder to save the split CSV files

# Step 1: Extract and merge emails
merged_csv_path = extract_and_merge_emails(input_folder, merged_folder, merged_filename)

# Step 2: Split the merged CSV into chunks of 400 emails
split_csv_into_chunks(merged_csv_path, output_folder, chunk_size=300)

