## This file is the main file that runs the Kivy app. It contains the main class App that is used to run the app. It also contains the SplashScreen class that is used to display the splash screen of the app. The App class also contains the on_start method that is used to add a back button dynamically to screens other than the splash screen. The add_back_button method is used to add the back button to the screen. The go_back method is used to go back to the previous screen when the back button is clicked. The App class also contains the build method that is used to build the app and return the screen manager. The App class also contains the run method that is used to run the app. The if __name__ == '__main__': block is used to run the app when the file is executed.
## kivy-PaymentLogger/src/kapp.py
## Execute this file to run the Kivy app : python kapp.py
# @Author: @Grimoors
# @Date: 2024-04-22
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-20 - 04:56 IST
# @Title: Kivy Payment Logger App
# @Description: A simple Kivy app to log payments manually and automatically

import kivy
from util.logger import Logger

logger = Logger()
originated_from= "Error Originated from file : kapp.py"

try:
    kivy.require('2.3.0')
except Exception as e:
#     print('Kivy version 2.3.0 or higher is required, please upgrade Kivy.')
#     print("Error Originated from file : kapp.py")
#     print('Error:', e)
    e_message = "Kivy version 2.3.0 or higher is required, please upgrade Kivy." + "Error Originated from file : kapp.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

try:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.widget import Widget
    from kivy.uix.screenmanager import ScreenManager
    from kivy.uix.screenmanager import Screen
    from kivy.uix.button import Button
except ImportError as e:
    # print('Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well.')
    # print("Error Originated from file : kapp.py")
    # print('Error:', e)
    e_message = "Kivy is not installed or your imports are wrong, please install Kivy first, check your imports as well." + "Error Originated from file : kapp.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise
except Exception as e:
    # print('An error occurred while importing Kivy modules.')
    # print("Error Originated from file : kapp.py")
    # print('Error:', e)
    e_message = "An error occurred while importing Kivy modules." + "Error Originated from file : kapp.py" + "Error is " + string(e)
    logger.log_Message( "payment-logger", "ERROR",e_message)
    raise

try:
    from paymentlogger import PaymentLoggerScreen, ManuallyLogPaymentScreen, AutoLogPaymentScreen
except ImportError as e:
    # print('PaymentLoggerScreen is not imported, please check your imports.')
    # print("Error Originated from file : kapp.py")
    # print('Error:', e)
    e_message = "PaymentLoggerScreen is not imported, please check your imports." + "Error Originated from file : kapp.py" + "Error is " + string(e)
    logger.log_Message("payment-logger", "ERROR",e_message)
    raise

class SplashScreen(Screen):
    pass




class App(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(PaymentLoggerScreen(name='payment_logger'))
        self.sm.add_widget(ManuallyLogPaymentScreen(name='manually_log_payment'))
        self.sm.add_widget(AutoLogPaymentScreen(name='auto_log_payment'))
        return self.sm
        pass

    def on_start(self):
        # Add a back button dynamically to screens other than the splash screen
        self.sm.bind(current_screen=self.add_back_button)
        pass
    

    def add_back_button(self, instance, value):
        if self.sm.current_screen.name != 'splash':
            back_button = Button(text="Back", size_hint=(None, None), size=(100, 50), pos=(0, 0))
            back_button.bind(on_release=self.go_back)
            if not any(isinstance(w, Button) for w in self.sm.current_screen.children):
                self.sm.current_screen.add_widget(back_button)
                pass
            pass
        pass

    def go_back(self, instance):
        if self.sm.current != 'splash':
            self.sm.current = self.sm.previous()
            pass
        else:
            instance.disabled = True  # Optionally disable the back button on the splash screen
            pass
        pass


    pass


if __name__ == '__main__':
    app = App()
    app.run()
    pass
