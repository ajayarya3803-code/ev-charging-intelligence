
from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

city_coordinates = {
    'Bengaluru': (12.85, 13.15, 77.45, 77.75),
    'Chennai': (12.90, 13.20, 80.15, 80.35),
    'Hyderabad': (17.25, 17.55, 78.30, 78.60),
    'Mumbai': (18.85, 19.25, 72.75, 73.05),
    'Pune': (18.40, 18.65, 73.75, 74.00),
    'Delhi': (28.45, 28.80, 76.95, 77.35),
    'Kochi': (9.85, 10.10, 76.20, 76.40),
    'Mysuru': (12.20, 12.40, 76.55, 76.75)
}


def generate_stations(n=100):
    records = []

    for i in range(n):

        created_at = fake.date_time_between(
            start_date='-1y',
            end_date='now'
        )

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date='now'
        )

        city = fake.random_element(list(city_coordinates.keys()))

        min_lat, max_lat, min_lon, max_lon = city_coordinates[city]

        latitude = round(random.uniform(min_lat, max_lat), 6)
        longitude = round(random.uniform(min_lon, max_lon), 6)

        record = {
            'station_id': f'S{1001+i}',
            'station_name': f'{fake.company()} Charging Station',
            'city': city,
            'latitude': latitude,
            'longitude': longitude,
            'total_chargers': fake.random_int(min=2, max=10),
            'created_at': created_at,
            'updated_at': updated_at
        }

        records.append(record)

    return pd.DataFrame(records)


if __name__ == "__main__":

    stations_df = generate_stations()

    stations_df.to_csv(
        'data/generated/stations.csv',
        index=False
    )

    print(stations_df.head())
    print("Total stations:", len(stations_df))
