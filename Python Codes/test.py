import serial
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyautogui  # Library for simulating keyboard inputs

# Specify serial port and baud rate
BAUD_RATE = 115200
COM_PORT = 'COM7'  # Change this to the port where your Arduino is connected

WINDOW_SIZE = 400
THRESHOLD_FACTOR = 0.2185
MAX = 100000
INTERVAL = 1000  # Increase the interval size to allow more data points to be plotted

flag = True
threshold = MAX
count = 0
sum_val = 0
avg_value = 0
max_value_encountered = 0
                 
# Initialize lists for plotting
timestamps = []
channel1_data = []

# Initialize threshold_text outside the animate function
fig, ax = plt.subplots()

# Function to simulate space bar press
def space_bar_press():
    pyautogui.press('space')

# Function to update plot
def animate(i):
    global count, sum_val, flag, threshold, max_value_encountered, timestamps, channel1_data
    
    # Connect to Arduino
    arduino = serial.Serial(COM_PORT, BAUD_RATE)

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
                        channel1_data.append(current_sample)
                        timestamps.append(time.time())

                        # Thresholding part
                        count += 1
                        value = current_sample
                        sum_val += value

                        if flag == False:
                            threshold = MAX

                        if value > threshold:
                            print("Found it! val:", value)
                            flag = False
                            
                            # Simulate space bar press
                            space_thread = threading.Thread(target=space_bar_press)
                            space_thread.start()

                        if count == WINDOW_SIZE:
                            thresholdingFunc()
                            flag = True

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        arduino.close()

    # Update plot with new data
    ax.clear()
    ax.plot(timestamps, channel1_data)
    
    # Adjust y-axis limits dynamically
    min_val = min(channel1_data[-WINDOW_SIZE:]) if channel1_data else 0
    max_val = max(channel1_data[-WINDOW_SIZE:]) if channel1_data else 0
    ax.set_ylim(0, max_val * 25.1)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Channel 1 Data')
    ax.set_title('Real-time Data Plot')

# Thresholding function
def thresholdingFunc():
    global count, sum_val, avg_value, threshold, max_value_encountered
    count = 0
    avg_value = sum_val / WINDOW_SIZE
    threshold = avg_value + (avg_value * THRESHOLD_FACTOR)
    sum_val = avg_value
    max_value_encountered = max(channel1_data[-WINDOW_SIZE:])  # Update max value encountered

try:
    ani = animation.FuncAnimation(fig, animate, interval=INTERVAL)
    plt.show()

except KeyboardInterrupt:
    print("Exiting...")

finally:
    print("Script ended.")
