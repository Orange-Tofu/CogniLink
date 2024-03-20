# This file copies data one row at a time from one csv file to the other. 

import csv

# Assign your filenames here
SRC_FILE_NAME = "alpha1" + ".csv"
DEST_FILE_NAME = "copy_of_dataset/copy_of_" + SRC_FILE_NAME + ".csv"

BAUD_RATE = 115200
CYCLE_COUNT = 5 # This count is also equivalent to number of seconds for which it will transfer data
# i.e. if CYCLE_COUNT is 5, then it will transfer BAUD_RATE * 5 number of data which is equivalent to data worth of 5 seconds.

# This is our assumed window size, or can also be called as assumed number of signals per second.
# While recording data, the baud rate is not matching data size as expected so we assume this to be our replacement for it.
WINDOW_SIZE = 46649


# Paths for the file 
src_file_path = "Datasets\\" + SRC_FILE_NAME
dest_file_path = "Datasets\\" + DEST_FILE_NAME

src_file = open(src_file_path, 'r')
count = 0

with open(dest_file_path, 'w', newline='') as dest_file:
    data_writer = csv.writer(dest_file)
    src_data = csv.reader(src_file)

    for row in src_data:
        
        # To skip the first row that is the header file
        count += 1
        if (count == 1):
            continue
        
        data_writer.writerow(row)

        if (count > WINDOW_SIZE * CYCLE_COUNT):
            print("Exiting")
            break

src_file.close()
