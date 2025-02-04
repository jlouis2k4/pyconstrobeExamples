import os
import json
import textwrap
import matplotlib.pyplot as plt
from pyconstrobe import ProcessManager
import queue
import time

trace_message_queue = queue.Queue()

def process_incoming_json(json_string):
    try:
        #ConStrobe will return results of simulation as a JSON string.
        parsed_data = json.loads(json_string)
    except json.JSONDecodeError:
        #If we find that the return string is not of JSON format, we are assuming it is trace.
        # I am storing in the queue, and then I will process it later.
        trace_message_queue.put(json_string)


#full_path=os.path.join(os.getcwd(),"TraceReturn.jstrx")
full_path="C:\\source\\pyconstrobeExamples\\TraceReturn.jstrx"

manager = ProcessManager(process_incoming_json)
message = f"LOAD {full_path};"
manager.write_message(message)

message = textwrap.dedent(f"""\
            SETANIMATE false;
            SETATTRIBUTE Queue2 InitialContent 1;
            RUNMODEL;
            GETRESULTS;
            GETTRACE trace;
            RESETMODEL;""")
manager.write_message(message)
communication_complete = False
while not communication_complete:
    if not trace_message_queue.empty():
        entry = trace_message_queue.get_nowait()  # Non-blocking
        print(entry)
        communication_complete = True
manager.write_message("CLOSE;")
exitCode = manager.cleanup()