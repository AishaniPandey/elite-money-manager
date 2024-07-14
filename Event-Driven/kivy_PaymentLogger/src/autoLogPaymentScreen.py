import kivy
import time
from datetime import datetime
import json
import kivy_PaymentLogger.src.util.logger

logger = kivy_PaymentLogger.src.util.logger.Logger()


try:
    kivy.require('2.3.0')
except Exception as e:
    # print('Kivy version 2.3.0 or higher is required, please upgrade Kivy.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Kivy version 2.3.0 or higher is required, please upgrade Kivy." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try:
    from kivy.uix.screenmanager import Screen
    from kivy.lang import Builder
    from kivy.uix.button import Button
    from kivy.uix.screenmanager import Screen
    from kivy.lang import Builder
    from kivy.uix.button import Button
    from kivy.uix.screenmanager import Screen
    from kivy.lang import Builder
    from kivy.uix.button import Button
    # from kivy.uix.layout import BoxLayout
    from kivy.uix.screenmanager import Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    # from kivy.uix.screen import Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.spinner import Spinner
    from datetime import datetime
    import time
except ImportError as e:
    # print('Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)  
    e_message = "Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try:
    Builder.load_file('kivy_PaymentLogger/src/paymentforms.kv')
    from kivy_PaymentLogger.src.util.toast import toast
except Exception as e:
    e_message = "An error occurred while loading the KV file." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    # print('An error occurred while loading the KV file.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try: 
    from kivy_PaymentLogger.src.designpatterns.strategyValidation import NonEmptyValidation, NumericValidation, DateValidation, PaymentTypeValidation, UPIReferenceValidation
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise



try:
    from kivy_PaymentLogger.src.designpatterns.commandDatabaseUpdater import Invoker, Command, UpdateSQLiteCommand, UpdateJsonCommand, NotifyThruKafkaCommand
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)

    raise


try:
    from kivy_PaymentLogger.src.designpatterns.strategyTransactionCheck import JSONCheckTransactionExists, SQLiteCheckTransactionExists, CheckTransactionExistsStrategy
except ImportError as e:
    # print('Design patterns are not imported, please check your imports.')
    # print("Error Originated from file : paymentlogger.py")
    # print('Error:', e)
    e_message = "Design patterns are not imported, please check your imports." + "Error Originated from file : paymentlogger.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

##Global Variable; Bad Practice; to be Deprecated later
json_path = 'kivy_PaymentLogger/src/db/payments.json'


class AutoLogPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super(AutoLogPaymentScreen, self).__init__(**kwargs)
        self.create_ui()

    def create_ui(self):
        layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')

        # Back Button
        back_button = Button(text='Back')
        back_button.bind(on_press=self.go_back)

        # Label for the screen
        label = Label(text='Log a Transaction', size_hint_y=None, height='48dp')

        # Text input for transaction file path
        self.transaction_file_path_input = TextInput(hint_text='Path to Json File of Transactions')

        # Button to initiate logging of transactions
        log_transactions_button = Button(text='Log Transaction(s)')
        log_transactions_button.bind(on_press=self.on_log_transactions_pressed)

        # Add widgets to the layout
        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(self.transaction_file_path_input)
        layout.add_widget(log_transactions_button)

        self.add_widget(layout)
        

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def on_log_transactions_pressed(self, instance):
        self.auto_log_payment(self.transaction_file_path_input.text)

    def auto_log_payment(self, transaction_file_path):
        # Load transactions from the specified JSON file
        try:
            with open(transaction_file_path, 'r') as file:
                transactions = json.load(file)
                toast(f"Loaded {len(transactions)} transactions from file.")
            for transaction in transactions:
                self.log_payment(transaction)
        except Exception as e:
            errorstring = str(e)
            print(f"Error loading or processing transactions: {errorstring}")
            toast(f"Error processing transactions: {errorstring}")

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
        db_path = './kivy_PaymentLogger/src/db/payments.db'
        json_path = './kivy_PaymentLogger/src/db/payments.json'
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