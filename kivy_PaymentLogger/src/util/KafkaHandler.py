from util.kafka_Producer import kafka_Producer
from util.logger import Logger

logger = Logger()

class KafkaHandler:
    def __init__(self):
        self.producer = kafka_Producer()
        
    def send_to_kafka(self, data, topic="tcreate"):
        while True:
            try:
                self.producer.send_message(topic, data)
                break

            except Exception as ex:
                logger.log_Message("payment-logger", "ERROR", f'Error while sending payment through kafka: {ex}')
