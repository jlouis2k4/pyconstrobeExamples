import os
import json
import textwrap
import matplotlib.pyplot as plt
from pyJStrobe import ProcessManager
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

def initialize_plot():
    """Initializes the plot."""
    plt.ion()  # Enable interactive mode
    ax.set_xlabel('Number of Trucks')
    ax.set_ylabel('Unit Cost ($/Lcy)')
    ax.set_title('Plot of Unit Cost vs Number of Trucks')
    plt.show()

def update_plot(entry):
    numExc = entry["ExcWt.CurCount"]
    numTruck = entry["TrkWt.CurCount"]
    SimTime = entry["SimTime"]
    custom_metric = (numTruck * 1000 + numExc * 1000 + ((numTruck * 250 + numExc * 300) * SimTime / 60)) / 15000 #unit cost in $/cy
    if numExc not in series_data:
        series_data[numExc] = ([], [])  # (numTruck values, custom_metric values)
    series_data[numExc][0].append(numTruck)
    series_data[numExc][1].append(custom_metric)
    ax.clear()
    ax.set_xlabel('Number of Trucks')
    ax.set_ylabel('Unit Cost ($/Lcy)')
    ax.set_title('Plot of Unit Cost vs Number of Trucks')
    for numExc, (numTruck_values, custom_metrics) in series_data.items():
        ax.plot(numTruck_values, custom_metrics, marker='o', label=f'numExc = {numExc}')
    ax.legend()
    plt.draw()

# Initialize
initialize_plot()
manager = ProcessManager(process_incoming_json)

try:
    full_path=os.path.join(os.getcwd(),"EarthMoving.jstrx")
    message = f"LOAD {full_path};"
    manager.write_message(message)
    for i in range(2, 4):
        for j in range(6, 40, 2):
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
            while not communication_complete:
                if not message_queue.empty():
                    entry = message_queue.get_nowait()  # Non-blocking
                    update_plot(entry)
                    communication_complete = True
            try:
                plt.pause(0.1)
            except Exception as e:
                print(f"Error updating plot: {e}")
    
    manager.write_message("CLOSE;")

finally:
    plt.ioff()  
    plt.show()  
    exitCode = manager.cleanup()
