import pandas as pd
import matplotlib.pyplot as plt

def plot_data_from_csv(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Extract the Channel1 column
    channel_data = data['Channel1']

    # Create the plot
    fig, ax = plt.subplots()
    ax.set_title('Real-time Data Plot')
    ax.set_xlabel('Index')
    ax.set_ylabel('Channel1')
    line, = ax.plot([], [], label='Channel1')
    ax.legend()

    # Iterate through each value in the Channel1 data and update the plot
    for index, value in enumerate(channel_data):
        # Update the plot with the new value
        x_data = list(range(1, index+2))
        y_data = channel_data.iloc[:index+1].tolist()
        line.set_data(x_data, y_data)

        # Adjust the plot limits if needed
        ax.relim()
        ax.autoscale_view()

        # Pause to update the plot
        plt.pause(0.1)  # Adjust this value to control the pause time

# Example usage
csv_file = "Datasets/alpha7.csv"
plot_data_from_csv(csv_file)