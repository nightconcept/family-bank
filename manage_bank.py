import json
import argparse
from datetime import datetime, timezone
import os
import sys

# --- Point to the JSON file in the data directory ---
DATA_FILE = 'data/transactions.json'

def get_current_data(filename):
    """Reads the JSON data file."""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        # Return empty list if file doesn't exist or is empty
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Basic validation: Ensure it's a list
            if not isinstance(data, list):
                print(f"Warning: Data in {filename} is not a JSON list. Starting fresh.", file=sys.stderr)
                return []
            return data
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filename}. Starting fresh.", file=sys.stderr)
        # Handle case where file exists but contains invalid JSON
        return []
    except Exception as e:
        print(f"Error reading data from {filename}: {e}", file=sys.stderr)
        # For critical errors, maybe exit
        # sys.exit(f"Critical error reading data. Aborting.")
        return [] # Or return empty list to attempt recovery

def add_transaction(filename, description, amount_str):
    """Reads JSON, adds a new transaction, and writes JSON back."""
    transactions = get_current_data(filename)
    current_balance = 0.0
    if transactions: # Check if the list is not empty
         # Get balance from the last dictionary in the list
        try:
            current_balance = float(transactions[-1].get('balance', 0.0))
        except (ValueError, TypeError):
             print(f"Warning: Could not parse balance from last transaction: {transactions[-1]}. Assuming 0.0.", file=sys.stderr)
             current_balance = 0.0

    try:
        transaction_amount = float(amount_str)
    except ValueError:
        print(f"Error: Invalid amount '{amount_str}'. Please provide a number.", file=sys.stderr)
        return False # Indicate failure

    new_balance = current_balance + transaction_amount
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Create the new transaction as a dictionary
    new_transaction = {
        "timestamp": timestamp,
        "description": description,
        "amount": round(transaction_amount, 2), # Store as float, rounded
        "balance": round(new_balance, 2)      # Store as float, rounded
    }

    # Append the new transaction dictionary to the list
    transactions.append(new_transaction)

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Write the entire updated list back to the file
        # Use indent for readability
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)

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
    parser = argparse.ArgumentParser(description="Add a transaction to the Kids Bank JSON.")
    parser.add_argument("amount", help="Transaction amount (positive for deposit, negative for withdrawal)")
    parser.add_argument("-d", "--description", required=True, help="Short description of the transaction")

    args = parser.parse_args()

    if not add_transaction(DATA_FILE, args.description, args.amount):
         sys.exit(1) # Exit with error code if transaction failed