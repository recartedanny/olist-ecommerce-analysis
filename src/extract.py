import pandas as pd
import logging



#csv names
FILES = {
    "customers":             "data-csv/olist_customers_dataset.csv",
    "geolocation":           "data-csv/olist_geolocation_dataset.csv",
    "products":              "data-csv/olist_products_dataset.csv",
    "sellers":               "data-csv/olist_sellers_dataset.csv",
    "orders":                "data-csv/olist_orders_dataset.csv",
    "items":                 "data-csv/olist_order_items_dataset.csv",
    "payments":              "data-csv/olist_order_payments_dataset.csv",
    "reviews":               "data-csv/olist_order_reviews_dataset.csv",
    "category_translations": "data-csv/product_category_name_translation.csv",
}

def read_csv (csv):
    try:
        
        result = pd.read_csv(csv)
        return result
    except Exception as e:
        logging.error(f"An error has occurred reading the file {csv}: {e}")
        raise


def build_dataset ():


   
    result ={}
    for name,file in FILES.items():
            try:
                logging.info(f"Loading dataset: {name} from {file}...")
                data = read_csv(file)
                result[name] = data
            except Exception as e:
                logging.error(f"An error has occurred: {e}")

    return result

