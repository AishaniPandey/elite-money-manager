# import json

# def load_json_data(file_path='data/expenses.json'):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return data


import json
from datetime import datetime
import os

# def load_json_data(file_path='data_view_subsystem/data/random_transactions.json'):
# # # def load_json_data(file_path='data_view_subsystem/data/non-recurring-payments.json'):
# # # def load_json_data(file_path='./kivy_PaymentLogger/src/db/payments.json'):
#     print(os.getcwd())
#     with open(file_path, 'r') as file:
#         data = json.load(file)

#################################333
# def load_json_data(user_name):
#     username_stored_in_json="./username.json"
#     with open(username_stored_in_json, 'r') as file:
#         user_name = json.load(file)

#     # feedback_file = f"./Data/Budget/{user_name["userName"]}_non-recurring-payments.json"
#     feedback_file = f"./Data/Budget/{user_name['userName']}_non-recurring-payments.json"

#     with open(feedback_file, 'r') as file:
#         data = json.load(file)

##############################3

def load_json_data():
    username_stored_in_json = "./username.json"
    with open(username_stored_in_json, 'r') as file:
        user_info = json.load(file)

    user_name = user_info["userName"]

    feedback_file = f"./Data/Budget/{user_name}_non-recurring-payments.json"

    os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
    if not os.path.exists(feedback_file):
        with open(feedback_file, 'w') as new_file:
            json.dump([], new_file)

    with open(feedback_file, 'r') as file:
        data = json.load(file)



    #     # Convert string dates to datetime objects if they are not already.
    #     # Adjust the format '%Y-%m-%d' according to your date format in JSON.
    #     transaction['t_date'] = datetime.strptime(transaction['t_date'], '%Y-%m-%d')
    # return data




    # Convert dates from Unix timestamp to datetime objects
    # for transaction in data:
    #     transaction['t_date'] = datetime.utcfromtimestamp(transaction['t_date'])
    # return data
    # for transaction in data:
    #     transaction['t_date'] = datetime.fromtimestamp(transaction['t_date'])

    if data: 
        for transaction in data:
            if isinstance(transaction.get('t_date'), int):
                transaction['t_date'] = datetime.fromtimestamp(transaction['t_date'])
            elif isinstance(transaction.get('t_date'), str):
                transaction['t_date'] = datetime.strptime(transaction['t_date'], "%Y-%m-%d %H:%M:%S")
            else:
                raise TypeError(f"Invalid type for 't_date': {type(transaction['t_date'])}")
    
    return user_name, data

