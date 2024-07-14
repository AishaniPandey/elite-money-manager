import json
import time
from kafka import KafkaProducer
import argparse

i=0

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def append_send_time(json_obj):
    json_obj['sendTime'] = str(int(time.time()))
    return json_obj

def produce_messages(producer, topic, json_array, n):
    global i
    for json_obj in json_array:
        print("Trying to send message ", i)
        print(f"Message: {json_obj}")
        msg = json.dumps(append_send_time(json_obj))
        producer.send(topic, value=msg.encode('utf-8'))
        i = i+1
        if i == n:
            break
        # time.sleep(1)  # Adjust the delay between messages if needed

if __name__ == "__main__":
    #parse command line arguments - filename\
    print("Producer started")
    parser = argparse.ArgumentParser(description='Read JSON file and produce messages to Kafka')
    parser.add_argument('--filename', type=str, help='Name of the JSON file to read')
    parser.add_argument('-n', type=int, help='Number of transactions to generate')
    args = parser.parse_args()
    filename = args.filename
    n = args.n
    print ( f"Filename: {filename}")
    print ( f"Number of transactions: {n}")
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    topic = 'tcreate'
    json_array = read_json_file(filename)
    produce_messages(producer, topic, json_array, n)
