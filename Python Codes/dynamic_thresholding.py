# Attempt to achieve dynamic thresholding, kindof-kindof works
import csv

# GLobal Variables
# Assign your filenames here
SRC_FILE_NAME = "alpha1" + ".csv"

# General observation, window size and threshold factor seems directly proportionate.
# Larger the window size, larger threshold factor is recommended.
WINDOW_SIZE = 700

# Keep this factor between 0.9-1.1 [including], for filtered eeg data, [Personally Recomended: 1.0]
# Keep this factor between 0.1-0.3 [including], for non-filtered eeg data [Personally Recomended: 2~2.5]
THRESHOLD_FACTOR = 0.2

# Paths for the file 
src_file_path = "Datasets\\" + SRC_FILE_NAME

count = 0
sum = 0
avg_value = 0
threshold = 1000000 # Random very large number

with open(src_file_path, 'r') as src_file:
    src_data = csv.DictReader(src_file)

    for value in src_data:
        value = int(value['Channel1'])
        count += 1
        
        sum += value

        if (value > threshold):
            print("Found it! val:", value)
        
        if (count == WINDOW_SIZE):
            count = 0
            avg_value = sum/WINDOW_SIZE
            threshold = avg_value + (avg_value * THRESHOLD_FACTOR)
            sum = avg_value
            print("------------------------------------------------------------------------------------------------------------------------------")
            print(threshold)
            print("------------------------------------------------------------------------------------------------------------------------------")


print("Exiting")