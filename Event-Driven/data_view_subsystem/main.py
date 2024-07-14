# from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager
# from client.home_screen import HomeScreen

# class MainApp(App):
#     def build(self):
#         self.manager = ScreenManager()
#         self.manager.add_widget(HomeScreen(name='home'))
#         return self.manager

# if __name__ == '__main__':
#     MainApp().run()

# data_view_subsystem/main.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from client.home_screen import HomeScreen
from client.calendar_view import CalendarView
from client.list_view import ListView
from client.pie_chart_view import PieChartView
from client.timeline_view import TimelineView
from client.json_Handler import load_json_data


class MainApp(App):
    def build(self):
        self.manager = ScreenManager()

        # data = load_json_data()

    

       

        # Create an instance of each view
        # calendar_screen = CalendarView(data, name='calendar')
        # list_screen = ListView(data, name='list')
        # pie_chart_screen = PieChartView(data, name='pie_chart')
        # timeline_screen = TimelineView(data, name='timeline')

        # Add the home screen and other views to the ScreenManager
        # self.manager.add_widget(HomeScreen(name='home'))
        # self.manager.add_widget(calendar_screen)
        # self.manager.add_widget(list_screen)
        # self.manager.add_widget(pie_chart_screen)
        # self.manager.add_widget(timeline_screen)

         # Add screens to the manager with their respective names
        self.manager.add_widget(HomeScreen(name='home'))
        self.manager.add_widget(CalendarView( name='calendar'))        
        self.manager.add_widget(ListView( name='list'))
        self.manager.add_widget(PieChartView(name='pie_chart'))
        self.manager.add_widget(TimelineView(name='timeline'))
        # self.manager.add_widget(TimelineView(json_file_path, name='timeline'))


        return self.manager

if __name__ == '__main__':
    MainApp().run()
