import csv
import argparse
from datetime import datetime, timezone
import os
import sys

CSV_FILE = 'data/transactions.csv'
HEADERS = ['timestamp', 'description', 'amount', 'balance']

def get_last_balance(filename):
    """Reads the last row of the CSV to get the latest balance."""
    last_balance = 0.0
    try:
        # Check if file exists and is not empty
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Skip header if exists
                header = next(reader, None)
                if header and header == HEADERS:
                    last_row = None
                    for row in reader: # Read all rows to get the last one
                        last_row = row
                    if last_row:
                        try:
                            last_balance = float(last_row[3]) # Balance is the 4th column (index 3)
                        except (ValueError, IndexError):
                            print(f"Warning: Could not parse balance from last row: {last_row}", file=sys.stderr)
                            # Optionally: Fallback or raise error
                elif header:
                     print(f"Warning: CSV header mismatch or file is corrupt. Expected {HEADERS}, got {header}. Starting balance assumed 0.", file=sys.stderr)
                # If only header exists, last_balance remains 0.0
        else:
             print(f"Info: CSV file '{filename}' not found or empty. Starting balance is 0.0.", file=sys.stderr)
             # Ensure the directory exists
             os.makedirs(os.path.dirname(filename), exist_ok=True)
             # Create file with header
             with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                 writer = csv.writer(csvfile)
                 writer.writerow(HEADERS)
                 print(f"Info: Created '{filename}' with headers.", file=sys.stderr)


    except FileNotFoundError:
        print(f"Info: CSV file '{filename}' not found. Starting balance is 0.0.", file=sys.stderr)
         # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
         # Create file with header
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(HEADERS)
            print(f"Info: Created '{filename}' with headers.", file=sys.stderr)
    except Exception as e:
        print(f"Error reading last balance from {filename}: {e}", file=sys.stderr)
        # Depending on desired robustness, you might want to exit here
        # sys.exit(f"Critical error reading balance. Aborting.")

    return last_balance

def add_transaction(filename, description, amount):
    """Appends a new transaction to the CSV file."""
    current_balance = get_last_balance(filename)
    try:
        transaction_amount = float(amount)
    except ValueError:
        print(f"Error: Invalid amount '{amount}'. Please provide a number.", file=sys.stderr)
        return False # Indicate failure

    new_balance = current_balance + transaction_amount
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    new_row = [timestamp, description, f"{transaction_amount:.2f}", f"{new_balance:.2f}"]

    try:
        # Use 'a' to append. 'newline=""' prevents extra blank rows.
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_row)
        print("Transaction added successfully:")
        print(f"  Timestamp: {timestamp}")
        print(f"  Description: {description}")
        print(f"  Amount: {transaction_amount:.2f}")
        print(f"  New Balance: {new_balance:.2f}")
        return True # Indicate success
    except Exception as e:
        print(f"Error writing transaction to {filename}: {e}", file=sys.stderr)
        return False # Indicate failure

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a transaction to the Kids Bank CSV.")
    parser.add_argument("amount", help="Transaction amount (positive for deposit, negative for withdrawal)")
    parser.add_argument("-d", "--description", required=True, help="Short description of the transaction")

    args = parser.parse_args()

    if not add_transaction(CSV_FILE, args.description, args.amount):
         sys.exit(1) # Exit with error code if transaction failed