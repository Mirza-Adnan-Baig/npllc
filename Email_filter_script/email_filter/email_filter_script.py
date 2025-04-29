import os
import pandas as pd
import re

def extract_and_merge_emails(input_folder, merged_folder, merged_filename):
    try:
        all_emails = set()  # Use a set to avoid duplicate emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Regex for email addresses

        # Create the merged folder if it doesn't exist
        os.makedirs(merged_folder, exist_ok=True)

        files_processed = 0  # Track number of files processed

        # Process each XLSX file in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.xlsx'):  # Only process .xlsx files
                filepath = os.path.join(input_folder, filename)
                print(f"Processing file: {filename}")

                try:
                    df = pd.read_excel(filepath, sheet_name=None)  # Load all sheets into a dictionary
                    files_processed += 1
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue  # Skip this file and continue processing others

                # Iterate through all sheets
                for sheet_name, sheet_data in df.items():
                    for column in sheet_data.columns:
                        column_data = sheet_data[column].astype(str).fillna("")
                        emails = column_data.apply(lambda x: re.findall(email_pattern, x))
                        for email_list in emails:
                            all_emails.update(email_list)

        if files_processed == 0:
            print("No valid XLSX files were found. Exiting...")
            return None  # Prevents proceeding to split_csv_into_chunks()

        # Prepare and save the merged DataFrame
        trimmed_emails = [email.strip() for email in all_emails]
        email_df = pd.DataFrame({"email": trimmed_emails})
        merged_file_path = os.path.join(merged_folder, merged_filename)
        email_df.to_csv(merged_file_path, index=False)

        print(f"Merged {len(trimmed_emails)} unique emails into {merged_file_path}")
        return merged_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def split_csv_into_chunks(merged_csv, output_folder, chunk_size=200):
    try:
        if not merged_csv or not os.path.exists(merged_csv):
            print("Merged CSV file is missing or invalid. Skipping email splitting.")
            return

        os.makedirs(output_folder, exist_ok=True)

        df = pd.read_csv(merged_csv)
        total_rows = len(df)
        print(f"Total emails to split: {total_rows}")

        for i in range(0, total_rows, chunk_size):
            chunk = df[i:i + chunk_size]
            chunk_filename = os.path.join(output_folder, f"emails_{i + 1}_to_{i + len(chunk)}.csv")
            chunk.to_csv(chunk_filename, index=False)
            print(f"Saved chunk: {chunk_filename}")

        print(f"Splitting complete. Files saved in {output_folder}")

    except Exception as e:
        print(f"An error occurred while splitting: {e}")

# Example usage
input_folder = 'Leo_fisher_sheet'
merged_folder = 'Leo_fisher_sheet_Merged'
merged_filename = 'Leo_fisher_sheet.csv'
output_folder = 'Leo_fisher_sheet_Split'

# Step 1: Extract and merge emails
merged_csv_path = extract_and_merge_emails(input_folder, merged_folder, merged_filename)

# Step 2: Split into chunks only if merging was successful
if merged_csv_path:
    split_csv_into_chunks(merged_csv_path, output_folder, chunk_size=400)
