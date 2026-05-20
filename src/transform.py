import logging

def clean_data(datasets):

        
    if "geolocation" in datasets:
        datasets["geolocation"].drop_duplicates(
            subset='geolocation_zip_code_prefix',
            keep='first',
            inplace=True,
            ignore_index=True
        )
        logging.info("Geolocation: duplicates removed")

   
    if "orders" in datasets:
        before = len(datasets["orders"])
        datasets["orders"] = datasets["orders"][
            datasets["orders"]["order_status"] == "delivered"
        ].reset_index(drop=True)
        after = len(datasets["orders"])
        logging.info(f"Orders: filtered to 'delivered' only ({before} → {after} rows)")

   
    if "orders" in datasets:
        valid_orders = set(datasets["orders"]["order_id"])

        if "items" in datasets:
            datasets["items"] = datasets["items"][
                datasets["items"]["order_id"].isin(valid_orders)
            ].reset_index(drop=True)
            logging.info(f"Items: filtered to delivered orders only ({len(datasets['items'])} rows)")

        if "payments" in datasets:
            datasets["payments"] = datasets["payments"][
                datasets["payments"]["order_id"].isin(valid_orders)
            ].reset_index(drop=True)
            logging.info(f"Payments: filtered to delivered orders only ({len(datasets['payments'])} rows)")

        if "reviews" in datasets:
            datasets["reviews"] = datasets["reviews"][
                datasets["reviews"]["order_id"].isin(valid_orders)
            ].reset_index(drop=True)
            logging.info(f"Reviews: filtered to delivered orders only ({len(datasets['reviews'])} rows)")

    
    if "products" in datasets and "category_translations" in datasets:
        translations = (
            datasets["category_translations"]
            .set_index("product_category_name")["product_category_name_english"]
            .to_dict()
        )
        datasets["products"]["product_category_name"] = (
            datasets["products"]["product_category_name"]
            .map(translations)
            .fillna(datasets["products"]["product_category_name"])
        )
        logging.info("Products: category names mapped to English")

    return datasets