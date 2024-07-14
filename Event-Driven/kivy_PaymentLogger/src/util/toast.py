## util/toast.py
# @Import: util.toast
# @Author: @Grimoors
# @Date: 2024-04-22
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-22 - 16:36 IST
# @Title: Toast Message in Kivy
# @Description: A simple toast message implementation in Kivy

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy_PaymentLogger.src.util.logger import Logger

def toast(text, duration=2):
    logger = Logger()
    # Create the label with your text
    toast = Label(text=text, size_hint=(None, None), size=(Window.width*0.8, 50),
                  pos_hint={'center_x': 0.5, 'center_y': 0.1})
    # Add the label to the current window
    Window.add_widget(toast)
    logger.log_Message("payment-logger", "INFO", "Toast message displayed")
    # Schedule the label's disappearance
    def remove_toast(dt):
        Window.remove_widget(toast)
    
    Clock.schedule_once(remove_toast, duration)
