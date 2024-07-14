import json
from datetime import datetime
import os
from random import randint
from logger import Logger
from kafka import KafkaConsumer
from kafka_Producer import kafka_Producer
from global_Data import *
import threading
from monitor import Monitor


logger = Logger()
monitor = Monitor()


class Feedback:

    def __init__(self, feedback_directory):
        self.feedback_directory = feedback_directory
        t = threading.Thread(target=self.process_feedback, args=())
        t.start()
        t1 = threading.Thread(target=monitor.heartbeat_Generator, args=("feedback",))
        t1.start()


    def submit_feedback (self, user_name, rating, description):
        
        feedback_data = {
            "userName": user_name,
            "rating": rating,
            "description": description,
            "timeOfRating": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "edited": False
        }

        while True:
            try:
                producerForLogging = kafka_Producer()
                producerForLogging.send_message("feedback", feedback_data)
                logger.log_Message("feedback-support", "INFO", "Successfully sent feedback by user to the kafka topic feedback")
                break

            except Exception as ex:
                logger.log_Message("feedback-support", "ERROR", f'Error while submitting feedback through kafka: {ex}')



    def process_feedback(self):

        consumer = KafkaConsumer("feedback", bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])

        try:
            for message in consumer:

                messageContents = json.loads(message.value)

                existing_feedback = self.load_feedback(messageContents["userName"])
                if existing_feedback:
                    existing_feedback["rating"] = messageContents["rating"]
                    existing_feedback["description"] = messageContents["description"]
                    existing_feedback["timeOfRating"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    existing_feedback["edited"] = True
                else:
                    existing_feedback = messageContents
                    existing_feedback["feedbackId"] = self.generate_feedback_id()

                self.save_feedback(messageContents["userName"], existing_feedback)

                logger.log_Message("feedback-support", "INFO", f'Feedback for user : {messageContents["userName"]} has been added.')
        
        except Exception as ex:
            logger.log_Message("feedback-support", "ERROR", f'Error in consuming data from topic feedback: {ex}')


    # def submit_feedback(self, user_name, rating, description):
        
    #     feedback_data = {
    #         "userName": user_name,
    #         "rating": rating,
    #         "description": description,
    #         "timeOfRating": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         "edited": False
    #     }

    #     existing_feedback = self.load_feedback(user_name)
    #     if existing_feedback:
    #         existing_feedback["rating"] = rating
    #         existing_feedback["description"] = description
    #         existing_feedback["timeOfRating"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         existing_feedback["edited"] = True
    #     else:
    #         existing_feedback = feedback_data
    #         existing_feedback["feedbackId"] = self.generate_feedback_id()
        
    #     self.save_feedback(user_name, existing_feedback)
    #     print(user_name, existing_feedback)

    def generate_feedback_id(self):
        # Generate a random feedback ID
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

        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        
        if not os.path.exists(feedback_file):
            with open(feedback_file, "w") as file:
                json.dump(feedback_data, file)
        else:
            with open(feedback_file, "w") as file:
                json.dump(feedback_data, file)
