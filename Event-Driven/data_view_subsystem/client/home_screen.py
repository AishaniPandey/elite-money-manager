# from kivy.uix.screenmanager import Screen
# from client.calendar_view import CalendarView
# from client.list_view import ListView
# from client.pie_chart_view import PieChartView
# from client.timeline_view import TimelineView
# # from client.json_handler import load_json_data
# from client.json_Handler import load_json_data

# class HomeScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         data = load_json_data()
#         self.add_widget(CalendarView(data))
#         self.add_widget(ListView(data))
#         self.add_widget(PieChartView(data))
#         self.add_widget(TimelineView(data))

# data_view_subsystem/client/home_screen.py

from kivy.uix.screenmanager import Screen
from data_view_subsystem.client.custom_button import CustomButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from monitor import Monitor
import threading


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Buttons to navigate to each view
        btn_calendar = CustomButton(text='Calendar View')
        btn_list = CustomButton(text='List View')
        btn_pie_chart = CustomButton(text='Pie Chart View')
        btn_timeline = CustomButton(text='Timeline View')
        welcome_splash = Label (text=" Welcome to thee Data View Subsystem", color="white")
            
        # Bind the buttons to switch to the respective screens
        btn_calendar.bind(on_press=self.switch_to_calendar)
        btn_list.bind(on_press=self.switch_to_list)
        btn_pie_chart.bind(on_press=self.switch_to_pie_chart)
        btn_timeline.bind(on_press=self.switch_to_timeline)

        layout.add_widget(btn_calendar)
        layout.add_widget(btn_list)
        layout.add_widget(btn_pie_chart)
        layout.add_widget(btn_timeline)
        layout.add_widget(welcome_splash)

        self.add_widget(layout)

        monitor = Monitor()
        t_Standard = threading.Thread(target=monitor.heartbeat_Generator, args=("home_screen", ))
        t_Standard.start()

    def switch_to_calendar(self, instance):
        self.manager.current = 'calendar'

    def switch_to_list(self, instance):
        self.manager.current = 'list'

    def switch_to_pie_chart(self, instance):
        self.manager.current = 'pie_chart'

    def switch_to_timeline(self, instance):
        self.manager.current = 'timeline'

