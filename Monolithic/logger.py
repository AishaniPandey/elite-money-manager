from datetime import datetime
from json_File_Handler import json_File_Handler


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

        try:
            jFH = json_File_Handler()
            jFH.append_To_File("./logs/log-" + subsystem_Name, log_entry)

        except Exception as ex:
            print(f'Error while writing logs into log-{subsystem_Name}: {ex}')
        