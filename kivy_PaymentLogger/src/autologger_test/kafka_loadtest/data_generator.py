import random
import json
import time
from datetime import datetime, timedelta
import argparse

def random_date_in_2024():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    time_between_dates = end_date - start_date
    days_random = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=days_random)
    return int(time.mktime(random_date.timetuple()))

def generate_random_transactions(num_transactions):
    categories = ["FOOD", "MISC", "TECH", "BUSINESS", "MEDICAL", "LOGISTICS", "UTILITIES", "DEBTS"]
    labels = ["Supermarket", "Electronics", "Pharmacy", "Apparel", "Restaurant", "Online Service", "Utility Bill", "Loan Payment"]
    transactions = []

    used_upi_ids = set()

    for _ in range(num_transactions):
        upi_id = str(random.randint(100000000000, 999999999999))
        # Simulate some UPI IDs used twice
        if len(used_upi_ids) < 950:  # First 950 UPIs are unique
            used_upi_ids.add(upi_id)
        elif random.choice([True, False]):  # Next 50 might repeat
            upi_id = random.choice(list(used_upi_ids))

        transaction = {
            "p_type": random.choice(["Credit", "Debit"]),
            "label": random.choice(labels),
            "amount": round(random.uniform(10, 5000), 2),
            "t_date": random_date_in_2024(),
            "t_id": upi_id,
            "accnt_trace": f"AT{random.randint(100000, 999999)}",
            "merch_trace": f"MT{random.randint(100000, 999999)}",
            "category": random.choice(categories)
        }
        transactions.append(transaction)

    return transactions

def save_transactions_to_file(transactions, filename="random_transactions.json"):
    with open(filename, 'w') as f:
        json.dump(transactions, f, indent=4)

if __name__ == "__main__":
    #parse command line arguments - number of transactions = n and filename
    parser = argparse.ArgumentParser(description='Generate random transactions and save them to a JSON file')
    parser.add_argument('-n', type=int, help='Number of transactions to generate')
    parser.add_argument('--filename', type=str, default='random_transactions.json', help='Name of the output JSON file')
    args = parser.parse_args()

    n = args.n
    filename = args.filename

    #example execution
    #python generator.py -n 1000 --filename transactions.json

    # Generate 1000 random transactions
    random_transactions = generate_random_transactions(n)
    # Save them to a JSON file
    save_transactions_to_file(random_transactions, filename)
