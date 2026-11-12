from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

PAYMENT_METHODS = [
    'UPI',
    'Credit Card',
    'Debit Card',
    'Net Banking',
    'Wallet'
]


def generate_transactions(sessions_df):

    records = []
    transaction_counter = 100001

    for session in sessions_df.to_dict('records'):

        session_id = session['session_id']
        session_status = session['session_status']
        energy = float(session['energy_consumed_kwh'])

        # Estimate charging cost in INR
        rate_per_kwh = random.uniform(16, 24)
        amount = round(max(energy * rate_per_kwh, 1), 2)

        # Determine initial payment status
        if session_status == 'Completed':
            payment_status = 'Success'
        elif session_status == 'Started':
            payment_status = 'Pending'
        else:
            payment_status = 'Failed'

        payment_method = random.choice(PAYMENT_METHODS)

        # Generate first payment attempt
        transaction_timestamp = (
            session['end_time']
            if session_status == 'Completed'
            else session['updated_at']
        )

        records.append({
            'transaction_id': f'T{transaction_counter}',
            'session_id': session_id,
            'transaction_type': 'Payment',
            'amount': amount,
            'payment_method': payment_method,
            'payment_status': payment_status,
            'transaction_timestamp': transaction_timestamp,
            'created_at': transaction_timestamp,
            'updated_at': transaction_timestamp
        })

        transaction_counter += 1

        # Some completed sessions have failed attempts
        # followed by successful retries
        if (
            session_status == 'Completed'
            and random.random() < 0.15
        ):

            retry_timestamp = (
                session['end_time'] - pd.Timedelta(minutes=2)
            )

            records.append({
                'transaction_id': f'T{transaction_counter}',
                'session_id': session_id,
                'transaction_type': 'Payment',
                'amount': amount,
                'payment_method': payment_method,
                'payment_status': 'Failed',
                'transaction_timestamp': retry_timestamp,
                'created_at': retry_timestamp,
                'updated_at': retry_timestamp
            })

            transaction_counter += 1

        # Refund a small percentage of successful payments
        if (
            session_status == 'Completed'
            and random.random() < 0.03
        ):

            refund_amount = round(
                amount * random.uniform(0.1, 0.5), 2
            )

            refund_timestamp = (
                session['end_time'] + pd.Timedelta(minutes=10)
            )

            records.append({
                'transaction_id': f'T{transaction_counter}',
                'session_id': session_id,
                'transaction_type': 'Refund',
                'amount': refund_amount,
                'payment_method': payment_method,
                'payment_status': 'Success',
                'transaction_timestamp': refund_timestamp,
                'created_at': refund_timestamp,
                'updated_at': refund_timestamp
            })

            transaction_counter += 1

    return pd.DataFrame(records)


if __name__ == '__main__':

    sessions_df = pd.read_csv(
        'data/generated/sessions.csv',
        parse_dates=['start_time', 'end_time', 'created_at', 'updated_at']
    )

    transactions_df = generate_transactions(sessions_df)

    transactions_df.to_csv(
        'data/generated/transactions.csv',
        index=False
    )

    print(transactions_df.head())
    print("Total transactions:", len(transactions_df))

    print("\nTransaction types:")
    print(transactions_df['transaction_type'].value_counts())

    print("\nPayment statuses:")
    print(transactions_df['payment_status'].value_counts())

    print("\nValidation:")
    print("Unique transaction IDs:",
          transactions_df['transaction_id'].nunique())

    print("Valid session references:",
          transactions_df['session_id'].isin(
              sessions_df['session_id']
          ).all())

    print("Null values:")
    print(transactions_df.isnull().sum())

    print("Non-positive amounts:",
          (transactions_df['amount'] <= 0).sum())