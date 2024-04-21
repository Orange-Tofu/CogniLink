import serial
import csv
import time
import matplotlib.pyplot as plt

# Specify serial port and baud rate
BAUD_RATE = 115200
COM_PORT = 'COM7'

# Connect to Arduino
arduino = serial.Serial(COM_PORT, BAUD_RATE)

# Open CSV file for writing
filename = "alphaQQ.csv"

# Initialize lists for x and y values
x_values = []
y_values = []

# Create the plot
plt.figure()
plt.title('Plot of Values')
plt.xlabel('Time (Minute:Second)')
plt.ylabel('Channel1')
plt.grid(True)
plt.ion()  # Turn on interactive mode

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Timestamp', 'Channel1']
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

                        # Get the current time (minute and second)
                        current_time = time.strftime('%M:%S')

                        # Write to CSV
                        writer.writerow({'Timestamp': current_time, 'Channel1': channel1_data})
                        print(f"Recorded: {current_time}, {channel1_data}")

                        # Append to x and y values lists
                        x_values.append(current_time)
                        y_values.append(channel1_data)

                        # Plot the values
                        plt.plot(x_values, y_values, linestyle='-')
                        plt.draw()  # Force the plot to update immediately
                        plt.pause(0.1)  # Pause to update the plot

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        arduino.close()
        plt.ioff()  # Turn off interactive mode
        plt.show()  # Display the final plot
        print("Serial connection closed.")
