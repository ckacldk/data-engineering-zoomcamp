import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import click


@click.command()
@click.option('--year', default=2025, type=int, help='Year of taxi data')
@click.option('--month', default=11, type=int, help='Month of taxi data')
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-database', default='green_taxi', help='PostgreSQL database name')
@click.option('--pg-batch-size', default=10000, type=int, help='Batch size for data loading')
def run(year, month, pg_user, pg_pass, pg_host, pg_port, pg_database, pg_batch_size):

    # -----------------------------
    # Download parquet
    # -----------------------------
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'

    df = pd.read_parquet(url)

    # -----------------------------
    # Postgres connection
    # -----------------------------
    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_database}'
    )

    # -----------------------------
    # Create table schema
    # -----------------------------
    df.head(0).to_sql(
        name='green_taxi_data',
        con=engine,
        if_exists='replace',
        index=False
    )

    print(pd.io.sql.get_schema(df, name='green_taxi_data', con=engine))

    # -----------------------------
    # Load data in batches
    # -----------------------------
    for i in tqdm(range(0, len(df), pg_batch_size)):
        chunk = df.iloc[i:i + pg_batch_size]

        chunk.to_sql(
            name='green_taxi_data',
            con=engine,
            if_exists='append',
            index=False
        )

    print("Green taxi data load finished")

    # -----------------------------
    # Verify row count
    # -----------------------------
    result = pd.read_sql(
        "SELECT COUNT(*) FROM green_taxi_data",
        engine
    )
    print(result)

    # -----------------------------
    # Load taxi zone lookup
    # -----------------------------
    zones_url = (
        'https://github.com/DataTalksClub/nyc-tlc-data/'
        'releases/download/misc/taxi_zone_lookup.csv'
    )

    df_zones = pd.read_csv(zones_url)

    df_zones.to_sql(
        name='taxi_zone_lookup',
        con=engine,
        if_exists='replace',
        index=False
    )

    print("Taxi zone lookup load finished")


if __name__ == "__main__":
    run()
