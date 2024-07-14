import json
import time
import argparse

def mark_transaction_processed(json_obj):
    json_obj['status'] = 'disabledandread'
    json_obj['receiveTime'] = str(int(time.time()))
    return json_obj

def process_interim_file(input_file, output_file):
    with open(output_file, 'a') as outfile:
        time.sleep(0.06)  # Delay to reduce CPU usage while polling
    # while True:
        with open(input_file, 'r') as infile:
            for line in infile:
                if not line.strip():  # Skip empty lines
                    continue
                                                                                                        
                transaction = json.loads(line.strip())
                if 'status' not in transaction:  # Process only if not already processed
                    modified_transaction = mark_transaction_processed(transaction)
                    outfile.write(json.dumps(modified_transaction) + '\n')


if __name__ == "__main__":
    print ( "Entered the receiver.py file")
    parser = argparse.ArgumentParser(description='Process transactions from an interim file and append to a final file.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the interim JSON file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the final JSON file.')
    args = parser.parse_args()
    print ( f"Path to the file entered is {args.input_file} and {args.output_file}")    
    process_interim_file(args.input_file, args.output_file)
