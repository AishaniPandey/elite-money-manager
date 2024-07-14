from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
import matplotlib.pyplot as plt
import os
from data_view_subsystem.client.custom_button import CustomButton
from collections import defaultdict
import tempfile
from data_view_subsystem.client.json_Handler import load_json_data

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n(Rs. {v:d})'.format(p=pct, v=val)
    return my_autopct

class PieChartView(Screen):

    def create_pie_chart(self, layout, expenses):
        # Filter for expenses and tally by category
        category_totals = defaultdict(float)
        for expense in expenses:
            if expense['p_type'] == 'Debit':
                category_totals[expense['category']] += expense['amount']

        if category_totals:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            fig, ax = plt.subplots()
            # Here we pass the custom autopct function
            ax.pie(amounts, labels=categories, autopct=make_autopct(amounts), startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle
            plt.title('Expenses by Category')
            fig_path = os.path.join(tempfile.gettempdir(), 'pie_chart.png')
            plt.savefig(fig_path, bbox_inches='tight')
            plt.close(fig)
            layout.add_widget(Image(source=fig_path))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        username,data = load_json_data()
        self.name = kwargs.get('name')
        layout = BoxLayout(orientation='vertical')

        back_button = CustomButton(text='Back')
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        expenses = [transaction for transaction in data if transaction['p_type'] == 'Debit']
        self.create_pie_chart(layout, expenses)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
