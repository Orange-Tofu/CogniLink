# This is a sample code which takes in input form the arduino serial monitor and then 
# further processes it accordingly.

import serial
import csv
import time
import threading

# Specify serial port and baud rate
BAUD_RATE = 115200 # Alternatively use 230400, i.e. its double
COM_PORT = 'COM7'
WINDOW_SIZE = 20
THRESHOLD_FACTOR = 0.2185
MAX = 100000

flag = True
threshold = MAX
count = 0
sum = 0
avg_value = 0
version = 0
stop_thread = False
blink_counter = 0

# Connect to arduino


def thresholdingFuncDynamic():
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

def thresholdingFuncStatic():
    global count, threshold

    count = 0
    threshold = 7000
    # print("------------------------------------------------------------------------------------------------------------------------------")
    # print(threshold)
    # print("------------------------------------------------------------------------------------------------------------------------------")
    # print("Exiting")
    return

def thresholdingFuncAverage():
    global count, sum, avg_value, threshold

    count = 0
    avg_value = sum/WINDOW_SIZE
    threshold = avg_value
    sum = avg_value
    # print("------------------------------------------------------------------------------------------------------------------------------")
    # print(threshold)
    # print("------------------------------------------------------------------------------------------------------------------------------")
    return

def running_function():
    # Open CSV file for writing
    # filename = time.strftime("%Y%m%d-%H%M%S") + ".csv"
    arduino = serial.Serial(COM_PORT, BAUD_RATE)
    filename = "Datasets/exp" + str(version) + ".csv"
    global blink_counter, count, sum, threshold, flag

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
                                blink_counter += 1
                                flag = False

                            if (count == WINDOW_SIZE):
                                if (version == 0):
                                    thresholdingFuncStatic()
                                elif(version == 1):
                                    thresholdingFuncAverage()
                                elif(version == 2):
                                    thresholdingFuncDynamic()
                                else:
                                    print("Smtg gone wrong")
                                flag = True

                            if(stop_thread):
                                return


        except KeyboardInterrupt:
            print("Exiting...")

        finally:
            arduino.close()
            print("Serial connection closed.")


def counter():
    duration = 60
    start_time = time.time()
    while time.time() - start_time < duration:
        pass
    global version, stop_thread
    version += 1
    stop_thread = True
    return

def main():
    file = open("blink_counts.txt", "a")
    global blink_counter, stop_thread

    for i in range(0, 3):
        thread1 = threading.Thread(target=counter)
        thread2 = threading.Thread(target=running_function)
        
        print("About to start, version:", version)
        time.sleep(10)
        print("Starting")
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        print("Both thread stopped")
        print("Blink count:", blink_counter)
        file.write(f"Blink version: {version}, blink_counted: {blink_counter}")
        
        time.sleep(10)

        stop_thread = False
        print()
        blink_counter = 0

    file.close()

main()