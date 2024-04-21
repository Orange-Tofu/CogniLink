import matplotlib.pyplot as plt

# Create an empty plot
plt.figure()
plt.title('Plot of Values')
plt.xlabel('Index')
plt.ylabel('Value')
plt.grid(True)
plt.ion()  # Turn on interactive mode

# Loop through values of i and update the plot
for i in range(0, 100, 1):
    plt.plot(i, marker='o', linestyle='-', color='blue')  # Plot the value
    plt.draw()  # Force the plot to update immediately
    plt.pause(0.001)  # Pause to update the plot

plt.ioff()  # Turn off interactive mode
plt.show()  # Display the final plot
