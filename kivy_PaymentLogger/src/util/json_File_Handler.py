##json_File_Handler.py
#@Import: util.json_File_Handler
#@Author : @YashSampat23154
#@LastModified : 2024-04-22 18:08 IST
#@Title : Payment Logger App JSON File Handler
#@LastModifiedBy: @Grimoors
#Description : CRUD on a JSON file as a proxy for a database.abs


import os
import fcntl
import json

debug = 0

class json_File_Handler(): 

    def append_To_File(self, file_path, new_data):
       
        try:
            if debug:
                print("From File : json_File_Handler -  Appending to file: ", file_path)
                print("From File : json_File_Handler - New data: ", new_data)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)

            with open(file_path, 'r+') as file:
                fcntl.flock(file.fileno(), fcntl.LOCK_EX)
                file.seek(0)
                file_content = file.read().strip()

                data = json.loads(file_content) if file_content else []

                data.append(new_data)

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

                fcntl.flock(file.fileno(), fcntl.LOCK_UN)

        except Exception as e:
            print("An error occurred while appending to the file: ", str(e))



    def search_Transaction_By_t_id (self, file_path, t_id):

        try:

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)
        
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    file_content = file.read().strip()

                    data = json.loads(file_content) if file_content else []

                    for entry in data:
                        if entry['t_id'] == t_id:
                            return True
                    return False
            else:
                print("File not found:", file_path)
                return False
            
        except Exception as e:
            print("An error occurred while searching in the file: ", str(e))
            return False
        


    def search_In_File (self, file_path, subsystem_Name):

        try:

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)
        
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    file_content = file.read().strip()

                    data = json.loads(file_content) if file_content else []

                    for entry in data:
                        if entry['subsystem_Name'] == subsystem_Name:
                            return True
                    return False
            else:
                print("File not found:", file_path)
                return False
            
        except Exception as e:
            print("An error occurred while searching in the file: ", str(e))
            return False
        


    def delete_From_File (self, file_path, subsystem_Name):

        try:

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)
            
            if os.path.exists(file_path):
                with open(file_path, 'r+') as file:
                    fcntl.flock(file.fileno(), fcntl.LOCK_EX)
                    file.seek(0)
                    file_content = file.read().strip()

                    data = json.loads(file_content) if file_content else []

                    updated_data = [entry for entry in data if entry.get('subsystem_Name') != subsystem_Name]

                    file.seek(0)
                    json.dump(updated_data, file, indent=4)
                    file.truncate()

                    fcntl.flock(file.fileno(), fcntl.LOCK_UN)

            else:
                print("File not found:", file_path)

        except Exception as e:
            print("An error occurred while deleting from the file: ", str(e))



    def update_In_File (self, file_path, subsystem_Name, current_Time):
       
        try:

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    json.dump([], new_file)
            
            if os.path.exists(file_path):
                with open(file_path, 'r+') as file:
                    fcntl.flock(file.fileno(), fcntl.LOCK_EX)
                    file.seek(0)
                    file_content = file.read().strip()

                    data = json.loads(file_content) if file_content else []

                    for entry in data:
                        if entry['subsystem_Name'] == subsystem_Name:
                    
                            entry['current_Time'] = current_Time

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()

                    fcntl.flock(file.fileno(), fcntl.LOCK_UN)

            else:
                print("File not found:", file_path)

        except Exception as e:
            print("An error occurred while updating the file: ", str(e))