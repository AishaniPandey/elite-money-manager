from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from authenticate import Authenticate
from feedback import Feedback
from support import Support
from budget_manager import Budget_Manager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from datetime import datetime
import time
import os
import json
from json_File_Handler import json_File_Handler


from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line


# Imports added by aishani for data view subsystem @AishaniPandey
from data_view_subsystem.client.home_screen import HomeScreen
from data_view_subsystem.client.calendar_view import CalendarView
from data_view_subsystem.client.list_view import ListView
from data_view_subsystem.client.pie_chart_view import PieChartView
from data_view_subsystem.client.timeline_view import TimelineView
from data_view_subsystem.client.json_Handler import load_json_data

#End of Imports @AishaniPandey



import string
from kivy_PaymentLogger.src.util.logger import Logger
logger = Logger()
jFH = json_File_Handler().get_instance()

try:
    # from kivy_PaymentLogger.src.paymentlogger import PaymentLoggerScreen, ManuallyLogPaymentScreen, AutoLogPaymentScreen, SplashScreen
    from kivy_PaymentLogger.src.splashScreen import SplashScreen
    from kivy_PaymentLogger.src.manuallyLogPaymentScreen import ManuallyLogPaymentScreen
    from kivy_PaymentLogger.src.paymentLoggerScreen import PaymentLoggerScreen
    from kivy_PaymentLogger.src.autoLogPaymentScreen import AutoLogPaymentScreen
except ImportError as e:
    # print('PaymentLoggerScreen is not imported, please check your imports.')
    # print("Error Originated from file : kapp.py")
    # print('Error:', e)
    e_message = "paymentlogger.py is not imported, please check your imports." + "Error Originated from file : kapp.py" + "Error is " + str(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

# from kivy_garden.star_rating import StarRating  # Importing StarRating from kivy garden


auth = Authenticate()
budget= Budget_Manager("./Data/Budget")
feedback = Feedback("./Data/Feedback")
support = Support("./Data/Support")
globalUsername = None
month = 0
# "./Data/Budget/<userName>_non-recurring-payments.json"
# feedback_file = f"./Data/Budget/{user_name}_non-recurring-payments.json"
# feedback_file = f"./Data/Budget/{user_name['userName']}_non-recurring-payments.json"

user_name, data = load_json_data()
feedback_file = f"./Data/Budget/{user_name}_non-recurring-payments.json"
# print(f"Feedback file for {user_name}: {feedback_file}")



class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.login_button = Button(text='Login', on_press=self.validate_credentials)
        self.register_button = Button(text='Register', on_press=self.switch_to_registration)
        self.message_label = Label(opacity=0)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Login', font_size=30))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        layout.add_widget(self.register_button)
        layout.add_widget(self.message_label)
        
        self.add_widget(layout)


    def validate_credentials(self, instance):
        global globalUsername
        username = self.username_input.text
        password = self.password_input.text

        success = auth.login(username, password)

        if success:
            globalUsername = username

            file_path = "./username.json"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)

            message = {
                    "userName" : globalUsername
            }
            
            with open(file_path, 'w') as json_file:
                json.dump(message, json_file)

            self.display_message("Login Successful!", (0, 1, 0, 1))
            Clock.schedule_once(lambda dt: self.hide_message(success), 2)   
        else:
            self.display_message("Invalid credentials", (1, 0, 0, 1))
            Clock.schedule_once(lambda dt: self.hide_message(success), 2)


    def switch_to_registration(self, instance):
        self.manager.current = 'registration_screen'

    
    def display_message(self, message, color):
        self.message_label.text = message
        self.message_label.color = color
        self.message_label.opacity = 1


    def hide_message(self, success):
        if success: 
            self.manager.current = 'success_screen'
        else: 
            self.message_label.opacity = 0

