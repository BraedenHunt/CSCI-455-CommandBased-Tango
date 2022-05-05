# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
import time
from tkinter import Tk

from Animation import Animation
from ListenCommand import ListenCommand
from RobotContainer import RobotContainer
from DriveCommand import  DriveCommand
from queue import Queue

from SayPhraseCommand import SayPhraseCommand
from ServoCommand import ServoCommand
from adventureDriver.adventureDriver import Game
from robotGUI import RobotGUI
from robot_animations import Window

CLOCK_RATE = 50.0 # HZ

def main():
    robot_container = RobotContainer()
    queue = robot_container.command_queue

    #add_slash_commands(queue, robot_container)
    #robot_container.add_drink_commands()

    command_thread = threading.Thread(target=run_commands, args=[queue])
    command_thread.start()
    '''
    queue.put(SayPhraseCommand(robot_container.speaker, "Hello World"))
    listen_command = ListenCommand(robot_container.speech_listener)
    queue.put(listen_command)
    while robot_container.speech_listener.phrases_heard.empty():
        pass
    queue.put(SayPhraseCommand(robot_container.speaker, listen_command.phrase))
    '''



    root = Tk()
    app = Window(root)
    root.wm_title("Background")
    root.geometry("800x480")
    '''
    app.loadImage("guiPics/dungeon_three.jpeg")
    app.drinkPotion("guiPics/potion5.gif")
    app.loadBlade("guiPics/blade.gif")
    app.loadEnemy("guiPics/orc.gif", 1)
    app.loadEnemy("guiPics/slime.gif", 2)
    app.loadEnemy("guiPics/demon.gif", 3)
    app.loadKey("guiPics/key.jpeg")
    app.healthBar(100)
    '''

    game_driver_thread = threading.Thread(target=run_game_driver, args=[queue, robot_container, app])
    game_driver_thread.start()

    root.mainloop()


def run_game_driver(queue: Queue, robot_container, app: Window):
    g = Game(queue, robot_container, False, app)
    g.play()


def run_commands(queue):
    print("test")
    current_command = None
    start_time = time.time()  # time in seconds
    while True:
        current_time = time.time() - start_time  # time in seconds
        if current_command is None:
            if not queue.empty():
                current_command = queue.get()
                #print("Current Command: " + str(current_command))
        else:
            if not current_command.initialized:
                #print("Initializing")
                current_command.initialize(current_time)
                current_command.update(current_time)
            if not current_command.is_finished():
                #print("Updating")
                current_command.update(current_time)
            else:
                #print("Ended Command")
                current_command.end(False)
                current_command = None
            time.sleep(1 / CLOCK_RATE)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
