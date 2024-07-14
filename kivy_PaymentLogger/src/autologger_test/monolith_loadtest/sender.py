import json
import time
import argparse

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def append_send_time(json_obj):
    json_obj['sendTime'] = str(int(time.time()))
    return json_obj

def main(filename, output_file):
    # Read transactions from the input file
    transactions = read_json_file(filename)
    
    # Append and write each transaction to the interim file
    with open(output_file, 'a') as outfile:
        for transaction in transactions:
            modified_transaction = append_send_time(transaction)
            outfile.write(json.dumps(modified_transaction) + '\n')
            time.sleep(0.001)  # Simulate time delay between sends

if __name__ == "__main__":
    print ( "Enter the path to the JSON file: " )
    parser = argparse.ArgumentParser(description='Append send time and write to an interim file.')
    parser.add_argument('--filename', type=str, required=True, help='Path to the input JSON file.')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the interim JSON file.')
    args = parser.parse_args()
    main(args.filename, args.output_file)
    print ( f"Path to the file entered is {args.filename} and {args.output_file}" )
