pyconstrobeExamples
===================

This folder contains a set of examples that demonstrate how Python can be used to open up, parametrize, and run ConStrobe models. It also shows how the output from ConStrobe can be used in Python to create visualizations. Finally, it shows how ConStrobe models opened from Python can query Python for specific data to be used in running in the model. 

Each example include a Python file along with a ConStrobe model, both with the same name. Notice that all Python code will have a callback function to handle incoming text from ConStrobe.

-----------------------------
1. Earthmoving1
-----------------------------
File(s): EarthMoving1.py and EarthMoving.jstrx
Description: Shows how we can run a series of ConStrobe models whose queues are populated by Python. Results from the ConStrobe model are used to plot a graph in Python as that model finishes its run. 

-----------------------------
2. Earthmoving2
-----------------------------
File(s): EarthMoving2.py and EarthMoving.jstrx
Description: Uses the same ConStrobe model as previous, but in this case, we use a more sophisticated strategy in searching for the excavator-truck combination that gives us the least unit cost. We change number of excavator after we see three consecutive increases in the number of trucks. 

-----------------------------
3. TestCommunication
-----------------------------
File(s): TestCommunication.py and TestCommunication.jstrx
Description: It demonstrates how we can send and receive data between ConStrobe and Python using the GET() and POST() functions in ConStrobe. 

-----------------------------
4. EarthMoving_Characterized
-----------------------------
File(s): EarthMoving_Characterized.py and EarthMoving_Characterized.jstrx
Description: A more sophisticated version of the previous case. 

-----------------------------
5. SimState
-----------------------------
File(s): SimState.py and SimState.jstrx
Description: It demonstrates how to send the state of the simulation to python. 



