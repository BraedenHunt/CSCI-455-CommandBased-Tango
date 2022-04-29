# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
import time

from Animation import Animation
from RobotContainer import RobotContainer
from DriveCommand import  DriveCommand
from queue import Queue

from ServoCommand import ServoCommand
from robotGUI import RobotGUI

CLOCK_RATE = 50.0 # HZ

def main():
    robot_container = RobotContainer()
    queue = robot_container.command_queue

    add_slash_commands(queue, robot_container)
    '''    animation_controller = Animation()
        animation_thread = threading.Thread(target=animation_controller.start)
        animation_thread.setDaemon(True)
        animation_thread.start()'''
    #window = RobotGUI(robot_container)
    #window.title("Robot Control GUI")
    #window.rowconfigure(0, minsize=480, weight=1)
    #window.columnconfigure(1, minsize=800, weight=1)
    #//window.geometry("800x480")
    command_thread = threading.Thread(target=run_commands, args=[queue])
    command_thread.setDaemon(True)
    command_thread.start()
    #window.mainloop()



def add_slash_commands(queue: Queue, robot_container:RobotContainer):
    inner_delay = 1
    between_delay = 1
    queue.put(ServoCommand(robot_container.shoulder_x, 1, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.bicep_flex, 1, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.shoulder_y, -1, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.wrist_flex, 0, delayed_end=between_delay))

    queue.put(ServoCommand(robot_container.shoulder_x, 0, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.bicep_flex, 0, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.shoulder_y, 0, delayed_end=inner_delay))
    queue.put(ServoCommand(robot_container.wrist_flex, 0, delayed_end=inner_delay))

def run_commands(queue):
    print("test")
    current_command = None
    start_time = time.time()  # time in seconds
    while True:
        current_time = time.time() - start_time  # time in seconds
        if current_command is None:
            if not queue.empty():
                current_command = queue.get()
                print("Current Command: " + str(current_command))
        else:
            if not current_command.initialized:
                print("Initializing")
                current_command.initialize(current_time)
                current_command.update(current_time)
            if not current_command.is_finished():
                #print("Updating")
                current_command.update(current_time)
            else:
                print("Ended Command")
                current_command.end(False)
                current_command = None
            time.sleep(1 / CLOCK_RATE)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
