import json
from datetime import datetime
import os
from random import randint

class Support:
    def __init__(self, support_directory):
        self.support_directory = support_directory

    def submit_issue(self, user_name, subject, content):

        issue_data = self.load_issues(user_name)

        issue_number = 1
        if "issues" in issue_data:
            issue_number = len(issue_data["issues"]) + 1

        issue = {
            "issueNumber": issue_number,
            "issueId": self.generate_issue_id(),
            "subject": subject,
            "content": content,
            "devStatus": "Pending",
            "userStatus": "Open"
        }

        if "issues" not in issue_data:
            issue_data["issues"] = []

        issue_data["issues"].append(issue)
        self.save_issue(user_name, issue_data)

        # Produce message to Kafka topic
        # message = {
        #     "action": "submit_issue",
        #     "issue": issue
        # }

    def generate_issue_id(self):
        # Generate a random issue ID (You can implement your own logic here)
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
        with open(issues_file, "w") as file:
            json.dump(issue_data, file)
