from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from data_view_subsystem.client.json_Handler import load_json_data

class ListView(Screen):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        username,data = load_json_data()
        self.data = data
        self.create_list_view()

    def create_list_view(self):
        sorted_transactions = sorted(self.data, key=lambda x: x['t_date'])
        # main_layout = BoxLayout(orientation='vertical')
        # Sort the transactions by date
        
        # scroll_view = ScrollView(do_scroll_x=False)
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        # This is important to ensure the layout expands to fit content
        list_layout.bind(minimum_height=list_layout.setter('height'))

         # Create and add a 'Back' button at the top
        back_button = Button(text='Back', size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)
        list_layout.add_widget(back_button)
        # main_layout.add_widget(back_button)

        

        for transaction in sorted_transactions:
            # Format the date as a string
            date_str = transaction['t_date'].strftime('%Y-%m-%d')
            trans_str = f"{date_str}: {transaction['label']} - {transaction['p_type']} Rs{transaction['amount']}"
            list_layout.add_widget(Label(text=trans_str, size_hint_y=None, height=30))

        scroll_view = ScrollView(do_scroll_x=False)
        scroll_view.add_widget(list_layout)

        # Add the scroll view to this screen
        self.add_widget(scroll_view)

    def go_back(self, instance):
        # Assuming that 'home' is the name of your main menu screen in the ScreenManager
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'

