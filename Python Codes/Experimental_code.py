# This is a sample code which takes in input form the arduino serial monitor and then 
# further processes it accordingly.

import serial
import csv
import time

# Specify serial port and baud rate
BAUD_RATE = 115200 # Alternatively use 230400, i.e. its double
COM_PORT = 'COM7'
WINDOW_SIZE = 400
THRESHOLD_FACTOR = 0.2185
MAX = 100000

flag = True
threshold = MAX
count = 0
sum = 0
avg_value = 0

# Connect to arduino
arduino = serial.Serial(COM_PORT, BAUD_RATE)

def thresholdingFunc():
    global count, sum, avg_value, threshold

    count = 0
    avg_value = sum/WINDOW_SIZE
    threshold = avg_value + (avg_value * THRESHOLD_FACTOR)
    sum = avg_value
    # print("------------------------------------------------------------------------------------------------------------------------------")
    # print(threshold)
    # print("------------------------------------------------------------------------------------------------------------------------------")
    print("Exiting")
    return


# Open CSV file for writing
# filename = time.strftime("%Y%m%d-%H%M%S") + ".csv"
filename = "Datasets/alpha7.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Timestamp', 'Channel1']  # Add more fields for multiple channels
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            if arduino.in_waiting > 0:
                raw_bytes = arduino.read(arduino.in_waiting)

                for byte_index, byte_value in enumerate(raw_bytes):
                    if byte_index == 0 or (byte_value & 0x80) == 0x80:
                        frame_start = byte_index
                        current_sample = 0

                    current_sample = (current_sample << 7) | (byte_value & 0x7F)

                    if byte_index - frame_start == 1:
                        channel1_data = current_sample

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow({'Timestamp': current_time, 'Channel1': channel1_data})
                        # print(f"Recorded: {current_time}, {channel1_data}")

                        # Thresholding part
                        count += 1
                        value = int(channel1_data)
                        sum += value

                        if (flag == False):
                            threshold = MAX

                        if (value > threshold):
                            print("Found it! val:", value)
                            flag = False

                        if (count == WINDOW_SIZE):
                            thresholdingFunc()
                            flag = True


    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        arduino.close()
        print("Serial connection closed.")
