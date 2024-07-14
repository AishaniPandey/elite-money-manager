import json
import os
import time
import threading
from json_File_Handler import json_File_Handler
from datetime import datetime, timedelta, timezone
from notify import Notify


class Budget_Manager():

    def __init__(self):

        os.makedirs(os.path.dirname("./recurring-payments.json"), exist_ok=True)

        if not os.path.exists("./recurring-payments.json"):
            with open("recurring-payments.json", 'w') as new_file:
                json.dump([], new_file)

        thread = threading.Thread(target=self.remind, args=())
        thread.start()
        


    def compute_remaining_money(self, month):

        incomes = 0
        expenses = 0

        with open('recurring-payments.json', 'r') as file:
            payments = json.load(file)

        for payment in payments:
            
            t_date = datetime.fromtimestamp(payment["t_date"], timezone.utc)
            months_to_days = payment['recurring_month_number'] * 30  # Assuming 30 days per month for simplicity
            new_date = t_date + timedelta(days=months_to_days)

            if new_date.year > t_date.year or new_date.month >= month:
                if payment['p_type'] == 'Credit':
                    incomes += payment['amount']
                elif payment['p_type'] == 'Debit':
                    expenses += payment['amount']


        remaining_money = incomes - expenses
        return remaining_money
    


    def add_recurring_payment(self, p_type, amount, t_date, label, recurring_month_number, reminder_days_in_advance, category):

        if os.path.exists("./recurring-payments.json"):

            recurring_payments_data = {
                "p_type": p_type,
                "amount": amount,
                "t_date": t_date,
                "label": label,
                "recurring_month_number": recurring_month_number,
                "reminder_days_in_advance": reminder_days_in_advance,
                "category": category
            }

            jFH = json_File_Handler()
            jFH.append_To_File("./recurring-payments.json", recurring_payments_data) 
            # logger.log_Message("budget-manager", "INFO", "Recurring-payments added")
            print("Recurring-payments added")
            return True
        


    def remind(self):

        notify = Notify()

        while True:

            current_date = datetime.now()
            print(current_date)
            
            with open('recurring-payments.json', 'r') as file:
                payments = json.load(file)

                for payment in payments:

                    if payment["p_type"] == "Debit":

                        for month in range(1, payment['recurring_month_number']+1):
                            t_date = datetime.fromtimestamp(payment['t_date'])
                            new_date = t_date + timedelta(days=30*month)
                            new_date = t_date - timedelta(days=payment['reminder_days_in_advance'])
                            print(new_date)

                            if new_date.date() == current_date.date() :
                                notify.send_Notification("fornotificationuseseproject3@gmail.com", "REMINDER", f"It's will soon be time to pay for : {payment['label']}")
                                print("Reminder has been sent successfully")

            time.sleep(24 * 3600)

    

processor = Budget_Manager()
month = 4  # Example: April
remaining_money = processor.compute_remaining_money(month)
print(f"Remaining money for month {month}: {remaining_money}")