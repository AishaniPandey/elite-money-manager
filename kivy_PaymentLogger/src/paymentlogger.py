## src/paymentlogger.py
# @Import : paymentlogger
# @Author: @Grimoors
# @Date: 2024-04-20
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-22 - 16:56 IST
# @Title: Payment Logger
# @Description: A simple payment logger to log payments manually and automatically




import kivy
import time
from datetime import datetime
import json
import util.logger

logger = util.logger.Logger()


try:
    kivy.require('2.3.0')
except Exception as e:
    # print('Kivy version 2.3.0 or higher is required, please upgrade Kivy.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Kivy version 2.3.0 or higher is required, please upgrade Kivy." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try:
    from kivy.uix.screenmanager import Screen
    from kivy.lang import Builder
except ImportError as e:
    # print('Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)  
    e_message = "Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try:
    Builder.load_file('paymentforms.kv')
    from util.toast import toast
except Exception as e:
    e_message = "An error occurred while loading the KV file." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    # print('An error occurred while loading the KV file.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try: 
    from designpatterns.strategyValidation import NonEmptyValidation, NumericValidation, DateValidation, PaymentTypeValidation, UPIReferenceValidation
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise



try:
    from designpatterns.commandDatabaseUpdater import Invoker, Command, UpdateSQLiteCommand, UpdateJsonCommand, NotifyThruKafkaCommand
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)

    raise


try:
    from designpatterns.strategyTransactionCheck import JSONCheckTransactionExists, SQLiteCheckTransactionExists, CheckTransactionExistsStrategy
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

##Global Variable; Bad Practice; to be Deprecated later
json_path = 'db/payments.json'

class PaymentLoggerScreen(Screen):

    def __init__(self, **kwargs):
        super(PaymentLoggerScreen, self).__init__(**kwargs)
        # self.auto_log_payment()



class ManuallyLogPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators = {
            'p_type': PaymentTypeValidation(),
            'label': NonEmptyValidation(),
            'amount': NumericValidation(),
            't_date': NonEmptyValidation(),
            't_id': UPIReferenceValidation()
        }
        self.set_current_time()
        self.date_validator = DateValidation()


    def log_payment(self, p_type, label, amount, t_date, unix_time, t_id, accnt_trace=None, merch_trace=None, category=None):
        # This function will log the payment to the database
        inputs = {'p_type': p_type, 'label': label, 'amount': amount, 't_date': unix_time, 't_id': t_id}
        if all(self.validators[key].validate(value) for key, value in inputs.items()) and unix_time is not None:
            print(f"Logging payment: {label} of {amount} on {t_date}")
            print(f"Logging payment: {label} of {amount} on {unix_time}")
            print("Valid Input")
            logger.log_Message("payment-logger", "INFO",f"Logging payment: {label} of {amount} on {t_date} at {unix_time}")
            inputs['amount'] = float(amount)
            inputs['t_id']= float(t_id)
            inputs['accnt_trace'] = accnt_trace
            inputs['merch_trace'] = merch_trace 
            inputs['category']= category
            # Implement Transaction Check here
            ## Implement the Strategy Design Pattern here
            ### Declare a CheckTransactionExistsStrategy object
            strategyTransactionCheckSQL = SQLiteCheckTransactionExists("./db/payments.db").exists(inputs['t_id'])
            strategyTransactionCheckJSON = JSONCheckTransactionExists(json_path).exists(inputs['t_id'])
            
            if strategyTransactionCheckSQL or strategyTransactionCheckJSON:
                print("Transaction already exists")
                logger.log_Message("payment-logger", "INFO","Transaction already exists")
                toast("Transaction already exists")
                return

            # ### Add the JSONCheckTransactionExists to the strategyTransactionCheck



            # Implement actual database logging here
            ## Implement the Command Design Pattern here
            ### Declare an Invoker object
            invoker = Invoker()
            # ### Add the UpdateSQLiteCommand to the invoker
            invoker.add_command(UpdateSQLiteCommand(inputs))
            ### Add the UpdateJsonCommand to the invoker
            invoker.add_command(UpdateJsonCommand(inputs, json_path))
            invoker.add_command(NotifyThruKafkaCommand(transaction))
            ### Execute the commands
            invoker.execute_commands()
        else:
            toast("Invalid Input")
            print("Invalid Input")
            logger.log_Message("payment-logger", "INFO","Invalid Input")
            pass
        pass

    def set_current_time(self):
        now = datetime.now()
        self.ids.day.text = str(now.day)
        self.ids.month.text = str(now.month)
        self.ids.year.text = str(now.year)
        self.ids.hour.text = str(now.hour)
        self.ids.minute.text = str(now.minute)
        pass

    def get_unix_time(self, day, month, year, hour, minute):
        if self.date_validator.validate(day, month, year):
            dt = datetime(year=int(year), month=int(month), day=int(day),
                          hour=int(hour), minute=int(minute))
            return int(time.mktime(dt.timetuple()))
        else:
            print("Invalid date selected")
            toast("Invalid date selected")
            KafkaHandler().send_to_kafka("Invalid date selected")
            return None

    pass


