import textwrap
from jsPy import ProcessManager
import queue
import time

numbers = ["1", "2", "3", "4", "5","6","7"]
ctr=0
endFlag=False

def returnDur(request):
    global ctr
    global endFlag
    if request == "GetDuration":
        str=numbers[ctr]
        ctr=ctr+1;
        if ctr==4:
            endFlag=True
        return str
manager = ProcessManager(callback=returnDur)
try:
    message = "LOAD C:/Users/Joseph/Desktop/TestCommunication.jstrx;"
    manager.write_message(message)
    message = textwrap.dedent(f"""\
    SETANIMATE true;
    RUNMODEL;""")
    manager.write_message(message)
    while endFlag==False:
        time.sleep(0.1)
finally:
    exitCode = manager.cleanup()
