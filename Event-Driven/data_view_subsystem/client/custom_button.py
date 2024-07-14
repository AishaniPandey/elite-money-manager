# from kivy.uix.button import Button

# class CustomButton(Button):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.size_hint = (0.3, 0.1)
#         self.font_size = 14

# client/custom_button.py

from kivy.uix.button import Button

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = '48dp'  # Assuming you have a 'dp' method available
        self.font_size = '16sp'
