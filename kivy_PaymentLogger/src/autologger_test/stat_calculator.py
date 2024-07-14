import json
import argparse
import math

def compute_statistics(filepath):
    with open(filepath, 'r') as file:
        transactions = file.readlines()

    n = len(transactions)
    sum_L = 0
    L_values = []

    for line in transactions:
        transaction = json.loads(line)
        L = int(transaction["receiveTime"]) - int(transaction["sendTime"])
        L_values.append(L)
        sum_L += L
        print(f"Processed line: {transaction}")

    if n > 0:
        L_mean = sum_L / n
        sum_sq_diff = sum((x - L_mean) ** 2 for x in L_values)
        L_std_dev = math.sqrt(sum_sq_diff / n)
    else:
        L_mean = 0
        L_std_dev = 0

    return n, L_mean, L_std_dev

def main():
    parser = argparse.ArgumentParser(description="Process JSON file to compute time differences and their statistics.")
    parser.add_argument('ordinal', type=int, help="Ordinal number (integer)")
    parser.add_argument('filepath', type=str, help="Path to the JSON file")
    args = parser.parse_args()

    n, L_mean, L_std_dev = compute_statistics(args.filepath)
    result = [args.ordinal, n, L_mean, L_std_dev]
    print(result)
    return result

if __name__ == "__main__":
    main()

# import json
# import math
# import argparse

# def calculate_statistics(o, filepath):
#     # Initialize variables
#     n = 0
#     sum_L = 0
#     L_values = []

#     # Open the file and process each line
#     with open(filepath, 'r') as file:
#         for line in file:
#             n += 1
#             transaction = json.loads(line)
#             L = int(transaction['receiveTime']) - int(transaction['sendTime'])
#             L_values.append(L)
#             sum_L += L

#     # Calculate mean of L
#     L_mean = sum_L / n if n != 0 else 0

#     # Calculate standard deviation of L
#     sum_sq_diff = sum((x - L_mean) ** 2 for x in L_values)
#     L_std_dev = math.sqrt(sum_sq_diff / n) if n != 0 else 0

#     # Print and return results
#     results = [o, n, L_mean, L_std_dev]
#     print(results)
#     return results

# def main():
#     # Setup argparse to manage command-line arguments
#     parser = argparse.ArgumentParser(description="Process JSON file to compute time difference statistics.")
#     parser.add_argument('ordinal', type=int, help="Ordinal number (integer)")
#     parser.add_argument('file_path', type=str, help="File path to the JSON file")
    
#     # Parse arguments
#     args = parser.parse_args()
    
#     # Calculate and print statistics
#     calculate_statistics(args.ordinal, args.file_path)

# if __name__ == "__main__":
#     main()
