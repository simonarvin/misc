
import numpy as np  # Import numpy library for numerical operations
import json  # Import json library for working with JSON data
import matplotlib.pyplot as plt  # Import matplotlib library for plotting
import tailwind_colors as tw  # Import tailwind_colors for color schemes

def oval_area(radius1, radius2) -> float:
    """
    Function to calculate the area of an oval given its radii.

    Parameters:
    - radius1: float, radius along the first axis
    - radius2: float, radius along the second axis

    Returns:
    - float, area of the oval
    """
    if np.isnan(radius1):  # Check if the first radius is NaN
        return np.nan  # Return NaN if radius1 is NaN
    return np.pi * radius1 * radius2  # Calculate and return the area of the oval

filepath = "datalog.json"  # Path to the JSON file containing data

time = []  # List to store time values
pupil = []  # List to store pupil data

# Read data from the JSON file
with open(filepath) as file:
    for line in file:
        data_temp = json.loads(line)  # Load JSON data from each line
        time.append(data_temp["time"])  # Append time value to the time list
        try:
            pupil.append(data_temp["pupil"])  # Append pupil data to the pupil list
        except KeyError:
            pupil.append(np.ones(4) * np.nan)  # Fill with NaNs if no pupil entry

time = np.array(time).astype(np.float64)  # Convert time list to numpy array of float64
time = (time - time[0])  # Normalize time to start from 0 and get duration in seconds

# Calculate areas of pupils using oval_area function
areas = [oval_area(*pup[1:3]) for pup in pupil]

# Create subplots for plotting pupil size, position, and speed
fig, axs = plt.subplots(1, 3, figsize=(9, 3))

# Plot pupil size over time
ax = axs[0]
ax.plot(time, areas, color=tw.TAILWIND_COLORS_HEX.INDIGO_700)
ax.set_ylabel(r"pupil size ($px^2$)")
ax.set_xlabel("time (s)")
ax.set_title("pupil size")

# Plot pupil position over time
ax = axs[1]
coordinates = []
for pup in pupil:
    if pup[0] != pup[0]:  # Check if the pupil position is NaN
        continue
    coordinates.append([pup[0][0], pup[0][1]])  # Append pupil position to coordinates
coordinates = np.array(coordinates)  # Convert coordinates list to numpy array

ax.plot(coordinates[:, 0], coordinates[:, 1], color=tw.TAILWIND_COLORS_HEX.RED_500)
ax.set_xlabel("x-coord (px)")
ax.set_ylabel("y-coord (px)")
ax.set_title("pupil position")

# Plot pupil speed over time
ax = axs[2]
dx = np.diff(coordinates[:, 0])  # Calculate change in x-coordinate
dy = np.diff(coordinates[:, 1])  # Calculate change in y-coordinate
speeds = np.sqrt(dx**2 + dy**2)  # Calculate speed using Euclidean distance formula

ax.bar(np.arange(len(speeds)), speeds, width=1, color=tw.TAILWIND_COLORS_HEX.RED_500)
ax.set_xlabel("time (s)")
ax.set_ylabel("speed")
ax.set_title("pupil speed (px/s)")
ax.set_ylim(0, 50)  # Set y-axis limit for better visualization
fig.tight_layout()  # Adjust layout to prevent overlapping
plt.show()  # Display the plots
