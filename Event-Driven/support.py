import json
from datetime import datetime
import os
from random import randint
from logger import Logger
from kafka import KafkaConsumer
from kafka_Producer import kafka_Producer
from global_Data import *
import threading
from monitor import Monitor

logger = Logger()
monitor = Monitor()

class Support:
    def __init__(self, support_directory):
        self.support_directory = support_directory
        t = threading.Thread(target=self.process_issue, args=())
        t.start()
        t1 = threading.Thread(target=monitor.heartbeat_Generator, args=("support",))
        t1.start()


    def submit_issue(self, user_name, subject, content):
    
        issue = {
            "userName": user_name,
            "subject": subject,
            "content": content,
        }

        while True:
            try:
                producerForLogging = kafka_Producer()
                producerForLogging.send_message("support", issue)
                logger.log_Message("feedback-support", "INFO", "Successfully sent support request by user to the kafka topic support")
                break

            except Exception as ex:
                logger.log_Message("feedback-support", "ERROR", f'Error while submitting support request through kafka: {ex}')


    def process_issue(self):

        consumer = KafkaConsumer("support", bootstrap_servers=[KAFKA_IP+":"+KAFKA_PORT_NO])

        try:
            for message in consumer:

                messageContents = json.loads(message.value)
                logger.log_Message("feedback-support", "INFO", f'Received message: {messageContents}')
                print(messageContents)

                issue_data = self.load_issues(messageContents["userName"])
                issue_number = 1
                if "issues" in issue_data:
                    issue_number = len(issue_data["issues"]) + 1
                
                issue = {
                    "issueNumber": issue_number,
                    "issueId": self.generate_issue_id(),
                    "subject": messageContents["subject"],
                    "content": messageContents["content"],
                    "devStatus": "Pending",
                    "userStatus": "Open"
                }

                if "issues" not in issue_data:
                    issue_data["issues"] = []

                issue_data["issues"].append(issue)
                self.save_issue(messageContents["userName"], issue_data)
                logger.log_Message("feedback-support", "INFO", f'Support request of user : {messageContents["userName"]} has been added.')



        except Exception as ex:
            logger.log_Message("feedback-support", "ERROR", f'Error while consuming support request through kafka: {ex}')


    # def submit_issue(self, user_name, subject, content):

    #     issue_data = self.load_issues(user_name)

    #     issue_number = 1
    #     if "issues" in issue_data:
    #         issue_number = len(issue_data["issues"]) + 1

    #     issue = {
    #         "issueNumber": issue_number,
    #         "issueId": self.generate_issue_id(),
    #         "subject": subject,
    #         "content": content,
    #         "devStatus": "Pending",
    #         "userStatus": "Open"
    #     }

    #     if "issues" not in issue_data:
    #         issue_data["issues"] = []

    #     issue_data["issues"].append(issue)
    #     self.save_issue(user_name, issue_data)


    def generate_issue_id(self):
        # Generate a random issue ID 
        return "ISSUE" + str(randint(100000000, 999999999)) + str(datetime.now().timestamp())


    def load_issues(self, user_name):

        issues_file = f"{self.support_directory}/{user_name}_issues.json"

        if os.path.exists(issues_file):
            with open(issues_file, "r") as file:
                issue_data = json.load(file)
        else:
            issue_data = {
                "userName": user_name,
                "issues": []
            }

        return issue_data


    def save_issue(self, user_name, issue_data):

        issues_file = f"{self.support_directory}/{user_name}_issues.json"

        os.makedirs(os.path.dirname(issues_file), exist_ok=True)

        with open(issues_file, "w") as file:
            json.dump(issue_data, file)
