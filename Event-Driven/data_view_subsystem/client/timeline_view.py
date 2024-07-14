from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import tempfile
import os
import json

class TimelineView(Screen):
    # def __init__(self, file_path='./data_view_subsystem/data/timeline_entries.json', **kwargs):
    def __init__(self, file_path='./recurring-payments.json', **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
        self.data = self.load_json_data(file_path)
        self.layout = BoxLayout(orientation='vertical')
        self.scroll_view = ScrollView(do_scroll_x=False)
        self.scroll_view.add_widget(self.layout)
        self.create_timeline_view()
        self.add_widget(self.scroll_view)

    def load_json_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        processed_data = []
        for entry in data:
            date = datetime.utcfromtimestamp(entry['t_date'])
            for i in range(entry['recurring_month_number']):
                next_date = date + timedelta(days=i*30)
                processed_data.append({
                    "p_type": entry["p_type"],
                    "label": entry["label"],
                    "amount": entry["amount"],
                    "t_date": next_date,
                    "recurring_month_number": entry["recurring_month_number"]
                })
        processed_data.sort(key=lambda x: x['t_date'])
        return processed_data

    def create_timeline_view(self):
        self.nav_layout = self.create_nav_buttons()
        self.layout.add_widget(self.nav_layout)
        self.update_graph()

    def create_nav_buttons(self):
        
        nav_layout = BoxLayout(size_hint_y=None, height=50 , pos_hint={'top': 1})
        prev_button = Button(text='< Previous Month', size_hint=(0.33, 1), pos_hint={'top': 2})
        prev_button.bind(on_press=self.go_to_previous_month)
        # nav_layout.add_widget(prev_button)

        next_button = Button(text='Next Month >', size_hint=(0.33, 1), pos_hint={'top': 2})
        next_button.bind(on_press=self.go_to_next_month)
        # nav_layout.add_widget(next_button)

        back_button = Button(text='Back', size_hint=(0.33, 1), pos_hint={'top': 2})
        back_button.bind(on_press=self.go_back)
        
        nav_layout.add_widget(prev_button)
        nav_layout.add_widget(next_button)
        nav_layout.add_widget(back_button)

        return nav_layout

    def go_to_previous_month(self, instance):
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.update_graph()

    def go_to_next_month(self, instance):
        self.current_date = (self.current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.update_graph()

    def go_back(self, instance):
        os.remove(self.graph_image.source)
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

    def update_graph(self):
        if hasattr(self, 'graph_image'):
            self.layout.remove_widget(self.graph_image)
        self.graph_image = Image(size_hint_y=0.8)
        temp_filename = self.create_graph_for_month(self.current_date)
        self.graph_image.source = temp_filename
        self.layout.add_widget(self.graph_image, index=1)

    def create_graph_for_month(self, target_date):
        start_date = datetime(target_date.year, target_date.month, 1)
        end_date = (start_date + timedelta(days=31)).replace(day=1)

        filtered_data = [t for t in self.data if start_date <= t['t_date'] < end_date]
        dates = [t['t_date'] for t in filtered_data]
        balances = []
        balance = self.get_starting_balance(start_date)

        for t in filtered_data:
            if t['p_type'] == 'Credit':
                balance += t['amount']
            else:
                balance -= t['amount']
            balances.append(balance)

        plt.figure()
        plt.plot(dates, balances, marker='o')
        plt.title(f'Cash in Hand for {target_date.strftime("%B %Y")}')
        plt.xlabel('Date')
        plt.ylabel('Cash in Hand')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_file.name)
        plt.close()
        return temp_file.name

    def get_starting_balance(self, start_date):
        previous_data = [t for t in self.data if t['t_date'] < start_date]
        balance = 0
        for t in previous_data:
            if t['p_type'] == 'Credit':
                balance += t['amount']
            else:
                balance -= t['amount']
        return balance









# from kivy.uix.screenmanager import Screen
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.image import Image
# from kivy.uix.scrollview import ScrollView
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import json
# import os
# import tempfile
# from collections import defaultdict

# class TimelineView(Screen):
#     def __init__(self, file_path='./data_view_subsystem/data/timeline_entries.json', **kwargs):
#         super().__init__(**kwargs)
#         self.current_date = datetime.now()
#         # self.current_date = datetime.now().date()
#         self.data = self.load_json_data(file_path)
#         self.layout = BoxLayout(orientation='vertical')
#         self.scroll_view = ScrollView(do_scroll_x=False)
#         self.scroll_view.add_widget(self.layout)
#         self.create_timeline_view()
#         self.add_widget(self.scroll_view)

#     def load_json_data(self, file_path):
#         with open(file_path, 'r') as file:
#             data = json.load(file)
#         processed_data = defaultdict(list)
#         for entry in data:
#             date = datetime.utcfromtimestamp(entry['t_date']).date()
#             for i in range(entry['recurring_month_number']):
#                 next_date = date + timedelta(days=i*30)

#                 # processed_data[next_date].append({
#                 #     "p_type": entry["p_type"],
#                 #     "label": entry["label"],
#                 #     "amount": entry["amount"]
#                 # })

#                 processed_data[next_date].append(entry)
#         # print("Loaded Data:", data)  # Debug: Print loaded data
#         # print("Processed Data:", processed_data)  # Debug: Print processed data
#         return processed_data


# #     # def load_json_data(self, file_path):
# #     #     with open(file_path, 'r') as file:
# #     #         data = json.load(file)
# #     #     processed_data = defaultdict(list)
# #     #     for entry in data:
# #     #         date = datetime.utcfromtimestamp(entry['t_date']).date()
# #     #         for i in range(entry['recurring_month_number']):
# #     #             next_date = date + timedelta(days=i*30)
# #     #             processed_data[next_date].append({
# #     #                 "p_type": entry["p_type"],
# #     #                 "label": entry["label"],
# #     #                 "amount": entry["amount"]
# #     #             })
# #     #     print("Processed Data:", processed_data)  # Print processed data
# #     #     return processed_data


# #     # def load_json_data(self, file_path):
# #     #     with open(file_path, 'r') as file:
# #     #         data = json.load(file)
# #     #     processed_data = defaultdict(list)
# #     #     for entry in data:
# #     #         date = datetime.utcfromtimestamp(entry['t_date']).date()
# #     #         for i in range(entry['recurring_month_number']):
# #     #             next_date = date + timedelta(days=i*30)
# #     #             processed_data[next_date].append({
# #     #                 "p_type": entry["p_type"],
# #     #                 "label": entry["label"],
# #     #                 "amount": entry["amount"]
# #     #             })
# #     #     return processed_data

#     def create_timeline_view(self):
#         self.nav_layout = self.create_nav_buttons()
#         self.layout.add_widget(self.nav_layout)
#         self.update_graph()

#     def create_nav_buttons(self):
#         nav_layout = BoxLayout(size_hint_y=None, height=50)
#         prev_button = Button(text='< Previous Month')
#         prev_button.bind(on_press=self.go_to_previous_month)
#         nav_layout.add_widget(prev_button)
#         next_button = Button(text='Next Month >')
#         next_button.bind(on_press=self.go_to_next_month)
#         nav_layout.add_widget(next_button)
#         back_button = Button(text='Back')
#         back_button.bind(on_press=self.go_back)
#         nav_layout.add_widget(back_button)
#         return nav_layout
#         # nav_layout = BoxLayout(size_hint_y=None, height=50)
#         # prev_button = Button(text='< Previous Month', size_hint=(0.33, 1))
#         # prev_button.bind(on_press=self.go_to_previous_month)
#         # nav_layout.add_widget(prev_button)
#         # next_button = Button(text='Next Month >', size_hint=(0.33, 1))
#         # next_button.bind(on_press=self.go_to_next_month)
#         # nav_layout.add_widget(next_button)
#         # back_button = Button(text='Back', size_hint=(0.33, 1))
#         # back_button.bind(on_press=self.go_back)
#         # nav_layout.add_widget(back_button)
#         # return nav_layout

#     def go_to_previous_month(self, instance):
#         self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
#         self.update_graph()

#     def go_to_next_month(self, instance):
#         self.current_date = (self.current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
#         self.update_graph()

#     def go_back(self, instance):
#         if os.path.exists(self.graph_image.source):
#             os.remove(self.graph_image.source)
#         self.manager.transition.direction = 'right'
#         self.manager.current = 'home'

#     # def go_back(self, instance):
#     #     self.manager.transition.direction = 'right'
#     #     self.manager.current = 'home'

#     def update_graph(self):
#         if hasattr(self, 'graph_image'):
#             self.layout.remove_widget(self.graph_image)
#         self.graph_image = Image()
#         temp_filename = self.create_graph_for_month(self.current_date)
#         self.graph_image.source = temp_filename
#         self.layout.add_widget(self.graph_image, index=1)

#     def calculate_cash_in_hand(self):
# #         # Initialize a dictionary to store cash in hand for each day
#         cash_in_hand_dict = defaultdict(float)

# #         # Sort the transactions by date
#         sorted_transactions = sorted(self.data.items(), key=lambda x: x[0])

# #         # Initialize balance
#         balance = 0

# #         # Iterate through each transaction
#         for date, transactions in sorted_transactions:
# #             # Update the balance based on transactions for the current date
#             for transaction in transactions:
#                 if transaction['p_type'] == 'Credit':
#                     balance += transaction['amount']
#                 else:
#                     balance -= transaction['amount']

# #             # Store the cash in hand for the current date
#             cash_in_hand_dict[date] = balance

# #             # Carry forward the balance to the next day
#             cash_in_hand_dict[date + timedelta(days=1)] = balance

# #         # Return the dictionary containing cash in hand for each day
#         return cash_in_hand_dict
    
#     def create_graph_for_month(self, target_date):
#         fig, ax = plt.subplots()
#         plt.title(f'Cash in Hand for {target_date.strftime("%B %Y")}')
#         plt.xlabel('Date')
#         plt.ylabel('Cash in Hand')

# #         # Get the calculated cash in hand data
#         cash_in_hand_dict = self.calculate_cash_in_hand()

# #         # Extract month and year from the target date
#         month = target_date.month
#         year = target_date.year

# #         # Generate date range for the target month
#         start_date = datetime(year, month, 1).date()
#         end_date = start_date + timedelta(days=31)
#         date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]

# #         # Initialize a list to store cash in hand for each day of the month
#         cash_in_hand_month = []

# #         # Iterate through each day of the month and get cash in hand
#         for date in date_range:
#             cash_in_hand_month.append(cash_in_hand_dict.get(date, -1))  # -1 for dates without transactions

# #         # Plot cash in hand for each day of the month
#         ax.plot(date_range, cash_in_hand_month, marker='o', label='Cash in Hand')

# #         # Customize the plot
#         ax.xaxis.set_major_locator(mdates.DayLocator())
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#         plt.xticks(rotation=90)
#         plt.tight_layout()

# #         # Save the plot as an image file
#         temp_file = os.path.join(tempfile.gettempdir(), f'graph_{target_date.strftime("%Y%m%d")}.png')
#         plt.savefig(temp_file)
#         plt.close()

#         return temp_file


# #     # def create_graph_for_month(self, target_date):
# #     #     fig, ax = plt.subplots()
# #     #     plt.title(f'Cash in Hand for {target_date.strftime("%B %Y")}')
# #     #     plt.xlabel('Date')
# #     #     plt.ylabel('Cash in Hand')

# #     #     start_date = datetime(target_date.year, target_date.month, 1).date()
# #     #     end_date = start_date + timedelta(days=31)

# #     #     date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]
# #     #     cash_in_hand = [0] * len(date_range)
# #     #     balance = 0

# #     #     for i, date in enumerate(date_range):
# #     #         if date in self.data:
# #     #             for entry in self.data[date]:
# #     #                 if entry['p_type'] == 'Credit':
# #     #                     balance += entry['amount']
# #     #                 else:
# #     #                     balance -= entry['amount']
# #     #         cash_in_hand[i] = balance

# #         # Print processed data
#         # print("Processed Data for", target_date.strftime("%B %Y"), ":", self.data.get(start_date))
#         # #Print The self.data variable 
#         # print("Print self.data : ",self.data)
#         # # Print cash in hand for each day
#         # print("Cash in Hand for", target_date.strftime("%B %Y"), ":", cash_in_hand)
#         # print(date_range)
#         # print(len(date_range))
#         ax.plot(date_range, cash_in_hand, marker='o', label='Cash in Hand')

#         ax.xaxis.set_major_locator(mdates.DayLocator())
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#         plt.xticks(rotation=90)
#         plt.tight_layout()

#         temp_file = os.path.join(tempfile.gettempdir(), f'graph_{target_date.strftime("%Y%m%d")}.png')
#         plt.savefig(temp_file)
#         plt.close()
#         return temp_file


#     # def create_graph_for_month(self, target_date):
#     #     fig, ax = plt.subplots()
#     #     plt.title(f'Cash in Hand for {target_date.strftime("%B %Y")}')
#     #     plt.xlabel('Date')
#     #     plt.ylabel('Cash in Hand')

#     #     start_date = datetime(target_date.year, target_date.month, 1)
#     #     end_date = start_date + timedelta(days=31)

#     #     date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days)]
#     #     cash_in_hand = [0] * len(date_range)
#     #     balance = 0

#     #     for i, date in enumerate(date_range):
#     #         if date in self.data:
#     #             for entry in self.data[date]:
#     #                 if entry['p_type'] == 'Credit':
#     #                     balance += entry['amount']
#     #                 else:
#     #                     balance -= entry['amount']
#     #         cash_in_hand[i] = balance

#     #     ax.plot(date_range, cash_in_hand, marker='o', label='Cash in Hand')

#     #     ax.xaxis.set_major_locator(mdates.DayLocator())
#     #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#     #     plt.xticks(rotation=90)
#     #     plt.tight_layout()

#     #     temp_file = os.path.join(tempfile.gettempdir(), f'graph_{target_date.strftime("%Y%m%d")}.png')
#     #     plt.savefig(temp_file)
#     #     plt.close()
#     #     return temp_file
