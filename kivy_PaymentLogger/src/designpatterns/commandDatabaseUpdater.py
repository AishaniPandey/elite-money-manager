## src/designpatterns/commandDatabaseUpdater.py
# @Import: designpatterns.commandDatabaseUpdater
# @Author: @Grimoors
# @Date: 2024-04-22
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-22 - 16:56 IST
# @Title: Command Design Pattern for Database Updater
# @Description: Command Design Pattern for updating SQLite database and JSON file; extensible for other databases or Kafka


import paymentdb
from util.json_File_Handler import json_File_Handler
from abc import ABC, abstractmethod
from util.KafkaHandler import KafkaHandler

debug = 0

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class UpdateSQLiteCommand(Command):
    def __init__(self, data):
        self.data = data
        self.db = paymentdb.PaymentDB()

    def execute(self):
        # Update SQLite database with self.data
        self.db.log_payment(**self.data)
        
        pass

# Concrete command to update JSON using json_File_Handler
class UpdateJsonCommand(Command):
    def __init__(self, data, json_path):
        self.data = data
        self.json_path = json_path
        self.handler = json_File_Handler()  # Instance of the JSON file handler

    def execute(self):
        # Use the append_To_File method from json_File_Handler to update JSON file
        if debug:
            print("From File : commandDatabaseUpdater -  Updating JSON file with data: ", self.data)
            print("From File : commandDatabaseUpdater - JSON file path: ", self.json_path)
        self.handler.append_To_File(self.json_path, self.data)

class NotifyThruKafkaCommand(Command):
    def __init__(self, data, kafka_topic="tcreate"):
        self.data = data
        self.kafka_topic = kafka_topic
        self.kafka = KafkaHandler()  # Instance of the Kafka handler

    def execute(self):
        # Use the send_to_kafka method from KafkaHandler to notify Kafka
        if debug:
            print("From File : commandDatabaseUpdater -  Notifying Kafka with data: ", self.data)
            print("From File : commandDatabaseUpdater - Kafka topic: ", self.kafka_topic)
        self.kafka.send_to_kafka( self.data , self.kafka_topic)

class Invoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()

# # Usage
# data = {'key': 'value'}
# invoker = Invoker()
# invoker.add_command(UpdateSQLiteCommand(data))
# invoker.add_command(UpdateJsonCommand(data))
# invoker.execute_commands()
