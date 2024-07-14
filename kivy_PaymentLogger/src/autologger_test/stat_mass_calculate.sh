#!/bin/bash

# Define the output CSV file
output_file="results.csv"

# Write the header of the CSV
echo "Ordinal,N,L_mean,L_std_dev" > $output_file

# Loop from 1 to 1015 and run the Python script
for i in $(seq 1 1015); do
    # Generate file path based on ordinal
    file_path="./kafka_loadtest/test_${i}_data/output_data.json"
    
    # Check if file exists
    if [ -f "$file_path" ]; then
        # Run Python script and capture the output
        result=$(python3 ./stat_calculator.py $i $file_path)
        
        # Remove brackets and spaces from the output
        result=$(echo $result | tr -d '[]' | tr -d ' ')
        
        # Write the result to the CSV file
        echo $result >> $output_file
    else
        echo "$i,-,-,-" >> $output_file # Write a placeholder if the file does not exist
    fi
done
