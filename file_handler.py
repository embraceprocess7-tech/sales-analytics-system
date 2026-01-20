#%% md
#Part-1 : data File Handler & Preprocessing (File I/O & Error Handling)
#%% md
#Task 1.1 Read Sales data with Encoding Handling
#%% md
#Create a function that reads the sales data file handling encoding issues
#%%
import csv
#%%
def read_sales_data(sales_data):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open("data/sales_data.txt", "r", encoding=encoding) as file:
                lines = file.readlines()

                # Skip header and remove empty lines
                data_lines = [
                    line.strip()
                    for line in lines[1:]
                    if line.strip()
                ]

                return data_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{"sales_data.txt"}' not found.")
            return []

    # If no encoding worked
    print("Error: Unable to read file with supported encodings.")
    return []


data = read_sales_data("sales_data.txt")
print(type(data))
print(len(data))
print(data[:3])

print(data)

#%%
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Handle commas in ProductName
        product_name = product_name.replace(",", " ")

        # Remove commas from numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name.strip(),
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
#%%
raw = read_sales_data("sales_data.txt")
parsed = parse_transactions(raw)

print(len(parsed))
print(parsed[0])
print(type(parsed[0]["Quantity"]))
print(type(parsed[0]["UnitPrice"]))
#%% md
#Part 1.3 : Data validation and Filtering
#%%
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    Returns: (valid_transactions, invalid_count, filter_summary)
    """

    required_fields = {
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    }

    valid = []
    invalid_count = 0

    # Validation
    for tx in transactions:
        if not required_fields.issubset(tx.keys()):
            invalid_count += 1
            continue

        if (
            tx["Quantity"] <= 0 or
            tx["UnitPrice"] <= 0 or
            not tx["TransactionID"].startswith("T") or
            not tx["ProductID"].startswith("P") or
            not tx["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        valid.append(tx)

    total_input = len(transactions)

    # Display available regions
    regions = sorted({tx["Region"] for tx in valid if tx["Region"]})
    print("Available Regions:", regions)

    # Transaction amount range
    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid]
    if amounts:
        print("Transaction Amount Range:", min(amounts), "-", max(amounts))

    filtered_by_region = 0
    filtered_by_amount = 0

    filtered = valid

    # Apply region filter
    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Region"] == region]
        filtered_by_region = before - len(filtered)
        print("After region filter:", len(filtered))

    # Apply amount filters
    if min_amount is not None:
        before = len(filtered)
        filtered = [
            tx for tx in filtered
            if tx["Quantity"] * tx["UnitPrice"] >= min_amount
        ]
        filtered_by_amount += before - len(filtered)

    if max_amount is not None:
        before = len(filtered)
        filtered = [
            tx for tx in filtered
            if tx["Quantity"] * tx["UnitPrice"] <= max_amount
        ]
        filtered_by_amount += before - len(filtered)

    if min_amount is not None or max_amount is not None:
        print("After amount filter:", len(filtered))

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary

raw = read_sales_data("sales_data.txt")
parsed = parse_transactions(raw)

valid_tx, invalid_count, summary = validate_and_filter(
    parsed,
    region="North",
    min_amount=5000,
    max_amount=200000
)

print("Invalid count:", invalid_count)
print("Summary:", summary)
print("Sample valid transaction:", valid_tx[0])
