import os
import textwrap
from pyJStrobe import ProcessManager
import queue
import time

numbers = ["1", "2", "3", "4", "5","6","7"]
ctr=0
endFlag=False

def returnDur(request):
    global ctr
    global endFlag
    print(request)
    if request == "GetDuration":
        str=numbers[ctr]
        ctr=ctr+1;
        if ctr==4:
            endFlag=True
        return str
       

manager = ProcessManager(callback=returnDur)
try:
    full_path=os.path.join(os.getcwd(),"TestCommunication.jstrx")
    message = f"LOAD {full_path};"
    manager.write_message(message)
    message = textwrap.dedent(f"""\
    SETANIMATE true;
    RUNMODEL;""")
    manager.write_message(message)
    while endFlag==False:
        time.sleep(0.1)
finally:
    exitCode = manager.cleanup()
