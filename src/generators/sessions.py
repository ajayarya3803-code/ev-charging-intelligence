from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

SESSION_STATUSES = [
    'Completed',
    'Completed',
    'Completed',
    'Completed',
    'Completed',
    'Completed',
    'Completed',
    'Completed',
    'Cancelled',
    'Failed',
    'Started'
]


def generate_sessions(vehicles_df, stations_df, n=10000):

    records = []

    vehicles = vehicles_df.to_dict('records')
    station_ids = stations_df['station_id'].tolist()

    for i in range(n):

        vehicle = random.choice(vehicles)
        station_id = random.choice(station_ids)

        status = random.choice(SESSION_STATUSES)

        if status == 'Started':
            start_time = fake.date_time_between(
                start_date='-2h',
                end_date='now'
            )
            end_time = None
            energy = round(
                random.uniform(1, min(float(vehicle['battery_capacity']) * 0.3, 25)),
                3
            )
            updated_at = fake.date_time_between(
                start_date=start_time,
                end_date='now'
            )

        else:
            start_time = fake.date_time_between(
                start_date='-1y',
                end_date='-1d'
            )

            duration_minutes = random.randint(15, 240)

            end_time = start_time + pd.Timedelta(
                minutes=duration_minutes
            )

            if status == 'Completed':
                max_energy = min(
                    float(vehicle['battery_capacity']) * 0.8,
                    80
                )
                energy = round(
                    random.uniform(2, max_energy),
                    3
                )
            else:
                energy = round(random.uniform(0, 10), 3)

            updated_at = end_time

        record = {
            'session_id': f'SESS{10001+i}',
            'vehicle_id': vehicle['vehicle_id'],
            'station_id': station_id,
            'start_time': start_time,
            'end_time': end_time,
            'energy_consumed_kwh': energy,
            'session_status': status,
            'created_at': start_time,
            'updated_at': updated_at
        }

        records.append(record)

    return pd.DataFrame(records)


if __name__ == '__main__':

    vehicles_df = pd.read_csv(
        'data/generated/vehicles.csv'
    )

    stations_df = pd.read_csv(
        'data/generated/stations.csv'
    )

    sessions_df = generate_sessions(
        vehicles_df,
        stations_df
    )

    sessions_df.to_csv(
        'data/generated/sessions.csv',
        index=False
    )

    print(sessions_df.head())
    print("Total sessions:", len(sessions_df))
    print(sessions_df['session_status'].value_counts())

    print("Unique session IDs:",
          sessions_df['session_id'].nunique())

    print("Valid vehicle references:",
          sessions_df['vehicle_id'].isin(
              vehicles_df['vehicle_id']
          ).all())

    print("Valid station references:",
          sessions_df['station_id'].isin(
              stations_df['station_id']
          ).all())

    print("Negative energy values:",
          (sessions_df['energy_consumed_kwh'] < 0).sum())

    print("Invalid end times:",
          (
              sessions_df['end_time'].notna()
              & (
                  sessions_df['end_time']
                  <= sessions_df['start_time']
              )
          ).sum())