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
    # from kivy.uix.layout import BoxLayout
    from kivy.uix.screenmanager import Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    import json
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

class PaymentLoggerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_ui()

    def create_ui(self):
        # Main layout container
        layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')

        # Back button with an event to go back to the splash screen
        back_button = Button(text='Back')
        back_button.bind(on_press=self.go_back)

        # Button to manually log a transaction, changes screen on press
        manually_log_button = Button(text='Manually Log Transaction')
        manually_log_button.bind(on_press=self.manually_log)

        # Button to auto log transactions, changes screen on press
        auto_log_button = Button(text='Auto Log Transactions')
        auto_log_button.bind(on_press=self.auto_log)

        # Adding widgets to the layout
        layout.add_widget(back_button)
        layout.add_widget(manually_log_button)
        layout.add_widget(auto_log_button)

        # Add layout to the screen
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def manually_log(self, instance):
        self.manager.current = 'manually_log_payment'

    def auto_log(self, instance):
        self.manager.current = 'auto_log_payment'