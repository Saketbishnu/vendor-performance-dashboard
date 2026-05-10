import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Configure logging
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Create SQL engine (SQLite database)
engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    """Helper function to load a DataFrame into the database."""
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f" Successfully ingested {table_name} with {df.shape[0]} rows.")
    except Exception as e:
        logging.error(f" Error ingesting {table_name}: {e}")

def load_raw_data():
    """Load all CSV files as DataFrames and ingest into the database."""
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            try:
                df = pd.read_csv('data/' + file)
                logging.info(f" Ingesting {file} into database...")
                ingest_db(df, file[:-4], engine)
            except Exception as e:
                logging.error(f" Error reading {file}: {e}")
    end = time.time()
    total_time = (end - start) / 60
    logging.info("------------- Ingestion complete -------------")
    logging.info(f"⏱ Total Time Taken: {total_time:.2f} minutes")

if __name__ == "__main__":
    load_raw_data()
