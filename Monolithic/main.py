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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from budget_manager import Budget_Manager

auth = Authenticate()
budget = Budget_Manager
feedback = Feedback("./Data/Feedback")
support = Support("./Data/Support")
globalUsername = None

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
            self.display_message("Registration Successful!", (0, 1, 0, 1))
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
        global globalUsername
        new_username = self.username_input.text
        new_password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        globalUsername = new_username

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

class BudgetScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Create Budget"))

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
        result = budget.add_recurring_payment(payment_data["p_type"], payment_data["amount"], payment_data["t_date"], payment_data["label"], payment_data["recurring_month_number"], payment_data["reminder_days_in_advance"], payment_data["category"])
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
        calendar_btn = Button(text="Calendar View")
        calendar_btn.bind(on_press=lambda x: self.switch_screen('calendar_screen'))
        self.button_layout.add_widget(calendar_btn)

        payment_btn = Button(text="Payment Logger")
        payment_btn.bind(on_press=lambda x: self.switch_screen('payment_screen'))
        self.button_layout.add_widget(payment_btn)

        recurring_payment_btn = Button(text="Recurring Payment")
        recurring_payment_btn.bind(on_press=lambda x: self.switch_screen('recurring_payment_screen'))
        self.button_layout.add_widget(recurring_payment_btn)

        budget_btn = Button(text="Create Budget")
        budget_btn.bind(on_press=lambda x: self.switch_screen('budget_screen'))
        self.button_layout.add_widget(budget_btn)

        feedback_btn = Button(text="Feedback")
        feedback_btn.bind(on_press=lambda x: self.switch_screen('feedback_screen'))
        self.button_layout.add_widget(feedback_btn)

        support_btn = Button(text="Support")
        support_btn.bind(on_press=lambda x: self.switch_screen('support_screen'))
        self.button_layout.add_widget(support_btn)

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name

class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(RegistrationScreen(name='registration_screen'))
        sm.add_widget(SuccessScreen(name='success_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()