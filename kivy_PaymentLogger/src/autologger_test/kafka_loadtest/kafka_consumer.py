import json
from kafka import KafkaConsumer
import time
import argparse

i = 0

def append_receive_time(json_obj):
    json_obj['receiveTime'] = str(int(time.time()))
    return json_obj

def consume_messages(consumer, topic, output_file='received.json', n=10):
    global i
    for message in consumer:
        msg = json.loads(message.value.decode('utf-8'))
        processed_msg = append_receive_time(msg)
        with open(output_file, 'a') as file:
            file.write(json.dumps(processed_msg) + '\n')
        i = i+1
        if i == n:
            break


if __name__ == "__main__":
    print("Consumer started")
    # Read command line argument for output file 
    parser = argparse.ArgumentParser(description='Consume messages from Kafka and append receive time')
    parser.add_argument('--output', type=str, default='received.json', help='Name of the output file')
    parser.add_argument('-n', type=int,     help='Number of transactions to generate'   )
    args = parser.parse_args()
    output_file = args.output
    n = args.n
    print ( f"Output file: {output_file}")
    print ( f"Number of transactions: {n}")

    consumer = KafkaConsumer('tcreate',
                             
                             bootstrap_servers=['localhost:9092']
                             
                             
                             )
    while (True):
        consume_messages(consumer, 'tcreate' , output_file, n)
        if i == n:
            break


