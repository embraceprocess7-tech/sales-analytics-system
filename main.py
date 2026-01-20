#%%

#%% md
#Task 5.1 Create main script
#%%
import file_handler
import data_processor
import api_handler
import output

def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Load sales data
        print("\n[1/10] Reading sales data...")
        transactions = data_processor.load_sales_data("data/sales_data.txt")
        print(f"✓ Loaded {len(transactions)} transactions")

        # [2/10] Parsing & cleaning (already done in load_sales_data)
        print("\n[2/10] Parsing and cleaning data...")
        valid_tx = transactions

        # [3/10] Sales analytics
        print("\n[3/10] Analyzing sales data...")
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)

        # [4/10] Fetch API products
        print("\n[4/10] Fetching product data...")
        api_products = fetch_all_products()
        product_map = create_product_mapping(api_products)

        # [5/10] Enrich sales data
        print("\n[5/10] Enriching sales data...")
        enriched = enrich_sales_data(valid_tx, product_map)

        # [6/10] Save enriched data
        print("\n[6/10] Saving enriched data...")
        save_enriched_data(enriched)

        # [7/10] Generate report
        print("\n[7/10] Generating report...")
        generate_sales_report(valid_tx, enriched)

        print("\n[10/10] Process completed successfully!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print(str(e))

#%%

#%%
main()
