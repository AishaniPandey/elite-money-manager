from kivy.uix.screenmanager import Screen
from data_view_subsystem.client.logger import Logger
from data_view_subsystem.client.global_Data import *
from data_view_subsystem.client.nonRecurring_Payment_Consumer import nonRecurring_Payment_Consumer

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = Logger()
        self.consumer_instance = nonRecurring_Payment_Consumer()
        self.consumer_instance.consume_data()

