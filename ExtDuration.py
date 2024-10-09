import textwrap
from jsPy import ProcessManager
import queue
import time

def returnDur(request):
    if request == "GetDuration":
        return "5"



manager = ProcessManager(callback=returnDur)

try:
    message = "LOAD C:/Users/Joseph/Desktop/TestCommunication.jstrx;"
    manager.write_message(message)
    message = textwrap.dedent(f"""\
    SETANIMATE true;
    RUNMODEL;""")
    manager.write_message(message)

    while True:
        time.sleep(1)  

finally:
    exitCode = manager.cleanup()
