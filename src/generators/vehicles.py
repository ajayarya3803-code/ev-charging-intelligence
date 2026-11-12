
from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

vehicle_catalog = {
    'Tata': ['Nexon EV', 'Punch EV', 'Tiago EV'],
    'Mahindra': ['BE 6', 'XUV400'],
    'MG': ['ZS EV', 'Comet EV'],
    'Hyundai': ['Kona Electric', 'Ioniq 5'],
    'BYD': ['Atto 3', 'Seal']
}

def generate_vehicles(customers_df, n=1200):

    records = []
    registrations = set()

    customer_ids = customers_df['customer_id'].tolist()

    for i in range(n):

        created_at = fake.date_time_between(
            start_date='-1y',
            end_date='now'
        )

        updated_at = fake.date_time_between(
            start_date=created_at,
            end_date='now'
        )

        brand = fake.random_element(list(vehicle_catalog.keys()))
        model = fake.random_element(vehicle_catalog[brand])

        # Generate unique Indian-style registration number
        while True:
            registration_number = (
                random.choice(['KA', 'TN', 'TS', 'MH', 'DL', 'KL', 'PY', 'KA'])
                + fake.numerify('##')
                + fake.lexify('??').upper()
                + fake.numerify('####')
            )

            if registration_number not in registrations:
                registrations.add(registration_number)
                break

        record = {
            'vehicle_id': f'V{1001+i}',
            'customer_id': random.choice(customer_ids),
            'registration_number': registration_number,
            'brand': brand,
            'model': model,
            'battery_capacity': fake.random_int(min=20, max=100),
            'created_at': created_at,
            'updated_at': updated_at
        }

        records.append(record)

    return pd.DataFrame(records)


if __name__ == '__main__':

    customers_df = pd.read_csv('data/generated/customers.csv')

    vehicles_df = generate_vehicles(customers_df)

    vehicles_df.to_csv(
        'data/generated/vehicles.csv',
        index=False
    )
