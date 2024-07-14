from kafka_Producer import kafka_Producer
from kafka import KafkaConsumer
from global_Data import *
from time import time, sleep
import threading
import json
from logger import Logger
from notify import Notify
from json_File_Handler import *


logger = Logger()
jFH = json_File_Handler().get_instance()
notify = Notify()


KAFKA_TOPIC_NAMES = ["monitor-authentication", "monitor-budget-manager", "monitor-data-view", "monitor-feedback", "monitor-support", "monitor-monitoring", "monitor-notification", "monitor-payment-logger", "monitor-test"]


class Monitor():

    def __init__(self):
        t = threading.Thread(target=self.heartbeat_Generator, args=("monitoring",))
        t.start()
    
    # Send a heartbeat every 60 seconds
    def heartbeat_Generator(self, subsystem_Name):

        while True:

            try:

                heartbeat = {
                    "subsystem_Name" : subsystem_Name,
                    "current_Time" : time()
                }

                producerForLogging = kafka_Producer()
                producerForLogging.send_message("monitor-"+ subsystem_Name, heartbeat)
    

            except Exception as ex:
                logger.log_Message("monitoring", "ERROR", f'Error while generating heartbeat of subsystem {subsystem_Name}: {ex}')

            sleep(30)



    def alerted_Monitoring(self): 

        try : 

            while (True):
                    
                # Send a notification to admin when heartbeat time exceeds 300
                remove_From_Alert_Monitoring = []
                current_Time = time()

                if os.path.exists("./monitoring/alerted_Monitoring.json"):

                    with open("./monitoring/alerted_Monitoring.json", 'r') as file:
                        file_content = file.read().strip()

                        data = json.loads(file_content) if file_content else []

                        for entry in data:
                            if current_Time - entry['current_Time'] >= 300:
                                remove_From_Alert_Monitoring.append(entry)

                    
                    for entry in remove_From_Alert_Monitoring:
                        jFH.delete_From_File("./monitoring/alerted_Monitoring.json", entry["subsystem_Name"])
                        notify.send_Notification("fornotificationuseseproject3@gmail.com", "ERROR in subsystem", f'{entry["subsystem_Name"]} is not working properly. Kindly take some action to ensure proper functioning of the application.')
                        logger.log_Message("monitoring", "INFO", f'Subsystem {entry["subsystem_Name"]} has stopped sending its heartbeat. Alerted Admin')

                    

                else:
                    os.makedirs(os.path.dirname("./monitoring/alerted_Monitoring.json"), exist_ok=True)
                    if not os.path.exists("./monitoring/alerted_Monitoring.json"):
                        with open("./monitoring/alerted_Monitoring.json", 'w') as new_file:
                            json.dump([], new_file)

                sleep(30)


        except Exception as ex:
            logger.log_Message("monitoring", "ERROR", f'Error in standard_Monitoring: {ex}')




    def standard_Monitoring(self): 
        
        try : 

            while (True):
                    
                # Add entry to alerted_Monitoring.json when heartbeat time exceeds 150
                remove_From_Stand_Monitoring = []
                current_Time = time()

                if os.path.exists("./monitoring/standard_Monitoring.json"):

                    with open("./monitoring/standard_Monitoring.json", 'r') as file:
                        file_content = file.read().strip()

                        data = json.loads(file_content) if file_content else []

                        for entry in data:
                            if current_Time - entry['current_Time'] >= 150:
                                remove_From_Stand_Monitoring.append(entry)


                    for entry in remove_From_Stand_Monitoring:
                        jFH.delete_From_File("./monitoring/standard_Monitoring.json", entry["subsystem_Name"])
                        logger.log_Message("monitoring", "INFO", f'Removed {entry["subsystem_Name"]} from Standard Monitoring')
                    

                    for entry in remove_From_Stand_Monitoring:
                        jFH.append_To_File("./monitoring/alerted_Monitoring.json", entry)
                        logger.log_Message("monitoring", "INFO", f'Added {entry["subsystem_Name"]} to Alerted Monitoring')

                else:
                    os.makedirs(os.path.dirname("./monitoring/standard_Monitoring.json"), exist_ok=True)
                    if not os.path.exists("./monitoring/standard_Monitoring.json"):
                        with open("./monitoring/standard_Monitoring.json", 'w') as new_file:
                            json.dump([], new_file)

                sleep(60)

        except Exception as ex:
            logger.log_Message("monitoring", "ERROR", f'Error in standard_Monitoring: {ex}')



    def add_Component_To_Monitor(self, kafka_Topic_Name): 

        try:
            consumer = KafkaConsumer(kafka_Topic_Name, bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])

            for message in consumer:
            
                messageContents = json.loads(message.value)
                print(messageContents)
                
                # Check whether the subsystem has an entry in alerted_Monitoring file. 
                present = jFH.search_In_File("./monitoring/alerted_Monitoring.json", messageContents["subsystem_Name"])
                
                # If entry is present delete entry from Json file
                if present: 
                    jFH.delete_From_File("./monitoring/alerted_Monitoring.json", messageContents["subsystem_Name"])
                    logger.log_Message("monitoring", "INFO", f'Removed {messageContents["subsystem_Name"]} from Alerted Monitoring')


                # Check whether the subsystem has an entry in standard_Monitoring file. 
                present = jFH.search_In_File("./monitoring/standard_Monitoring.json", messageContents["subsystem_Name"])
                
                # If entry is present update the entry time for that subsystem. 
                if present: 
                    present = jFH.update_In_File("./monitoring/standard_Monitoring.json", messageContents["subsystem_Name"], messageContents["current_Time"])
                    logger.log_Message("monitoring", "INFO", f'Updated {messageContents["subsystem_Name"]} in Standard Monitoring')
                    

                # If entry is not present in standard_Monitoring then add it there.
                else: 
                    jFH.append_To_File("./monitoring/standard_Monitoring.json", messageContents)
                    logger.log_Message("monitoring", "INFO", f'Added {messageContents["subsystem_Name"]} to Standard Monitoring')


        except Exception as ex:
            logger.log_Message("monitoring", "ERROR", f'Error while consuming heartbeat from topic {kafka_Topic_Name}: {ex}')


    def start_Monitoring(self): 
        
        t_Standard = threading.Thread(target=self.standard_Monitoring, args=())
        t_Alerted = threading.Thread(target=self.alerted_Monitoring, args=())
        t_Standard.start()
        t_Alerted.start()

        for topic in KAFKA_TOPIC_NAMES :
            t = threading.Thread(target=self.add_Component_To_Monitor, args=(topic, ))
            t.start()
        

if __name__ == '__main__':
    monitor = Monitor()
    monitor.start_Monitoring()