
import psycopg2
import os
import logging
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
load_dotenv()




DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_connections():
    engine = create_engine(DATABASE_URL)
    conn = psycopg2.connect(
                 dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
    logging.debug("Conexión exitosa")

    

    return conn, engine

def create_database(conn):
  
        
     
     try:
            
            cursor=conn.cursor()
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS customers(
                        customer_id TEXT PRIMARY KEY,
                        customer_unique_id TEXT,
                        customer_zip_code_prefix TEXT,
                        customer_city TEXT,
                        customer_state TEXT
                        );
            """)
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS sellers(
                        seller_id TEXT PRIMARY KEY,
                        seller_zip_code_prefix TEXT,
                        seller_city TEXT,
                        seller_state TEXT
                        );

            """)
            cursor.execute("""
            
                        CREATE TABLE IF NOT EXISTS orders (
                        order_id TEXT,
                        customer_id TEXT,
                        order_status TEXT,
                        order_purchase_timestamp TIMESTAMP,
                        order_approved_at TIMESTAMP,
                        order_delivered_carrier_date TIMESTAMP,
                        order_delivered_customer_date TIMESTAMP,
                        order_estimated_delivery_date TIMESTAMP,

                        PRIMARY KEY(order_id),
                        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                        );
            """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS geolocation(
                        geolocation_zip_code_prefix TEXT PRIMARY KEY,
                        geolocation_lat REAL,
                        geolocation_lng REAL,
                        geolocation_city TEXT,
                        geolocation_state TEXT);
                            """)
            cursor.execute("""
            
                        CREATE TABLE IF NOT EXISTS products(
                        product_id TEXT PRIMARY KEY,
                        product_category_name TEXT,
                        product_name_lenght INTEGER,
                        product_description_lenght INTEGER,
                        product_photos_qty INTEGER,
                        product_weight_g REAL,
                        product_length_cm REAL,
                        product_height_cm REAL,
                        product_width_cm REAL

                        );
            """)
            
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS items(
                        order_id TEXT,
                        order_item_id INTEGER,
                        product_id TEXT,
                        seller_id TEXT,
                        shipping_limit_date TIMESTAMP,
                        price REAL,
                        freight_value REAL,

                        PRIMARY KEY (order_id,order_item_id),
                        FOREIGN KEY (product_id) REFERENCES products (product_id),
                        FOREIGN KEY(order_id) REFERENCES orders (order_id),
                        FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
                        );
            """)
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS payments(
                        order_id TEXT ,
                        payment_sequential INTEGER,
                        payment_type TEXT,
                        payment_installments INTEGER,
                        payment_value REAL,
                        PRIMARY KEY (order_id,payment_sequential)
                        );
            """)

            cursor.execute("""

                        CREATE TABLE IF NOT EXISTS reviews(
                        review_id TEXT,
                        order_id TEXT,
                        review_score INTEGER,
                        review_comment_title TEXT,
                        review_comment_message TEXT,
                        review_creation_date TIMESTAMP,
                        review_answer_timestamp TIMESTAMP,

                        PRIMARY KEY(review_id, order_id),
                        FOREIGN KEY(order_id) REFERENCES orders (order_id)
                        );
            """)
            
            
            
            cursor.execute("""

                        CREATE TABLE IF NOT EXISTS category_translations(
                        product_category_name TEXT PRIMARY KEY,
                        product_category_name_english TEXT);
                            """
            )
            conn.commit()
            cursor.close()
     except Exception as e:
         logging.error(f"Error: {e}")
        




     
     

def save_database(engine,datasets,conn):
    
    try:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE reviews, category_translations, payments, items, orders, products, sellers, geolocation, customers CASCADE")
        logging.info("The tables have been trucated")
        conn.commit()
        cursor.close()
       
        logging.debug("Conexión exitosa con SQLAlchemy")
           
            
        for name,df in datasets.items():
                try:
                    df.to_sql(name, con=engine, if_exists='append', index=False)
                    
                    
                    logging.info(f"Loaded {len(df)} rows into {name}")

                except Exception as e:
                    logging.error(f"Error in loading {name} - Error= {e}")
          
        
    except Exception as e:
        logging.error(f"Error: {e}")


    return 