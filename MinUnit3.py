# main.py

import json
import textwrap
import matplotlib.pyplot as plt
from jsPy import ProcessManager
import queue
import time

# Initialize a queue for inter-thread communication
message_queue = queue.Queue()

def process_incoming_json(json_string):
    try:
        parsed_data = json.loads(json_string)
        message_queue.put(parsed_data)  # Put parsed data into the queue for processing
    except json.JSONDecodeError:
        print("Invalid JSON string")

series_data = {}
fig, ax = plt.subplots()
custom_metric_history = []  # Keep track of the last three custom metrics

def initialize_plot():
    """Initializes the plot."""
    plt.ion()  # Enable interactive mode
    ax.set_xlabel('Number of Trucks')
    ax.set_ylabel('Unit Cost ($/Lcy)')
    ax.set_title('Plot of Unit Cost vs Number of Trucks')
    plt.show()

def update_plot(entry):
    global custom_metric_history  # Access the history variable
    returnValue=False
    numExc = entry["ExcWt.CurCount"]
    numTruck = entry["TrkWt.CurCount"]
    SimTime = entry["SimTime"]
    custom_metric = (numTruck * 1000 + numExc * 1000 + ((numTruck * 250 + numExc * 300) * SimTime / 60)) / 15000

    if numExc not in series_data:
        series_data[numExc] = ([], [])  # (numTruck values, custom_metric values)
    
    # Append values to the respective series
    series_data[numExc][0].append(numTruck)
    series_data[numExc][1].append(custom_metric)

    # Add current custom_metric to the history
    custom_metric_history.append(custom_metric)
    if len(custom_metric_history) > 3:  # Keep only the last three entries
        custom_metric_history.pop(0)

    # Check if we have three consecutive increases
    if len(custom_metric_history) == 3 and all(custom_metric_history[i] < custom_metric_history[i + 1] for i in range(2)):
        print("Three consecutive increases detected, breaking the inner loop.")
        returnValue=True  # Return True to indicate a break condition
        custom_metric_history = []

    ax.clear()
    ax.set_xlabel('Number of Trucks')
    ax.set_ylabel('Unit Cost ($/Lcy)')
    ax.set_title('Plot of Unit Cost vs Number of Trucks')

    # Plotting the data
    for numExc, (numTruck_values, custom_metrics) in series_data.items():
        ax.plot(numTruck_values, custom_metrics, marker='o', label=f'numExc = {numExc}')
    
    ax.legend()
    plt.draw()
    plt.pause(0.1)  # Pause to allow the plot to update
    
    return returnValue  # Return False to indicate no break condition

# Initialize
initialize_plot()
manager = ProcessManager(process_incoming_json)

try:
    message = "LOAD C:/Users/Joseph/Desktop/EarthMoving.jstrx;"
    manager.write_message(message)
    previous_best = 6
    for i in range(2, 10):
        for j in range(previous_best, 40, 2):
            message = textwrap.dedent(f"""\
            SETANIMATE false;
            SETATTRIBUTE Soil InitialContent 15000;
            SETATTRIBUTE ExcWt InitialContent {i};
            SETATTRIBUTE TrkWt InitialContent {j};
            RUNMODEL;
            GETRESULTS;
            RESETMODEL;""")
            manager.write_message(message)
            communication_complete = False
            breakFlag = False
            while not communication_complete:
                if not message_queue.empty():
                    entry = message_queue.get_nowait()
                    breakFlag=update_plot(entry)
                    communication_complete = True  # We received a response for this iteration

            # Allow the plot to update in real-time
            try:
                plt.pause(0.1)
            except Exception as e:
                print(f"Error during plt.pause: {e}")
            if breakFlag: 
                previous_best=j-6;
                break
            else:
                continue

    # Close after the loop is finished
    manager.write_message("CLOSE;")


    
finally:
    plt.ioff()  
    plt.show()  
    exitCode = manager.cleanup()
