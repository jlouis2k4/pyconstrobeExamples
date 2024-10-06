
# main.py

import json
import textwrap
import matplotlib.pyplot as plt
from jsPy import ProcessManager

# Fixed path to executable
# path_to_exe = r"C:\source\jStrobe\jsApp\Debug\jStrobe.exe"
json_data_array = []

def process_incoming_json(json_string):
    try:
        parsed_data = json.loads(json_string)
        json_data_array.append(parsed_data)
        return update_plot(parsed_data)
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
    custom_metric = ((numTruck * 250 + numExc * 300) *SimTime/60)/15000
    #custom_metric = (numTruck*1000+numExc*1000+((numTruck * 250 + numExc * 300) *SimTime/60))/15000

    # Initialize the series if it doesn't exist
    if numExc not in series_data:
        series_data[numExc] = ([], [])  # (numTruck values, custom_metric values)

    # Append values to the respective series
    series_data[numExc][0].append(numTruck)
    series_data[numExc][1].append(custom_metric)

    # Clear the axis to redraw
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
    return custom_metric

# Example usage

initialize_plot()
manager = ProcessManager()#path_to_exe)


try:
    message = "LOAD C:/Users/Joseph/Desktop/EarthMoving.jstrx;"
    manager.write_message(message)
    ideal_num_truck=6
    for i in range(2, 10):
        consecutive_increases = 0  
        previous_cost = float('inf')  

        for j in range(ideal_num_truck, 40, 2):
            message = textwrap.dedent(f"""\
            SETANIMATE false;
            SETATTRIBUTE Soil InitialContent 15000;
            SETATTRIBUTE ExcWt InitialContent {i};
            SETATTRIBUTE TrkWt InitialContent {j};
            RUNMODEL;
            GETRESULTS;
            RESETMODEL;""")
            manager.write_message(message)

            # Read the response
            response = manager.read_messages()
            
            if response:
                if "COMPLETE" in response:
                    communication_complete = True
                else:
                    # Process the response and calculate the unit cost
                    unit_cost = process_incoming_json(response)
            else:
                time.sleep(0.1)  # Sleep briefly to avoid busy waiting
            
            # Check if unit cost has increased
            if unit_cost > previous_cost:
                consecutive_increases += 1
            else:
                consecutive_increases = 0  # Reset if unit cost doesn't increase

            # Update the previous cost
            previous_cost = unit_cost

            # Break the inner loop if there are 3 consecutive increases
            if consecutive_increases >= 3:
                print(f"Breaking inner loop at i={i}, j={j} due to 3 successive increases in unit cost")
                ideal_num_truck=j-8
                break
    
    # Close the connection after the loop
    manager.write_message("CLOSE;")
    communication_complete = False

except Exception as e:
    print(f"An error occurred: {e}")


finally:
    plt.ioff()  
    plt.show()  
    exitCode = manager.cleanup()
