import os
import json
from logger import Logger
from json_File_Handler import json_File_Handler


logger = Logger()
jFH = json_File_Handler()


class Authenticate(): 

    def login(self, username, password):

        os.makedirs(os.path.dirname("./credentials.json"), exist_ok=True)

        if not os.path.exists("./credentials.json"):
            with open("./credentials.json", 'w') as new_file:
                json.dump([], new_file)
    
        if os.path.exists("./credentials.json"):
            with open("./credentials.json", 'r') as file:
                file_content = file.read().strip()

                data = json.loads(file_content) if file_content else []

                for entry in data:
                    if entry['name'] == username and entry['password'] == password: 
                        return True
                return False
        else:
            # logger.log_Message("authentication", "ERROR", "Error locating credentials.json")
            print("Error locating credentials.json")
            return False




    def register(self, username, password, confirmed_Password):

        if username == "" or password == "" or confirmed_Password == "": 
            return False

        if password != confirmed_Password:
            logger.log_Message("authentication", "ERROR", "Passwords don't match")
            print("Passwords do not match.")
            return False
        
        os.makedirs(os.path.dirname("./credentials.json"), exist_ok=True)

        if not os.path.exists("./credentials.json"):
            with open("./credentials.json", 'w') as new_file:
                json.dump([], new_file)
    
        if os.path.exists("./credentials.json"):

            with open("./credentials.json", 'r') as file:
                file_content = file.read().strip()

                data = json.loads(file_content) if file_content else []
                
                for entry in data:
                    if entry['name'] == username:
                        # logger.log_Message("authentication", "ERROR", "Username already exists")
                        print("Username already exists.")
                        return False
            
            message = {
                    "name" : username,
                    "password" : password
                }

            jFH.append_To_File("./credentials.json", message) 
            # logger.log_Message("authentication", "INFO", "New user created")
            print("New user created")
            return True
