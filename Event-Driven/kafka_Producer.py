from kafka import KafkaProducer
import json


# Declaring ip and port of the kafka server that we will use. 
KAFKA_IP = '127.0.0.1'
KAFKA_PORT_NO = '9092'



class kafka_Producer():

    _instance = None

    @staticmethod
    def get_instance():
        if kafka_Producer._instance is None:
            kafka_Producer._instance = KafkaProducer(
                bootstrap_servers=[f"{KAFKA_IP}:{KAFKA_PORT_NO}"],
                api_version=(0, 10, 1)
            )
        return kafka_Producer._instance
    
    
    # To send a message using a particular topic
    def send_message (self, kafkaTopicName, message):

        try:
            producer =  self.get_instance()
            producer.send(kafkaTopicName, json.dumps(message).encode('utf-8'))
            producer.flush()

        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))
