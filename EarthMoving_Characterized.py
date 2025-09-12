import os
import textwrap
from pyconstrobe import ProcessManager
import queue
import time


numbers = ["1", "2", "3", "4", "5","6","7"]
ctr=0
endFlag=False

def MessageReceived(type,message):
    global ctr
    global endFlag    
    print(message)
    if type == "TRACE":
        print(message)
    elif type == "POST":
        print(message)
    elif type == "GET":
        return 0

manager = ProcessManager(callback=MessageReceived)
try:
    full_path=os.path.join(os.getcwd(),"Earthmoving_Characterized.jstrx")
    message = f"LOAD {full_path};"
    manager.write_message(message)
    message = textwrap.dedent(f"""\
    SETANIMATE true;
    RUNMODEL;""")
    manager.write_message(message)
    while manager.finishRunFlag==False:
        time.sleep(0.1)
    manager.write_message("CLOSE;")
finally:
    exitCode = manager.cleanup()
