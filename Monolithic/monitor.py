from time import time, sleep
import threading
import json
from logger import Logger
from notify import Notify
from json_File_Handler import *


logger = Logger()
jFH = json_File_Handler()


class Monitor():
    
    # Send a heartbeat every 60 seconds
    def heartbeat_Generator(self, subsystem_Name):

        while True:

            try:

                heartbeat = {
                    "subsystem_Name" : subsystem_Name,
                    "current_Time" : time()
                }

                # Check whether the subsystem has an entry in alerted_Monitoring file. 
                present = jFH.search_In_File("./monitoring/alerted_Monitoring.json", heartbeat["subsystem_Name"])
                
                # If entry is present delete entry from Json file
                if present: 
                    jFH.delete_From_File("./monitoring/alerted_Monitoring.json", heartbeat["subsystem_Name"])
                    logger.log_Message("monitoring", "INFO", f'Removed {heartbeat["subsystem_Name"]} from Alerted Monitoring')


                # Check whether the subsystem has an entry in standard_Monitoring file. 
                present = jFH.search_In_File("./monitoring/standard_Monitoring.json", heartbeat["subsystem_Name"])
                
                # If entry is present update the entry time for that subsystem. 
                if present: 
                    present = jFH.update_In_File("./monitoring/standard_Monitoring.json", heartbeat["subsystem_Name"], heartbeat["current_Time"])
                    logger.log_Message("monitoring", "INFO", f'Updated {heartbeat["subsystem_Name"]} in Standard Monitoring')
                    

                # If entry is not present in standard_Monitoring then add it there.
                else: 
                    jFH.append_To_File("./monitoring/standard_Monitoring.json", heartbeat)
                    logger.log_Message("monitoring", "INFO", f'Added {heartbeat["subsystem_Name"]} to Standard Monitoring')

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
                            if current_Time - entry['current_Time'] >= 30:
                                remove_From_Alert_Monitoring.append(entry)


                    notify = Notify()
                    
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
                            if current_Time - entry['current_Time'] >= 15:
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



monitor = Monitor()
t_Standard = threading.Thread(target=monitor.standard_Monitoring, args=())
t_Alerted = threading.Thread(target=monitor.alerted_Monitoring, args=())
t_Standard.start()
t_Alerted.start()