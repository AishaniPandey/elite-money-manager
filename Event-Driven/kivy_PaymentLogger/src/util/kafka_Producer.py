#@Author : @YashSampat23154
from kafka import KafkaProducer
import json


# Declaring ip and port of the kafka server that we will use. 
KAFKA_IP = '127.0.0.1'
KAFKA_PORT_NO = '9092'



class kafka_Producer():

    # To create a new producer
    def obtain_producer(self):
        
        producer = None

        try:
            producer = KafkaProducer(bootstrap_servers=[KAFKA_IP + ":" + KAFKA_PORT_NO],api_version=(0, 10, 1))
            
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))

        finally:
            return producer
    
    
    # To send a message using a particular topic
    def send_message (self, kafkaTopicName, message):

        producer = self.obtain_producer()

        try:
            producer.send(kafkaTopicName, json.dumps(message).encode('utf-8'))
            producer.flush()

        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))