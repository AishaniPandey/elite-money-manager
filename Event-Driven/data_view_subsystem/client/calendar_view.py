from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from collections import defaultdict
from datetime import datetime, timedelta
from data_view_subsystem.client.json_Handler import load_json_data

debug = 1 

class CalendarView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        username, data = load_json_data()
        self.data = data
        self.current_date = datetime.now()
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None) 
        self.create_monthly_calendar_view()

    def create_monthly_calendar_view(self):
        self.layout.clear_widgets()  # Clear the current layout
        scroll_view = ScrollView(do_scroll_x=False)
        # scroll_view.add_widget(self.layout)

        self.layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Navigation Buttons
        nav_layout = BoxLayout(size_hint_y=None, height=50)
        prev_button = Button(text='< Previous Month')
        prev_button.bind(on_press=self.go_to_previous_month)
        nav_layout.add_widget(prev_button)

        next_button = Button(text='Next Month >')
        next_button.bind(on_press=self.go_to_next_month)
        nav_layout.add_widget(next_button)

        # Back Button
        back_button = Button(text='Back', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)
        nav_layout.add_widget(back_button)

        self.layout.add_widget(nav_layout)
        # if debug:
        #     print("From File : calendar_view.py", self.current_date)
        #     print("From File : calendar_view.py",self.data)
        
        transactions_by_day = self.group_transactions_by_day(self.data, self.current_date)
        # if debug:
            # print("From File : calendar_view.py , From Function - create-monthly-calendar-view, Printing 'Transactions_by_day, an output of group_transactions_by_day' - ",transactions_by_day)
        # for day in self.get_days_in_month(self.current_date):
        #     day_label = Label(text=day.strftime('%Y-%m-%d'), size_hint_y=None, height=40)
        #     self.layout.add_widget(day_label)
        #     if day in transactions_by_day:
        #         for transaction in transactions_by_day[day]:
        #             trans_label = Label(
        #                 text=f" - {transaction['label']}: ${transaction['amount']} ({'Credit' if transaction['p_type'] == 'Credit' else 'Debit'})",
        #                 size_hint_y=None, height=30)
        #             self.layout.add_widget(trans_label)
        #     else:
        #         no_trans_label = Label(text=" - No transactions", size_hint_y=None, height=30)
        #         self.layout.add_widget(no_trans_label)
        for day in self.get_days_in_month(self.current_date):
            day_label = Label(text=day.strftime('%Y-%m-%d'), size_hint_y=None, height=40)
            self.layout.add_widget(day_label)
            
            # Convert 'day' to a date object for comparison
            day_as_date = day.date()

            if day_as_date in transactions_by_day:
                for transaction in transactions_by_day[day_as_date]:
                    trans_label = Label(
                        text=f" - {transaction['label']}: Rs{transaction['amount']} ({'Credit' if transaction['p_type'] == 'Credit' else 'Debit'})",
                        size_hint_y=None, height=30)
                    self.layout.add_widget(trans_label)
            else:
                no_trans_label = Label(text=" - No transactions", size_hint_y=None, height=30)
                self.layout.add_widget(no_trans_label)

        scroll_view.add_widget(self.layout)
        # self.clear_widgets()
        self.add_widget(scroll_view)

    def get_days_in_month(self, given_date):
        num_days = (datetime(given_date.year, given_date.month + 1, 1) - datetime(given_date.year, given_date.month, 1)).days
        return [datetime(given_date.year, given_date.month, day) for day in range(1, num_days + 1)]
    
    def group_transactions_by_day(self, transactions, given_date):
        transactions_by_day = defaultdict(list)

        for transaction in transactions:
            if isinstance(transaction, dict) and 't_date' in transaction:
                if isinstance(transaction['t_date'], int):
                    # If t_date is an integer, convert from timestamp
                    transaction_date = datetime.utcfromtimestamp(transaction['t_date']).date()
                elif isinstance(transaction['t_date'], datetime):
                    # If t_date is already a datetime object, use it directly
                    transaction_date = transaction['t_date'].date()
                else:
                    raise TypeError(f"Invalid type for 't_date': {type(transaction['t_date'])}")
                
                if transaction_date.month == given_date.month and transaction_date.year == given_date.year:
                    transactions_by_day[transaction_date].append(transaction)
            else:
                raise TypeError(f"Invalid transaction format: {transaction}")

        return transactions_by_day

    
    # def group_transactions_by_day(self, transactions, given_date):
    #     transactions_by_day = defaultdict(list)
    #     for transaction in transactions:
            
    #         # Assuming t_date is a Unix timestamp, convert it to datetime
    #         transaction_date = datetime.utcfromtimestamp(transaction['t_date']).date()
    #         if transaction_date.month == given_date.month and transaction_date.year == given_date.year:
    #             transactions_by_day[transaction_date].append(transaction)
    #     return transactions_by_day



    # def group_transactions_by_day(self, transactions, given_date):
    #     transactions_by_day = defaultdict(list)
    #     for transaction in transactions:
    #         transaction_date = transaction['t_date'].date()
    #         if transaction_date.month == given_date.month and transaction_date.year == given_date.year:
    #             transactions_by_day[transaction_date].append(transaction)
    #     return transactions_by_day

    def go_to_previous_month(self, instance):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.create_monthly_calendar_view()

    def go_to_next_month(self, instance):
        next_month = self.current_date.replace(day=28) + timedelta(days=4)  # This will always jump to the next month
        self.current_date = next_month.replace(day=1)
        self.create_monthly_calendar_view()

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

