
import pandas as pd

from pathlib import Path
from sqlalchemy import text

from src.database.connection import get_sql_engine


DATA_DIR = Path("data/generated")

# Parent tables must be loaded before child tables
DATASETS = [
    ("customers", "customers.csv", []),
    ("vehicles", "vehicles.csv", ["created_at", "updated_at"]),
    ("charging_stations", "stations.csv", ["created_at", "updated_at"]),
    ("charging_sessions", "sessions.csv",
     ["start_time", "end_time", "created_at", "updated_at"]),
    ("transactions", "transactions.csv",
     ["transaction_timestamp", "created_at", "updated_at"])
]


def load_data():

    engine = get_sql_engine()

    try:
        # Read all CSV files before starting the database load
        dataframes = {}

        for table_name, filename, date_columns in DATASETS:

            file_path = DATA_DIR / filename

            if not file_path.exists():
                raise FileNotFoundError(f"Missing file: {file_path}")

            df = pd.read_csv(
                file_path,
                parse_dates=date_columns
            )

            dataframes[table_name] = df

            print(f"{table_name}: {len(df)} records ready")

        # Load all tables in one database transaction
        with engine.begin() as connection:

            # Prevent accidental duplicate loading
            for table_name, _, _ in DATASETS:

                count = connection.execute(
                    text(f"SELECT COUNT(*) FROM dbo.[{table_name}]")
                ).scalar()

                if count != 0:
                    raise RuntimeError(
                        f"Table {table_name} is not empty. "
                        "Stopping to prevent duplicate records."
                    )

            # Insert data in foreign-key order
            for table_name, _, _ in DATASETS:

                df = dataframes[table_name]

                df.to_sql(
                    name=table_name,
                    con=connection,
                    schema="dbo",
                    if_exists="append",
                    index=False,
                    chunksize=1000
                )

                print(
                    f"Loaded {len(df)} records into dbo.{table_name}"
                )

        print("\nAll datasets loaded successfully!")

    except Exception as e:
        print("\nData loading failed:", e)
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    load_data()