class RegistrationScreen(Screen):

    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)

        self.username_input = TextInput(hint_text='Enter Username', multiline=False)
        self.password_input = TextInput(hint_text='Enter Password', multiline=False, password=True)
        self.confirm_password_input = TextInput(hint_text='Confirm Password', multiline=False, password=True)
        self.submit_button = Button(text='Submit', on_press=self.register_user)
        self.return_to_login_button = Button(text='Login', on_press=self.switch_to_login)
        self.message_label = Label(opacity=0)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Registration', font_size=30))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_password_input)
        layout.add_widget(self.submit_button)
        layout.add_widget(self.return_to_login_button)
        layout.add_widget(self.message_label)
        
        self.add_widget(layout)


    def switch_to_login(self, instance): 
        self.manager.current = 'login_screen'


    def register_user(self, instance):
        new_username = self.username_input.text
        new_password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        success = auth.register(new_username, new_password, confirm_password)

        if success:
            self.display_message("Registration Successful!", (0, 1, 0, 1))
            Clock.schedule_once(lambda dt: self.hide_message(success), 2)  
        else:
            self.display_message("Error in credentials", (1, 0, 0, 1))
            Clock.schedule_once(lambda dt: self.hide_message(success), 2)  


    def display_message(self, message, color):
        self.message_label.text = message
        self.message_label.color = color
        self.message_label.opacity = 1


    def hide_message(self, success):
        if success:
            self.manager.current = 'login_screen'
        else:
            self.message_label.opacity = 0



# Define screens for financial features
class BaseScreen(Screen):
    pass

class CalendarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Calendar View"))

class PaymentScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Payment Logger"))

class BudgetView(Screen):
    def __init__(self, **kwargs):
        super(BudgetView, self).__init__(**kwargs)
        self.setup_layout()

    def setup_layout(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        # Add/Create Budget Button
        budget_button = Button(text="Add/Create Budget", size_hint=(None, None), size=(200, 50))
        budget_button.bind(on_press=self.go_to_month_screen)
        layout.add_widget(budget_button)

        # Month input
        month_label = Label(text="Enter month (as integer):")
        self.month_input = TextInput(multiline=False)
        layout.add_widget(month_label)
        layout.add_widget(self.month_input)

        # Category dropdown
        category_label = Label(text="Select Category:")
        self.category_spinner = Spinner(
            text='SELECT',
            values=('FOOD', 'MISC', 'TECH', 'BUSINESS', 'MEDICAL', 'BILLS', 'UTILITIES', 'DEBTS', 'SAVINGS')
        )
        layout.add_widget(category_label)
        layout.add_widget(self.category_spinner)

        # Submit button
        submit_button = Button(text="Submit")
        submit_button.bind(on_press=self.calculate_and_show_chart)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def calculate_and_show_chart(self, instance):
        month = int(self.month_input.text)
        category = self.category_spinner.text
        actual_money_spend = budget.actual_Amount_Spend_on_Category(globalUsername, month, category)
        budget1 = budget.get_Budgeted_Value_on_Category(globalUsername, month, category)

        # Calculate percentages
        total = budget1
        used = actual_money_spend
        if total != 0:
            percentage_used = (used / total) * 100
        else:
            percentage_used = 0

        # Show pie chart
        popup = Popup(title='Pie Chart', size_hint=(None, None), size=(400, 400))
        pie_chart = PieChart(size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5}, percentage_used=percentage_used)
        popup.content = pie_chart
        popup.open()

    def go_to_month_screen(self, instance):
        self.manager.current = "month_screen"


