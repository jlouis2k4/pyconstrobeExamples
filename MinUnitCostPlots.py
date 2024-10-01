# main.py

import json
import textwrap
import matplotlib.pyplot as plt


import os
import sys

package_path = r"C:\source\jStrobe\jsPy"#\jsPy"  # Change this to the actual path
if package_path not in sys.path:
    sys.path.append(package_path)

from jsPy import ProcessManager

# Fixed path to executable
path_to_exe = r"C:\source\jStrobe\jsApp\Debug\jStrobe.exe"
json_data_array = []

def process_incoming_json(json_string):
    try:
        parsed_data = json.loads(json_string)
        json_data_array.append(parsed_data)
        update_plot(parsed_data)
    except json.JSONDecodeError:
        print("Invalid JSON string")

series_data = {}
fig, ax = plt.subplots()

def initialize_plot():
    """Initializes the plot."""
    plt.ion()  # Enable interactive mode
    ax.set_xlabel('Number of Trucks')
    ax.set_ylabel('Unit Cost ($/Lcy)')
    ax.set_title('Plot of Unit Cost vs Number of Trucks')

    plt.show()

def update_plot(entry):
    """Updates the plot with new data from a JSON object."""
    numExc = entry["ExcWt.CurCount"]
    numTruck = entry["TrkWt.CurCount"]
    SimTime = entry["SimTime"]

    # Calculate the metric to plot
    custom_metric = (numTruck * 250 + numExc * 300) / (60000 / SimTime)

    # Initialize the series if it doesn't exist
    if numExc not in series_data:
        series_data[numExc] = ([], [])  # (numTruck values, custom_metric values)

    # Append values to the respective series
    series_data[numExc][0].append(numTruck)
    series_data[numExc][1].append(custom_metric)

    # Clear the axis to redraw
    ax.clear()

    # Plotting the data
    for numExc, (numTruck_values, custom_metrics) in series_data.items():
        ax.plot(numTruck_values, custom_metrics, marker='o', label=f'numExc = {numExc}')

    ax.legend()
    plt.draw()
    plt.pause(0.1)  # Pause to allow the plot to update

# Example usage





def plot_truck_vs_custom_metric(json_data):
    # Dictionary to hold lists of values for each numExc
    series_data = {}

    # Process each entry in the JSON data
    for entry in json_data:
        numExc = entry["ExcWt.CurCount"]
        numTruck = entry["TrkWt.CurCount"]
        SimTime = entry["SimTime"]

        # Calculate the metric to plot
        custom_metric = (numTruck * 250 + numExc * 300) / (60000 / SimTime)

        # Initialize the series if it doesn't exist
        if numExc not in series_data:
            series_data[numExc] = ([], [])  # (numTruck values, custom_metric values)

        # Append values to the respective series
        series_data[numExc][0].append(numTruck)
        series_data[numExc][1].append(custom_metric)

    # Plotting the data
    for numExc, (numTruck_values, custom_metrics) in series_data.items():
        plt.plot(numTruck_values, custom_metrics, marker='o', label=f'numExc = {numExc}')

    plt.xlabel('Number of Trucks')
    plt.ylabel('Unit Cost ($/Lcy)')
    plt.title('Plot of Unit Cost vs Number of Trucks')
    plt.legend()
    plt.show()

initialize_plot()
manager = ProcessManager(path_to_exe)


try:
    message = "LOAD C:/Users/Joseph/Desktop/EarthMoving.jstrx;"
    manager.write_message(message)
    for i in range(1, 4):
        for j in range(6, 20):
            message = textwrap.dedent(f"""\
            SETATTRIBUTE Soil InitialContent 1000;
            SETATTRIBUTE ExcWt InitialContent {i};
            SETATTRIBUTE TrkWt InitialContent {j};
            RUNMODEL;
            GETRESULTS;
            RESETMODEL;""")
            manager.write_message(message)
    manager.write_message("CLOSE;")
    communication_complete = False

    while not communication_complete:
        response = manager.read_messages()
        if response:
            if "COMPLETE" in response:
                communication_complete = True
            else:
                process_incoming_json(response)
        else:
            time.sleep(0.1)  # Sleep briefly to avoid busy waiting

finally:
    plt.ioff()  
    plt.show()  
    exitCode = manager.cleanup()
    #plot_truck_vs_custom_metric(json_data_array)
    #plot_values_from_array()
