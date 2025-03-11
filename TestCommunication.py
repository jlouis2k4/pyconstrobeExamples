import os
import textwrap
from pyconstrobe import ProcessManager
import queue
import time
import debugpy

numbers = ["1", "2", "3", "4", "5","6","7"]
ctr=0
endFlag=False

def returnDur(type,message):
    global ctr
    global endFlag
    if type == "TRACE":
        print(message)
    if message == "GetDuration":
        response_str = ctr
        ctr += 1
        if ctr > 4:
            endFlag = True
        return response_str  # This is sent by `read_messages()`

       
debugpy.breakpoint()
manager = ProcessManager(callback=returnDur)
try:
    full_path=os.path.join(os.getcwd(),"TestCommunication.jstrx")
    message = f"LOAD {full_path};"
    manager.write_message(message)
    message = textwrap.dedent(f"""\
    SETANIMATE true;
    RUNMODEL;""")
    manager.write_message(message)
    while manager.finishRunFlag==False:
        time.sleep(0.1)
    manager.gotTraceFlag=False
    manager.write_message("GETTRACE trace;")
    while manager.gotTraceFlag==False:
        time.sleep(0.1)
    manager.write_message("CLOSE;")
finally:
    exitCode = manager.cleanup()
