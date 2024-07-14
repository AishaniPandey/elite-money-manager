import json
import os
import time
import threading
from logger import Logger
from json_File_Handler import json_File_Handler
from datetime import datetime, timedelta, timezone
from notify import Notify
from monitor import Monitor

logger = Logger()
monitor = Monitor()

class Budget_Manager():

    def __init__(self, feedback_directory):

        self.feedback_directory = feedback_directory
        thread = threading.Thread(target=self.remind, args=())
        thread.start()
        t = threading.Thread(target=monitor.heartbeat_Generator, args=("budget-manager",))
        t.start()
        


    def remind(self):

        notify = Notify()

        while True:

            current_date = datetime.now()

            user_files = [f for f in os.listdir(self.feedback_directory) if f.endswith("_recurring-payments.json")]

            for user_file in user_files:

                with open(os.path.join(self.feedback_directory, user_file), 'r') as file:
            
                    payments = json.load(file)

                    for payment in payments:

                        if payment["p_type"] == "Debit":

                            for month in range(1, payment['recurring_month_number']+1):
                                t_date = datetime.fromtimestamp(payment['t_date'])
                                new_date = t_date + timedelta(days=30*month) # Assuming 30 days per month for simplicity
                                new_date = t_date - timedelta(days=payment['reminder_days_in_advance'])

                                if new_date.date() == current_date.date() :
                                    notify.send_Notification("fornotificationuseseproject3@gmail.com", "REMINDER", f"It's will soon be time to pay for : {payment['label']}")
                                    logger.log_Message("budget-manager", "INFO", "Reminder has been sent successfully")
                                    print("Reminder has been sent successfully")

            time.sleep(24 * 3600)




    def add_recurring_payment(self, user_name, p_type, amount, t_date, label, recurring_month_number, reminder_days_in_advance, category):

        file_path = f"{self.feedback_directory}/{user_name}_recurring-payments.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        if os.path.exists(file_path):

            recurring_payments_data = {
                "p_type": p_type,
                "amount": amount,
                "t_date": t_date,
                "label": label,
                "recurring_month_number": recurring_month_number,
                "reminder_days_in_advance": reminder_days_in_advance,
                "category": category
            }

            jFH = json_File_Handler().get_instance()
            jFH.append_To_File(file_path, recurring_payments_data) 
            logger.log_Message("budget-manager", "INFO", "Recurring-payments added")
            # print("Recurring-payments added")
            return True



    def compute_remaining_money(self, user_name, month):

        file_path = f"{self.feedback_directory}/{user_name}_recurring-payments.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        incomes = 0
        expenses = 0

        with open(file_path, 'r') as file:
            payments = json.load(file)

        for payment in payments:
            
            t_date = datetime.fromtimestamp(payment["t_date"], timezone.utc)
            months_to_days = payment['recurring_month_number'] * 30  # Assuming 30 days per month for simplicity
            new_date = t_date + timedelta(days=months_to_days)

            # print("t_date:")
            # print(t_date)
            # print("new_date:")
            # print(new_date)
            # print("")

            if new_date.year > t_date.year or new_date.month >= month and month >= t_date.month:
                if payment['p_type'] == 'Credit':
                    incomes += payment['amount']
                elif payment['p_type'] == 'Debit':
                    expenses += payment['amount']

        remaining_money = incomes - expenses
        return remaining_money
          
    

    def create_budget(self, user_name, month, food = "NA", misc = "NA", tech = "NA" , business = "NA", medical = "NA", bills = "NA", utilities = "NA", debts = "NA", savings = "NA"):

        file_path = f"{self.feedback_directory}/{user_name}_budget-on-categories.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        budget_data = []
        existing_entry_index = None
        for index, entry in enumerate(budget_data):
            if entry["month"] == month:
                existing_entry_index = index
                break

        # Convert 'NA' values to None to handle them properly
        if food == "NA":
            food = None
        if misc == "NA":
            misc = None
        if tech == "NA":
            tech = None
        if business == "NA":
            business = None
        if medical == "NA":
            medical = None
        if bills == "NA":
            bills = None
        if utilities == "NA":
            utilities = None
        if debts == "NA":
            debts = None
        if savings == "NA":
            savings = None

        new_entry = {
            "month": month,
            "FOOD": food,
            "MISC": misc,
            "TECH": tech,
            "BUSINESS": business,
            "MEDICAL": medical,
            "BILLS": bills,
            "UTILITIES": utilities,
            "DEBTS": debts,
            "SAVINGS": savings
        }

        if existing_entry_index is not None:
            budget_data[existing_entry_index] = new_entry
        else:
            budget_data.append(new_entry)

        with open(file_path, 'w') as file:
            json.dump(budget_data, file, indent=4)


    def actual_Amount_Spend_on_Category(self, user_name, check_month, category):

        file_path = f"{self.feedback_directory}/{user_name}_non-recurring-payments.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        actual_Amount_Spend = 0
        
        with open(file_path, 'r') as file:
            payments = json.load(file)

        for payment in payments:
            
            t_date = datetime.fromtimestamp(payment["t_date"], timezone.utc)

            if t_date.month == month and payment['p_type'] == 'Debit' and payment['category'] == category:
                actual_Amount_Spend += payment['amount']

        file_path = f"{self.feedback_directory}/{user_name}_recurring-payments.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        with open(file_path, 'r') as file:
            payments = json.load(file)

        for payment in payments:

            if payment["p_type"] == "Debit":
                
                for month in range(1, payment['recurring_month_number']+1):
                    t_date = datetime.fromtimestamp(payment['t_date'])
                    new_date = t_date + timedelta(days=30*month) # Assuming 30 days per month for simplicity

                    if new_date.month == check_month and payment['category'] == category:
                        actual_Amount_Spend += payment['amount']

        return actual_Amount_Spend 



    def get_Budgeted_Value_on_Category(self, user_name, month, category):

        remaining_Amount = self.compute_remaining_money(user_name, month)

        file_path = f"{self.feedback_directory}/{user_name}_budget-on-categories.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as new_file:
                json.dump([], new_file)

        with open(file_path, 'r') as file:
            budget_data = json.load(file)

            for entry in budget_data:

                if entry["month"] == month:
                
                    if entry[category] == None:
                        return 0
                    else:
                        return remaining_Amount * (entry[category] / 100)
                        
            return 0  


    def difference_budgetedValue_ActualSpending(self, user_name, month, category): 
        actual_Amount = self.actual_Amount_Spend_on_Category(user_name, month, category)
        budgeted_Amount = self.get_Budgeted_Value_on_Category(user_name, month, category)
        return budgeted_Amount-actual_Amount

    

# processor = Budget_Manager()
# month = 3 
# remaining_money = processor.compute_remaining_money(month)
# actual_money_spend = processor.actual_Amount_Spend_on_Category(5, "FOOD")
# budget = processor.get_Budgeted_Value_on_Category(5, "FOOD")
# print(remaining_money)
# print(actual_money_spend)
# print(budget)