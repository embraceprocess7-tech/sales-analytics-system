#%% md
#Part 3 - API Integreation

#Base URL - https://dummyjson.com/products
#%% md
#Task 3.1(a) Fetch all Products
#%%
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns:
        list: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("Successfully fetched products")
        return products

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products")
        return []

#%% md
#verify
#%%
products = fetch_all_products()
print(len(products))
print(products[0])
#%% md
#Task 3.1(b) create product mapping
#%%
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters:
    - api_products: list of products from fetch_all_products()

    Returns:
    - dictionary mapping product IDs to product info
    """

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping

#%% md
#verify
#%%
products = fetch_all_products()
product_map = create_product_mapping(products)

list(product_map.items())[:1]

#%% md
#3.2 Enrich sales data
#%% md
#loading data_processor
#%%
import file_handler
import data_processor


#%% md
#load_sales_data

#%%
import data_processor

transactions = data_processor.load_sales_data("data/sales_data.txt")


#%%
def enrich_sales_data(transactions, product_mapping):
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        product_id_raw = txn.get("ProductID", "")
        api_match = False

        try:
            # Extract numeric ID from ProductID (e.g., P101 -> 101)
            product_id = int(product_id_raw[1:])

            api_product = product_mapping.get(product_id)

            if api_product:
                enriched_txn["API_Category"] = api_product.get("category")
                enriched_txn["API_Brand"] = api_product.get("brand")
                enriched_txn["API_Rating"] = api_product.get("rating")
                api_match = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None

        enriched_txn["API_Match"] = api_match
        enriched_transactions.append(enriched_txn)

    return enriched_transactions

#%% md
#verify
#%%
products = fetch_all_products()
product_mapping = create_product_mapping(products)

len(product_mapping)

#%%
enriched = enrich_sales_data(transactions, product_mapping)
enriched[0]

#%% md
#save_enrich_data
#%%
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    if not enriched_transactions:
        return

    headers = list(enriched_transactions[0].keys())

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for txn in enriched_transactions:
            row = []
            for h in headers:
                value = txn.get(h)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")


    print(f"Enriched data saved successfully to {filename}")
#%% md
#Verify
#%%
save_enriched_data(enriched, "data/enriched_sales_data.txt")
