#!/bin/bash

# Number of iterations (n)
n=1015

# Path to the monolith scripts
sender_script="./sender.py"
receiver_script="./reciever.py"

# Loop through x from 1 to n
for ((x=1; x<=n; x++))
do 
    # Create subfolder
    folder_name="datafiles/test_${x}_data"
    mkdir -p "$folder_name"

    # Generate random data
    python3 data_generator.py -n $((x)) --filename "$folder_name/input_data.json"

    # Define filenames for interim and final output files
    interim_file="$folder_name/sender_interim_file.json"
    final_file="$folder_name/received_final.json"


    # Run sender in another new terminal
    gnome-terminal -- bash -c "python3 $sender_script --filename $folder_name/input_data.json --output_file $interim_file > ./$folder_name/sender_output.txt" 
    # Run receiver in a new terminal
    sleep 0.001
    gnome-terminal -- bash -c "python3 $receiver_script --input_file ./$interim_file --output_file ./$final_file > ./$folder_name/receiver_output.txt"
done
