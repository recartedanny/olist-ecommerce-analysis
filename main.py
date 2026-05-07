from src.extract import build_dataset
from src.transform import clean_data
from src.load import get_connections,create_database, save_database
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
load_dotenv()

def main():

    
    datasets = build_dataset()
    datasets_clean= clean_data(datasets)
    conn, engine = get_connections()
    create_database(conn)
    save_database(engine, datasets_clean,conn)

if __name__ == "__main__":
    main()










     