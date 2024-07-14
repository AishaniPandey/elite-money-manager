import json
from datetime import datetime
import os
from random import randint

class Feedback:
    def __init__(self, feedback_directory):
        self.feedback_directory = feedback_directory

    def submit_feedback(self, user_name, rating, description):
        
        feedback_data = {
            "userName": user_name,
            "rating": rating,
            "description": description,
            "timeOfRating": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "edited": False
        }

        existing_feedback = self.load_feedback(user_name)
        if existing_feedback:
            existing_feedback["rating"] = rating
            existing_feedback["description"] = description
            existing_feedback["timeOfRating"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            existing_feedback["edited"] = True
        else:
            existing_feedback = feedback_data
            existing_feedback["feedbackId"] = self.generate_feedback_id()
        
        self.save_feedback(user_name, existing_feedback)
        # print(user_name, existing_feedback)

        # Produce message to Kafka topic
        # message = {
        #     "action": "submit_feedback",
        #     "feedback": existing_feedback
        # }
        # self.producer.send_message("feedback_system", message)

    def generate_feedback_id(self):
        # Generate a random feedback ID (You can implement your own logic here)
        return "FB" + str(randint(100000000, 999999999)) + str(datetime.now().timestamp())

    def load_feedback(self, user_name):
        feedback_file = f"{self.feedback_directory}/{user_name}_feedback.json"
        if os.path.exists(feedback_file):
            try:
                with open(feedback_file, "r") as file:
                    feedback_data = json.load(file)
            except FileNotFoundError:
                feedback_data = None
        else:
            feedback_data = None
        return feedback_data

    def save_feedback(self, user_name, feedback_data):
        feedback_file = f"{self.feedback_directory}/{user_name}_feedback.json"
        if not os.path.exists(feedback_file):
            with open(feedback_file, "w") as file:
                json.dump(feedback_data, file)
        else:
            with open(feedback_file, "w") as file:
                json.dump(feedback_data, file)