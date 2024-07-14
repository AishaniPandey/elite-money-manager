#!/bin/bash

# Number of iterations (n)
n=1015

# Path to your Kafka scripts
producer_script="kafka_producer.py"
consumer_script="kafka_consumer.py"

# Loop through x from 1 to n
for ((x=1; x<=n; x++))
do
    # Create subfolder
    folder_name="test_${x}_data"
    mkdir -p "$folder_name"

    # python3 data_generator.py -n 100 --filename test_100_data/input_data.json

    # Generate random data
    python3 data_generator.py -n $((x)) --filename "$folder_name/input_data.json"

    # Run consumer in a new terminal
    gnome-terminal -- bash -c "python3 $consumer_script --output "$folder_name/output_data.json" -n $((x))"

    # # # Wait for a few seconds to allow the consumer to start
    # sleep 

    # Run producer in another new terminal
    gnome-terminal -- bash -c "python3 $producer_script --filename "$folder_name/input_data.json" -n $((x))"

    # # Wait for the producer to finish
    # sleep 3

    # # Move the output file to the subfolder
    # mv received.json "$folder_name/output_data.json"
done
