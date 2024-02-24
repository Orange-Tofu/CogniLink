import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import keyboard
import threading

# Load the data from the CSV file
data = []
times = []
with open('../Datasets/alpha1.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            times.append(row['Timestamp'])
            data.append(float(row['Channel1']))
        except ValueError:
            # Ignore non-numeric values
            pass

# Set your thresholds
upper_threshold = 550  # Adjust this value as per your requirement
lower_threshold = 480  # Adjust this value as per your requirement

# Downsampling factor
downsampling_factor = 200  # Adjusted to accommodate the 5-minute duration

# Convert timestamps to numeric values
numeric_times = list(range(len(times)))

# Initialize the plot with higher DPI
fig, ax = plt.subplots(dpi=200)
line, = ax.plot([], [], lw=1.5)
time_text = ax.text(0.95, 0.1, '', transform=ax.transAxes, ha='right')
eeg_text = ax.text(0.95, 0.05, '', transform=ax.transAxes, ha='right')
key_text = ax.text(0.5, 0.9, '', transform=ax.transAxes, ha='center', fontsize=12, color='red')
ax.set_xlabel('Time (s)', ha='right', x=1.0)
ax.set_ylabel('EEG data', ha='right', y=1.0)
ax.set_title('Real-time EEG data visualization')

# Initialize lists to store data for plotting
time_values = []
eeg_values = []
prev_above_upper_threshold = False
prev_below_lower_threshold = False

# Function to update the plot in real-time
def update(frame):
    global prev_above_upper_threshold, prev_below_lower_threshold  # Declare the global variables

    # Append new values to the lists
    time_values.append(numeric_times[frame*downsampling_factor])
    eeg_values.append(data[frame*downsampling_factor])

    # Set the data for the line
    line.set_data(time_values, eeg_values)

    # Check threshold conditions
    if data[frame*downsampling_factor] > upper_threshold:
        if not prev_above_upper_threshold:
            keyboard.press('up')
            key_text.set_text('Key Pressed: UP')
            print(f"Signal went above upper threshold at time {times[frame*downsampling_factor]} with value {data[frame*downsampling_factor]} .. PRESSED UP")
            prev_above_upper_threshold = True
            prev_below_lower_threshold = False
            threading.Timer(1, reset_key_text).start()
    elif data[frame*downsampling_factor] < lower_threshold:
        if not prev_below_lower_threshold:
            keyboard.press("down")
            key_text.set_text('Key Pressed: DOWN')
            print(f"Signal went above below threshold at time {times[frame*downsampling_factor]} with value {data[frame*downsampling_factor]} .. PRESSED DOWN")
            prev_below_lower_threshold = True
            prev_above_upper_threshold = False
            threading.Timer(1, reset_key_text).start()
    else:
        prev_above_upper_threshold = False
        prev_below_lower_threshold = False

    # Adjust the view window as the data progresses
    if frame > 10:  # Adjust this value based on the length of your data
        ax.set_xlim(numeric_times[frame*downsampling_factor] - 5000, numeric_times[frame*downsampling_factor] + 5000)  # Adjust the view window as the data progresses
        ax.set_ylim(min(eeg_values) - 5, max(eeg_values) + 5)  # Adjust the y-axis as the data progresses

    # Dynamically update x and y labels
    time_text.set_text(f'Time - {times[frame*downsampling_factor]}')
    eeg_text.set_text(f'EEG data - {data[frame*downsampling_factor]}')

    fig.canvas.draw()  # Update the canvas without changing the labels on resizing

    return line, time_text, eeg_text, key_text

# Function to reset the key text
def reset_key_text():
    key_text.set_text('')

# Animate the plot with a reduced interval
ani = FuncAnimation(fig, update, frames=len(times)//downsampling_factor, blit=True, interval=5)

# Display the plot
plt.show()