# class AutoLogPaymentScreen(Screen):

#     def auto_log_payment(self, *args, **kwargs):
#         # This function could retrieve transactions from an API or a scheduled job
#         print("Automatically logging periodic transactions.")
#         # Implement automatic logging logic here
#     pass

class AutoLogPaymentScreen(Screen):
    def auto_log_payment(self, transaction_file_path):
        # Load transactions from the specified JSON file
        try:
            with open(transaction_file_path, 'r') as file:
                transactions = json.load(file)
            for transaction in transactions:
                self.log_payment(transaction)
        except Exception as e:
            print(f"Error loading or processing transactions: {str(e)}")
            toast("Error processing transactions")

    def log_payment(self, transaction):
        # Extract transaction details
        p_type = transaction.get('p_type')
        label = transaction.get('label')
        amount = transaction.get('amount')
        t_date = transaction.get('t_date')
        t_id = transaction.get('t_id')
        accnt_trace = transaction.get('accnt_trace', None)
        merch_trace = transaction.get('merch_trace', None)
        category = transaction.get('category', None)

        # Validate transaction details
        validators = {
            'p_type': PaymentTypeValidation(),
            'label': NonEmptyValidation(),
            'amount': NumericValidation(),
            't_date': NonEmptyValidation(),  # Assuming t_date is a string and valid
            't_id': UPIReferenceValidation()  # Validate UPI reference ID format
        }

        valid = all(validator.validate(transaction[key]) for key, validator in validators.items() if key in transaction)
        if not valid:
            toast(f"Invalid data for transaction ID {t_id}")
            print(f"Invalid data for transaction ID {t_id}")
            logger.log_Message("payment-logger", "INFO",f"Invalid data for transaction ID {t_id}")
            return

        # Check if transaction already exists
        db_path = './db/payments.db'
        json_path = './db/payments.json'
        if SQLiteCheckTransactionExists(db_path).exists(t_id) or JSONCheckTransactionExists(json_path).exists(t_id):
            toast(f"Transaction with ID {t_id} already exists.")
            print(f"Transaction with ID {t_id} already exists.")
            logger.log_Message("payment-logger", "INFO",f"Transaction with ID {t_id} already exists.")

            return

        # Log the transaction
        print(f"Automatically logging payment: {label} of {amount} on {t_date}")
        logger.log_Message("payment-logger", "INFO",f"Automatically logging payment: {label} of {amount} on {t_date}")
        # Implement actual database and JSON logging here
        invoker = Invoker()
        invoker.add_command(UpdateSQLiteCommand(transaction))
        invoker.add_command(UpdateJsonCommand(transaction, json_path))
        invoker.add_command(NotifyThruKafkaCommand(transaction))
        invoker.execute_commands()

        toast("Transaction logged successfully.")
        print("Transaction logged successfully.")
        logger.log_Message("payment-logger", "INFO","Transaction logged successfully.")