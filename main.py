# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from RobotContainer import RobotContainer
from queue import Queue
from SpeechRecognition import SpeechRecognition

def main():
    robot_container = RobotContainer()
    queue = Queue()
    speech = SpeechRecognition(queue, robot_container)
    current_command = None
    start_time = time.time() # time in seconds
    while True:
        current_time = time.time()-start_time # time in seconds
        if current_command is None:
            if not queue.empty():
                current_command = queue.get()
        else:
            if not current_command.initialized:
                current_command.initialize(current_time)
            if not current_command.is_finished():
                current_command.update(current_time)
            else:
                print("Ended Command")
                current_command = None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
