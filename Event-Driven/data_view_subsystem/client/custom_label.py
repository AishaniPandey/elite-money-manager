from kivy.uix.label import Label

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 16
        self.color = [0, 0, 0, 1]
