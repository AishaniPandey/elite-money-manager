from kivy_PaymentLogger.src.util.kafka_Producer import kafka_Producer
from kafka import KafkaConsumer
from kivy_PaymentLogger.src.util.global_Data import *
from datetime import datetime
from kivy_PaymentLogger.src.util.json_File_Handler import json_File_Handler
import json
import threading


KAFKA_TOPIC_NAMES = ["log-authentication", "log-budget-manager", "log-data-view", "log-feedback-support", "log-monitoring", "log-notification", "log-payment-logger", "log-test"]


class Logger(): 
       

    def log_Message (self, subsystem_Name, severity, message):

        cur_time = datetime.now()
        
        log_entry = {
            "subsystem_Name" : subsystem_Name,
            "date": cur_time.strftime("%Y-%m-%d"),
            "time": cur_time.strftime("%H:%M:%S"),
            "severity": severity,
            "message": message
        }

        while True:
            try:
                producerForLogging = kafka_Producer()
                producerForLogging.send_message("log-"+ subsystem_Name, log_entry)
                break

            except Exception as ex:
                print(f'Error while producing messages of subsystem {subsystem_Name}: {ex}')



    def log_System (self, kafka_Topic_Name):

        consumer = KafkaConsumer(kafka_Topic_Name, bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])
    
        try:
            for message in consumer:

                messageContents = json.loads(message.value)
                print(messageContents)

                jFH = json_File_Handler()
                jFH.append_To_File("./logs/" + kafka_Topic_Name, messageContents)


        except Exception as ex:
            print(f'Error while consuming messages from topics {kafka_Topic_Name}: {ex}')
        
        

    def start_Logger(self): 
        for topic in KAFKA_TOPIC_NAMES :
            t = threading.Thread(target=self.log_System, args=(topic, ))
            t.start()


if __name__ == '__main__':
    logger = Logger()
    logger.start_Logger()