class PieChart(Widget):
    def __init__(self,  percentage_used=0, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.percent = percentage_used
        self.red_angle = self.percent * 3.6  # 3.6 degrees per percentage
        self.grey_angle = 360 - self.red_angle
        self.green_color = [0, 1, 0, 1]  # Green color
        self.yellow_color = [1, 1, 0, 1]  # Yellow color
        self.red_color = [1, 0, 0, 1]  # Red color
        self.black_color = [0, 0, 0, 1] # Black color
        self.draw()

    def draw(self):
        with self.canvas:
            if 0 <= self.percent <= 30:
                Color(*self.green_color)
            elif 30 < self.percent <= 70:
                Color(*self.yellow_color)
            else:
                Color(*self.red_color)

            Ellipse(pos=(self.center_x - self.size[0]/2, self.center_y - self.size[1]/2),
                    size=self.size, angle_end=self.red_angle)
            Color(*[0.5, 0.5, 0.5, 1])  # Grey color
            Ellipse(pos=(self.center_x - self.size[0]/2, self.center_y - self.size[1]/2),
                    size=self.size, angle_start=self.red_angle, angle_end=360)
            Line(circle=(self.center_x, self.center_y, self.size[0]/2), width=1.5)
        
        if 0 <= self.percent <= 30:
            label_text = f"{self.percent}% used"
            label_color = self.black_color
        elif 30 < self.percent <= 70:
            label_text = f"{self.percent}% used"
            label_color = self.black_color
        else:
            label_text = f"{self.percent}% used"
            label_color = self.black_color

        label = Label(text=label_text, color=label_color, font_size=20,
                      size_hint=(None, None), size=(self.width, 50),
                      pos=(self.center_x - self.width / 2, self.center_y - 25))
        self.add_widget(label)

class MonthScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Input for month
        month_label = Label(text="Month (as integer)", size_hint_y=None, height=40, color=(0, 0.5, 1, 1))
        self.month_input = TextInput(hint_text="Month", size_hint_y=None, height=40, multiline=False)
        layout.add_widget(month_label)
        layout.add_widget(self.month_input)

        # Submit button for month input
        submit_month_button = Button(text="Submit Month", size_hint_y=None, height=40)
        layout.add_widget(submit_month_button)

        # Add an empty space
        layout.add_widget(Label(size_hint_y=None, height=80))

        submit_month_button.bind(on_press=lambda instance: self.validate_month())

        self.add_widget(layout)

    def validate_month(self):
        global globalUsername
        global month

        try:
            month = int(self.month_input.text)
            remaining_money = budget.compute_remaining_money(globalUsername, month)
            self.show_remaining_message(remaining_money)
        except ValueError:
            popup = Popup(title='Error', content=Label(text='Invalid month input'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def show_remaining_message(self, remaining_money):
        popup = Popup(title='Remaining Money', content=Label(text=f'You have {remaining_money} amount remaining for the month'), size_hint=(None, None), size=(400, 200))
        popup.open()
        # Switch to category screen
        self.manager.current = "budget_screen"


class BudgetScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Input for budget categories
        categories = {
            "FOOD": TextInput(hint_text="Food (0-100)/NA"),
            "MISC": TextInput(hint_text="Misc (0-100)/NA"),
            "TECH": TextInput(hint_text="Tech (0-100)/NA"),
            "BUSINESS": TextInput(hint_text="Business (0-100)/NA"),
            "MEDICAL": TextInput(hint_text="Medical (0-100)/NA"),
            "BILLS": TextInput(hint_text="Bills (0-100)/NA"),
            "UTILITIES": TextInput(hint_text="Utilities (0-100)/NA"),
            "DEBTS": TextInput(hint_text="Debts (0-100)/NA"),
            "SAVINGS": TextInput(hint_text="Savings (0-100)/NA")
        }

        for category, input_field in categories.items():
            layout.add_widget(Label(text=category))
            layout.add_widget(input_field)

        # Submit button
        submit_button = Button(text="Submit", size_hint_y=None, height=40)
        layout.add_widget(submit_button)

        # Add an empty space below the submit button
        layout.add_widget(Label(size_hint_y=None, height=80))

        submit_button.bind(on_press=lambda instance: self.validate_categories(categories))

        self.add_widget(layout)

    def validate_categories(self, categories):
        global month
        total_percentage = 0
        for category, input_field in categories.items():
            try:
                input_text = input_field.text.strip()
                if input_text.upper() == 'NA':
                    continue  # Ignore 'NA' input
                percentage = int(input_text)
                total_percentage += percentage
                if not (0 <= percentage <= 100):
                    raise ValueError("Percentage should be between 0 and 100")
            except ValueError:
                popup = Popup(title='Error', content=Label(text=f'Invalid input for {category}'), size_hint=(None, None), size=(400, 200))
                popup.open()
                return

        if total_percentage > 100:
            popup = Popup(title='Error', content=Label(text='Total percentage should be less than equal 100'), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # # Process the budget data here
        # for category, input_field in categories.items():
        #     input_text = input_field.text.strip()
        #     if input_text.upper() != 'NA':
        #         print(category, ":", input_text)

        budget.create_budget(
            int(month),
            int(categories["FOOD"].text) if categories["FOOD"].text != "NA" else "NA",
            int(categories["MISC"].text) if categories["MISC"].text != "NA" else "NA",
            int(categories["TECH"].text) if categories["TECH"].text != "NA" else "NA",
            int(categories["BUSINESS"].text) if categories["BUSINESS"].text != "NA" else "NA",
            int(categories["MEDICAL"].text) if categories["MEDICAL"].text != "NA" else "NA",
            int(categories["BILLS"].text) if categories["BILLS"].text != "NA" else "NA",
            int(categories["UTILITIES"].text) if categories["UTILITIES"].text != "NA" else "NA",
            int(categories["DEBTS"].text) if categories["DEBTS"].text != "NA" else "NA",
            int(categories["SAVINGS"].text) if categories["SAVINGS"].text != "NA" else "NA"
        )

        # Clear the input fields
        for input_field in categories.values():
            input_field.text = ""
        popup = Popup(title='Success', content=Label(text=f'Budget created'), size_hint=(None, None), size=(400, 200))
        popup.open()




class RecurringPaymentScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Payment Type Dropdown
        self.payment_type_input = Button(text="Payment Type", size_hint=(None, None))
        self.payment_type_dropdown = DropDown()
        self.add_payment_type_options()
        self.payment_type_input.bind(on_release=self.payment_type_dropdown.open)
        self.payment_type_dropdown.bind(on_select=lambda instance, x: setattr(self.payment_type_input, 'text', x))
        
        # Amount Input
        self.amount_input = TextInput(hint_text="Amount", input_type='number')
        
        # Date Input
        self.date_input = TextInput(hint_text="Date (yyyy-mm-dd)")
        
        # Label Input
        self.label_input = TextInput(hint_text="Label")
        
        # Recurring Month Number Input
        self.recurring_month_input = TextInput(hint_text="Recurring Month Number", input_type='number')
        
        # Reminder Days in Advance Input
        self.reminder_days_input = TextInput(hint_text="Reminder Days in Advance", input_type='number')
        
        # Category Dropdown
        self.category_input = Button(text="Category", size_hint=(None, None))
        self.category_dropdown = DropDown()
        self.add_category_options()
        self.category_input.bind(on_release=self.category_dropdown.open)
        self.category_dropdown.bind(on_select=lambda instance, x: setattr(self.category_input, 'text', x))
        
        # Submit Button
        self.submit_button = Button(text="Submit", on_press=self.on_submit)
        
        layout = GridLayout(cols=2)
        layout.add_widget(Label(text="Payment Type"))
        layout.add_widget(self.payment_type_input)
        layout.add_widget(Label(text="Amount"))
        layout.add_widget(self.amount_input)
        layout.add_widget(Label(text="Date (yyyy-mm-dd)"))
        layout.add_widget(self.date_input)
        layout.add_widget(Label(text="Label"))
        layout.add_widget(self.label_input)
        layout.add_widget(Label(text="Recurring Month Number"))
        layout.add_widget(self.recurring_month_input)
        layout.add_widget(Label(text="Reminder Days in Advance"))
        layout.add_widget(self.reminder_days_input)
        layout.add_widget(Label(text="Category"))
        layout.add_widget(self.category_input)
        layout.add_widget(self.submit_button)
        label = Label(text="", size_hint=(1, 5))
        layout.add_widget(label)
        
        self.add_widget(layout)
    
    def add_payment_type_options(self):
        options = ["Credit", "Debit"]
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.payment_type_dropdown.select(btn.text))
            self.payment_type_dropdown.add_widget(btn)
    
    def add_category_options(self):
        categories = ["FOOD", "MISC", "TECH", "BUSINESS", "MEDICAL", "LOGISTICS", "UTILITIES", "DEBTS", "SALARY"]
        for category in categories:
            btn = Button(text=category, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.category_dropdown.select(btn.text))
            self.category_dropdown.add_widget(btn)
    
    def on_submit(self, instance):
        global globalUsername

        payment_data = {
            "p_type": self.payment_type_input.text,
            "amount": float(self.amount_input.text),
            "t_date": self.date_input.text,
            "label": self.label_input.text,
            "recurring_month_number": int(self.recurring_month_input.text),
            "reminder_days_in_advance": int(self.reminder_days_input.text),
            "category": self.category_input.text
        }
        print(payment_data)

        # Form validation checks
        if not all(payment_data.values()):
            self.show_popup("All fields are required")
            return
        
        try:
            amount = int(payment_data["amount"])
            if amount <= 0:
                self.show_popup("Amount must be greater than 0")
                return
        except ValueError:
            self.show_popup("Amount must be a valid number")
            return
        

        try: 
            recurring_month_number = int(payment_data["recurring_month_number"])    
            if recurring_month_number <= 0:
                self.show_popup("Recurring Month Number must be greater than 0")
                return
        except ValueError:
            self.show_popup("Recurring Month Number must be a valid number")
            return
        
        try: 
            reminder_days_in_advance = int(payment_data["reminder_days_in_advance"])
            if reminder_days_in_advance <= 0:
                self.show_popup("Reminder Days in Advance must be greater than 0")
                return
        except ValueError:
            self.show_popup("Reminder Days in Advance must be a valid number")
            return
        
        # Additional validation for date format (YYYY-MM-DD)
        if len(payment_data["t_date"]) != 10 or payment_data["t_date"][4] != '-' or payment_data["t_date"][7] != '-':
            self.show_popup("Date format must be YYYY-MM-DD")
            return
        # check for all fields are non empty 
        # amount, recurring_month_number, reminder_days_in_advance > 0
        # t_date is in format yyyy-mm-dd
        year, month, day = map(int, payment_data['t_date'].split('-'))
        dt = datetime(year=int(year), month=int(month), day=int(day))
        t_date = int(time.mktime(dt.timetuple()))

        result = budget.add_recurring_payment(globalUsername, payment_data["p_type"], payment_data["amount"], t_date, payment_data["label"], payment_data["recurring_month_number"], payment_data["reminder_days_in_advance"], payment_data["category"])

        if result :
            self.show_popup("Recurring payment added successfully")
            self.payment_type_input.text=""
            self.amount_input.text=""
            self.date_input.text=""
            self.label_input.text=""
            self.recurring_month_input.text=""
            self.reminder_days_input.text=""
        else:
            print("Error in adding budget")


    def show_popup(self, message):
        popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

class FeedbackScreen(BaseScreen):
    
    def __init__(self, **kwargs):
        global globalUsername
        super().__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, padding=[40, -20, 40, 100])
        
        # Rating Field
        rating_label = Label(text="Rating:")
        rating_spinner = Spinner(text='1', values=('1', '2', '3', '4', '5'), size_hint=(1, None), height=50)
        layout.add_widget(rating_label)
        layout.add_widget(rating_spinner)

        # Description Field
        description_label = Label(text="Describe your Experience:")
        description_input = TextInput(multiline=True, size_hint=(1, None), height=80)
        layout.add_widget(description_label)
        layout.add_widget(description_input)

        # Submit Feedback ton
        submit_button = Button(text="Submit Feedback", size_hint=(1, None), height=50)
        submit_button.bind(on_press=lambda instance: feedback.submit_feedback(globalUsername, rating_spinner.text, description_input.text))
        layout.add_widget(submit_button)

        self.add_widget(layout)

class SupportScreen(BaseScreen):
    
    def __init__(self, **kwargs):
        global globalUsername
        super().__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=10, padding=[40, -20, 40, 100])

        # Subject Field
        subject_label = Label(text="Subject:")
        subject_input = TextInput(multiline=False, size_hint=(1, None), height=30)
        layout.add_widget(subject_label)
        layout.add_widget(subject_input)

        # Description Field
        description_label = Label(text="Description:")
        description_input = TextInput(multiline=True, size_hint=(1, None), height=80)
        layout.add_widget(description_label)
        layout.add_widget(description_input)

        # Submit Issue Button
        submit_button = Button(text="Submit Issue", size_hint=(1, None), height=50)
        submit_button.bind(on_press=lambda instance: support.submit_issue(globalUsername, subject_input.text, description_input.text))
        layout.add_widget(submit_button)

        self.add_widget(layout)

# Combined SuccessScreen functionality
class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

        # Screen Manager for financial features
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(CalendarScreen(name='calendar_screen'))
        self.screen_manager.add_widget(PaymentScreen(name='payment_screen'))
        self.screen_manager.add_widget(BudgetScreen(name='budget_screen'))
        self.screen_manager.add_widget(RecurringPaymentScreen(name='recurring_payment_screen'))
        self.screen_manager.add_widget(FeedbackScreen(name='feedback_screen'))
        self.screen_manager.add_widget(SupportScreen(name='support_screen'))
        self.screen_manager.add_widget(MonthScreen(name='month_screen'))
        self.screen_manager.add_widget(BudgetView(name='budget_view'))
        
        # Files added for payment logger - Blame @Grimoors
        self.screen_manager.add_widget(SplashScreen(name='splash'))
        self.screen_manager.add_widget(PaymentLoggerScreen(name='payment_logger'))
        self.screen_manager.add_widget(ManuallyLogPaymentScreen(name='manually_log_payment'))
        self.screen_manager.add_widget(AutoLogPaymentScreen(name='auto_log_payment'))
        #End of Blame @Grimoors

        # Files added by aishani for data view subsystem

        self.screen_manager.add_widget(HomeScreen(name='home'))
        self.screen_manager.add_widget(CalendarView( name='calendar'))        
        self.screen_manager.add_widget(ListView( name='list'))
        self.screen_manager.add_widget(PieChartView(name='pie_chart'))
        self.screen_manager.add_widget(TimelineView(name='timeline'))
        #End of Blame @AishaniPandey

        # Button layout for financial features
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.create_buttons()

        # Label for authentication success message
        self.message_label = Label()
        self.add_widget(self.message_label)

        self.add_widget(self.screen_manager)
        self.add_widget(self.button_layout)

    def create_buttons(self):
        # Create and add buttons to the button layout
        calendar_btn = Button(text="Data View Subsystem")
        calendar_btn.bind(on_press=lambda x: self.switch_screen('home'))
        self.button_layout.add_widget(calendar_btn)

        payment_btn = Button(text="Payment Logger")
        payment_btn.bind(on_press=lambda x: self.switch_screen('payment_logger'))
        self.button_layout.add_widget(payment_btn)

        recurring_payment_btn = Button(text="Recurring Payment")
        recurring_payment_btn.bind(on_press=lambda x: self.switch_screen('recurring_payment_screen'))
        self.button_layout.add_widget(recurring_payment_btn)

        budget_btn = Button(text="View Budget")
        budget_btn.bind(on_press=lambda x: self.switch_screen('budget_view'))
        self.button_layout.add_widget(budget_btn)

        feedback_btn = Button(text="Feedback")
        feedback_btn.bind(on_press=lambda x: self.switch_screen('feedback_screen'))
        self.button_layout.add_widget(feedback_btn)

        support_btn = Button(text="Support")
        support_btn.bind(on_press=lambda x: self.switch_screen('support_screen'))
        self.button_layout.add_widget(support_btn)

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name
        # print(f"Screen {screen_name} not found. Available screens: {self.screen_manager.screen_names}")

class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(RegistrationScreen(name='registration_screen'))
        sm.add_widget(SuccessScreen(name='success_screen'))

        # # Files added for payment logger - Blame @Grimoors
        # sm.add_widget(SplashScreen(name='splash'))
        # sm.add_widget(PaymentLoggerScreen(name='payment_logger'))
        # sm.add_widget(ManuallyLogPaymentScreen(name='manually_log_payment'))
        # sm.add_widget(AutoLogPaymentScreen(name='auto_log_payment'))

        # Files added by aishani for data view subsystem @AishaniPandey
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CalendarView( name='calendar'))        
        sm.add_widget(ListView( name='list'))
        sm.add_widget(PieChartView(name='pie_chart'))
        sm.add_widget(TimelineView(name='timeline'))
        #End of Blame @AishaniPandey
        
        self.sm=sm
        return sm

    def submit_issue(self, subject, content):
        global username
        # Retrieve user input for subject and content
        support_screen = self.root.get_screen('support_screen')
        support_screen.submit_issue(username, subject, content)

    def submit_feedback(self, subject, content):
        global username
        # Retrieve user input for subject and content
        support_screen = self.root.get_screen('feedback_screen')
        support_screen.submit_feedback(username, subject, content)

    # def on_start(self):
    #     # Add a back button dynamically to screens other than the splash screen
    #     self.sm.bind(current_screen=self.add_back_button)
    #     pass
    

    # def add_back_button(self, instance, value):
    #     if self.sm.current_screen.name != 'splash':
    #         back_button = Button(text="Back", size_hint=(None, None), size=(100, 50), pos=(0, 0))
    #         back_button.bind(on_release=self.go_back)
    #         if not any(isinstance(w, Button) for w in self.sm.current_screen.children):
    #             self.sm.current_screen.add_widget(back_button)
    #             pass
    #         pass
    #     pass

    # def go_back(self, instance):
    #     if self.sm.current != 'splash':
    #         self.sm.current = self.sm.previous()
    #         pass
    #     else:
    #         instance.disabled = True  # Optionally disable the back button on the splash screen
    #         pass
    #     pass

if __name__ == '__main__':
    MyApp().run()