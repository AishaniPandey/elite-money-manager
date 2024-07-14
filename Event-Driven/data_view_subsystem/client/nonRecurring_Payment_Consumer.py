from kafka import KafkaConsumer


from data_view_subsystem.json_File_Handler import json_File_Handler
import json

KAFKA_IP = '127.0.0.1'
KAFKA_PORT_NO = '9092'

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
            for message in self.consumer:
                messageContents = json.loads(message.value)
                jFH = json_File_Handler().get_instance()
                jFH.append_To_File("data_view_subsystem/data/non-recurring-payments.json", messageContents)
                logger.log_Message("budget-manager", "INFO", "Non-recurring Payment is added to non-recurring-payments.json")

        
        except Exception as ex:
            logger.log_Message("budget-manager", "ERROR", f'Error in reading data from topic tcreate: {ex}')



consumer_instance = nonRecurring_Payment_Consumer()
consumer_instance.consume_data()