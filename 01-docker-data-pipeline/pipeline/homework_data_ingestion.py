import os
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

PARSE_DATES = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]


TRIPS_PARQUET_FILE = "green_tripdata_2025-11.parquet"
TRIPS_CSV_FILE = "green_tripdata_2025-11.csv"
ZONE_CSV_FILE = "taxi_zone_lookup.csv"


TRIPS_TABLE = "green_taxi_trips"
ZONE_TABLE = "taxi_zone_lookup"

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--chunksize', default=100_000, type=int, help='Chunk size')
def ingest_data(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize):

    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

   
    if not os.path.exists(TRIPS_PARQUET_FILE):
        raise FileNotFoundError(f"{TRIPS_PARQUET_FILE} not found")

    print("Reading parquet file...")
    df_green = pd.read_parquet(TRIPS_PARQUET_FILE)

    df_green = df_green.astype(DTYPE)
    df_green[PARSE_DATES] = df_green[PARSE_DATES].apply(
        pd.to_datetime
    )

    print("Converting parquet to CSV...")
    df_green.to_csv(TRIPS_CSV_FILE, index=False)

    print("Loading green taxi data to Postgres...")
    df_iter = pd.read_csv(
        TRIPS_CSV_FILE,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        chunksize=chunksize
    )

    first = True
    for chunk in tqdm(df_iter):
        if first:
            chunk.head(0).to_sql(
                TRIPS_TABLE,
                engine,
                if_exists='replace'
            )
            first = False

        chunk.to_sql(
            TRIPS_TABLE,
            engine,
            if_exists='append'
        )

    
    if not os.path.exists(ZONE_CSV_FILE):
        raise FileNotFoundError(f"{ZONE_CSV_FILE} not found")

    print("Loading taxi zone lookup data...")
    df_zone = pd.read_csv(
        ZONE_CSV_FILE,
        dtype={
            "LocationID": "Int64",
            "Borough": "string",
            "Zone": "string",
            "service_zone": "string"
        }
    )

    df_zone.to_sql(
        ZONE_TABLE,
        engine,
        if_exists='replace',
        index=False
    )

    print("Ingestion completed successfully.")


if __name__ == '__main__':
    ingest_data()
