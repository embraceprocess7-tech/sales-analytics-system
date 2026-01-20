#%% md
#Part 2 : Data Processing (List, Dictionaries & Functions)
#%% md
#Task 2.1 : sales Summary Calculator
#%% md
#2.1 a : calculate Total revenue
#%% md
#load the data for usage
#%%
def load_sales_data(file_path):
    transactions = []

    with open(file_path, "r", encoding="utf-8") as file:
        headers = file.readline().strip().split("|")

        for line in file:
            values = line.strip().split("|")

            # ❗ Skip malformed rows
            if len(values) != len(headers):
                continue

            record = dict(zip(headers, values))

            try:
                record["Quantity"] = int(record["Quantity"])
                record["UnitPrice"] = float(record["UnitPrice"].replace(",", ""))
            except (KeyError, ValueError):
                continue

            transactions.append(record)

    return transactions


#%%
import file_handler



#%%
transactions = load_sales_data("data/sales_data.txt")

#%%
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns:
        float: total revenue
    """
    total = 0.0
    for txn in transactions:
        total += txn["Quantity"] * txn["UnitPrice"]
    return total

#%% md
#verify
#%%
print(len(transactions))
print(transactions[0])

#%%
total_revenue = calculate_total_revenue(transactions)
print(total_revenue)

#%% md
#2.1b : Region_wise Sales Analysis
#%%
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns:
        dict: region-wise sales statistics
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    # Aggregate sales & count per region
    for txn in transactions:
        region = txn["Region"]
        sale_amount = txn["Quantity"] * txn["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += sale_amount
        region_data[region]["transaction_count"] += 1

    # Add percentage calculation
    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions

#%% md
#verify
#%%
region_data = region_wise_sales(transactions)
type(region_data), list(region_data.keys())


#%%
first_region = next(iter(region_data.values()))
first_region

#%% md
#2.1 c : Top Selling Products
#%%
def top_selling_products(transactions, n=5):
    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        qty = txn["Quantity"]
        revenue = qty * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    # Convert to required tuple format
    result = [
        (product, data["quantity"], data["revenue"])
        for product, data in product_data.items()
    ]

    # Sort by total quantity sold (descending)
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]

#%% md
#Verify
#%%
top_selling_products(transactions, 3)

#%% md
#2.1 (d) : Customer Purchase Analysis
#%%
def customer_analysis(transactions):
    customer_data = {}

    for txn in transactions:
        customer = txn.get("CustomerID")

        # Skip records with missing customer ID
        if not customer:
            continue

        amount = txn["Quantity"] * txn["UnitPrice"]
        product = txn["ProductName"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products"].add(product)

    # Final formatting
    result = {}

    for customer, data in customer_data.items():
        avg_order_value = (
            data["total_spent"] / data["purchase_count"]
            if data["purchase_count"] > 0 else 0
        )

        result[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": sorted(list(data["products"]))
        }

    # Sort by total_spent descending
    result = dict(
        sorted(
            result.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return result

#%% md
#verify
#%%
customer_stats = customer_analysis(transactions)

for customer, data in list(customer_stats.items())[:3]:
    print(customer, data)

#%% md
#Task 2.2 : data _based Analysis
#%% md
#2.2 a Daily sales Trend
#%%
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    """

    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Final formatting
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": daily_data[date]["revenue"],
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result
#%% md
#verify
#%%
trend = daily_sales_trend(transactions)
print(list(trend.items())[:2])
#%% md
#2.2 b Find_peak_sales_day(transactions)
#%%
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: (date, revenue, transaction_count)
    """

    daily_summary = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_summary:
            daily_summary[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_summary[date]["revenue"] += amount
        daily_summary[date]["transaction_count"] += 1

    peak_date = None
    max_revenue = 0.0
    peak_tx_count = 0

    for date, data in daily_summary.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            peak_tx_count = data["transaction_count"]

    return peak_date, max_revenue, peak_tx_count
#%% md
#verify
#%%
peak = find_peak_sales_day(transactions)
print(peak)
#%% md
#2.3 Product performance
#%% md
#2.3 a Low_performing_products
#%%
from collections import defaultdict

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales.

    Returns:
    List of tuples -> (ProductName, TotalQuantity, TotalRevenue)
    """

    product_stats = defaultdict(lambda: {"qty": 0, "revenue": 0.0})

    # Aggregate quantity and revenue per product
    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        price = tx["UnitPrice"]

        product_stats[name]["qty"] += qty
        product_stats[name]["revenue"] += qty * price

    # Filter low-performing products
    result = []
    for product, data in product_stats.items():
        if data["qty"] < threshold:
            result.append(
                (product, data["qty"], data["revenue"])
            )

    # Sort by TotalQuantity ascending
    result.sort(key=lambda x: x[1])

    return result
#%% md
#verify the correctness
#%%
low_products = low_performing_products(transactions, threshold=10)

print("Low Performing Products:")
for p in low_products:
    print(p)