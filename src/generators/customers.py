
from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

cities = [
    'Bengaluru', 'Chennai', 'Hyderabad', 'Mumbai',
    'Pune', 'Delhi', 'Kochi', 'Mysuru'
]

def generate_customers(n=1000):
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

        record = {
            'customer_id': f'C{1001+i}',
            'customer_name': fake.name(),
            'email': fake.unique.email(),
            'phone': fake.numerify('9#########'),
            'city': random.choice(cities),
            'created_at': created_at,
            'updated_at': updated_at
        }

        records.append(record)

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    customers_df = generate_customers()

    customers_df.to_csv(
    "data/generated/customers.csv",
    index=False
)
