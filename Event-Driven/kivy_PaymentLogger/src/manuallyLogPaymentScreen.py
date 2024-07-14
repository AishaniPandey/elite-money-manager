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

    import json
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


class ManuallyLogPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super(ManuallyLogPaymentScreen, self).__init__(**kwargs)
        self.create_ui()
        self.validators = {
            'p_type': PaymentTypeValidation(),
            'label': NonEmptyValidation(),
            'amount': NumericValidation(),
            't_date': NonEmptyValidation(),
            't_id': UPIReferenceValidation()
        }
        self.set_current_time()
        self.date_validator = DateValidation()
        # Implement Monitoring 

    def create_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        back_button = Button(text='Back')
        back_button.bind(on_press=self.go_back)
        self.back_button = back_button  # Storing a reference to the back button

        label = Label(text='Log a Transaction', size_hint_y=None, height=48)
        
        # Creating spinner for payment type
        p_type_spinner = Spinner(
            text='Select Payment Type',
            values=('Credit', 'Debit'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        self.p_type_spinner = p_type_spinner  # Storing a reference to the payment type spinner

        label_input = TextInput(hint_text='Payment Label')
        self.label_input = label_input  # Storing a reference to the label input

        amount_input = TextInput(hint_text='Amount')
        self.amount_input = amount_input  # Storing a reference to the amount input

        # Creating spinners for date and time
        day_spinner = Spinner(text='DD', values=[str(i) for i in range(1, 32)])
        self.day_spinner = day_spinner  # Storing a reference to the day spinner

        month_spinner = Spinner(text='MM', values=[str(i) for i in range(1, 13)])
        self.month_spinner = month_spinner  # Storing a reference to the month spinner
        
        year_spinner = Spinner(text='YYYY', values=[str(i) for i in range(2020, 2031)])
        self.year_spinner = year_spinner  # Storing a reference to the year spinner
        
        hour_spinner = Spinner(text='Hr', values=[str(i) for i in range(0, 24)])
        self.hour_spinner = hour_spinner  # Storing a reference to the hour spinner
        
        minute_spinner = Spinner(text='Min', values=[str(i) for i in range(0, 60)])
        self.minute_spinner = minute_spinner  # Storing a reference to the minute spinner
        
        now_button = Button(text='Now')
        now_button.bind(on_press=self.set_current_time)
        self.now_button = now_button  # Storing a reference to the now button
        
        time_layout = BoxLayout(orientation='horizontal')
        time_layout.add_widget(Label(text='Transaction Time', size_hint_y=None, height=48))
        time_layout.add_widget(day_spinner)
        time_layout.add_widget(month_spinner)
        time_layout.add_widget(year_spinner)
        time_layout.add_widget(hour_spinner)
        time_layout.add_widget(minute_spinner)
        time_layout.add_widget(now_button)
        
        t_id_input = TextInput(hint_text='Transaction ID (12 digit UPI Reference ID)')
        self.t_id_input = t_id_input  # Storing a reference to the transaction ID input
        
        accnt_trace_input = TextInput(hint_text='Account Trace (Optional)')
        self.accnt_trace_input = accnt_trace_input  # Storing a reference to the account trace input
        
        merch_trace_input = TextInput(hint_text='Merchant Trace (Optional)')
        self.merch_trace_input = merch_trace_input  # Storing a reference to the merchant trace input
        
        category_input = TextInput(hint_text='Category (Optional)')
        self.category_input = category_input  # Storing a reference to the category input
        
        
        log_button = Button(text='Log Transaction')
        log_button.bind(on_press=lambda x: self.log_payment(
            p_type_spinner.text, label_input.text, amount_input.text,
            self.get_unix_time(day_spinner.text, month_spinner.text, year_spinner.text, hour_spinner.text, minute_spinner.text),
            self.get_unix_time(day_spinner.text, month_spinner.text, year_spinner.text, hour_spinner.text, minute_spinner.text),
            t_id_input.text, accnt_trace_input.text, merch_trace_input.text, category_input.text
        ))
        self.log_button = log_button  # Storing a reference to the log button

        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(log_button)
        layout.add_widget(p_type_spinner)
        layout.add_widget(label_input)
        layout.add_widget(amount_input)
        layout.add_widget(time_layout)
        layout.add_widget(t_id_input)
        layout.add_widget(category_input)
        layout.add_widget(accnt_trace_input)
        layout.add_widget(merch_trace_input)
        
        
        
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'payment_logger'
        

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
            strategyTransactionCheckSQL = SQLiteCheckTransactionExists("./kivy_PaymentLogger/src/db/payments.db").exists(inputs['t_id'])
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
            invoker.add_command(NotifyThruKafkaCommand(inputs))
            ### Execute the commands
            invoker.execute_commands()
        else:
            toast("Invalid Input")
            print("Invalid Input")
            logger.log_Message("payment-logger", "INFO","Invalid Input")
            #  logger.log_Message("payment-logger", "INFO","Invalid Input")
            logger.log_Message("payment-logger", "INFO", f"The transaction ID is {inputs['t_id']}")
            logger.log_Message("payment-logger", "INFO", f"The transaction label is {inputs['label']}")
            logger.log_Message("payment-logger", "INFO", f"The transaction amount is {inputs['amount']}")
            logger.log_Message("payment-logger", "INFO", f"The transaction date is {inputs['t_date']}")
            logger.log_Message("payment-logger", "INFO", f"The transaction type is {inputs['p_type']}")
            logger.log_Message("payment-logger", "INFO", f"The transaction account trace is {accnt_trace}")
            logger.log_Message("payment-logger", "INFO", f"The transaction merchant trace is {merch_trace}")
            logger.log_Message("payment-logger", "INFO", f"The transaction category is {category}")
            pass
        pass

    def set_current_time(self,*args):
        now = datetime.now()
        self.day_spinner.text = str(now.day)
        self.month_spinner.text = str(now.month)
        self.year_spinner.text = str(now.year)
        self.hour_spinner.text = str(now.hour)
        self.minute_spinner.text = str(now.minute)
        pass

    def get_unix_time(self, day, month, year, hour, minute):
        if self.date_validator.validate(day, month, year):
            dt = datetime(year=int(year), month=int(month), day=int(day),
                          hour=int(hour), minute=int(minute))
            return int(time.mktime(dt.timetuple()))
        else:
            print("Invalid date selected")
            toast("Invalid date selected")
            logger.log_Message("payment-logger", "INFO","Invalid Input Date")
            return None

    pass