from kafka import KafkaConsumer
from logger import Logger
from global_Data import *
from json_File_Handler import json_File_Handler
import json
import os

logger = Logger()

class nonRecurring_Payment_Consumer():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(nonRecurring_Payment_Consumer, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance


    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.consumer = KafkaConsumer("tcreate", bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])


    def consume_data(self): 
        try:

            username_stored_in_json = "./username.json"
            with open(username_stored_in_json, 'r') as file:
                user_info = json.load(file)

            user_name = user_info["userName"]

            feedback_file = f"./Data/Budget/{user_name}_non-recurring-payments.json"

            os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
            if not os.path.exists(feedback_file):
                with open(feedback_file, 'w') as new_file:
                    json.dump([], new_file)

            for message in self.consumer:
                messageContents = json.loads(message.value)
                jFH = json_File_Handler().get_instance()
                jFH.append_To_File(feedback_file, messageContents)
                logger.log_Message("budget-manager", "INFO", "Non-recurring Payment is added to non-recurring-payments.json")

        
        except Exception as ex:
            logger.log_Message("budget-manager", "ERROR", f'Error in reading data from topic tcreate: {ex}')



consumer_instance = nonRecurring_Payment_Consumer()
consumer_instance.consume_data()