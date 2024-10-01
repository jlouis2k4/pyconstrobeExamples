
import os
import sys

package_path = r"C:\source\jStrobe\jsPy"#\jsPy"  # Change this to the actual path
if package_path not in sys.path:
    sys.path.append(package_path)

from jsPy import ProcessManager

def main():
    # Create an instance of ProcessManager
    manager = ProcessManager()  # Replace with your executable path


    # Send a simple message to the process
    try:
        manager.write_message("LOAD C:/Users/Joseph/Desktop/EarthMoving.jstrx;")
        manager.write_message(f"""\SETATTRIBUTE Soil InitialContent 1000;
SETATTRIBUTE ExcWt InitialContent 1;
SETATTRIBUTE TrkWt InitialContent 2;
RUNMODEL;
GETRESULTS;
RESETMODEL;""")
        manager.write_message("CLOSE;")
    except Exception as e:
        print(f"Error while writing message: {e}")

    # Read results from the process (optional)
    try:
        manager.read_messages()
    except Exception as e:
        print(f"Error while reading messages: {e}")

    # Clean up the process
    exit_code=manager.cleanup()
    #exit(exit_code)

if __name__ == "__main__":
    main()
