import threading
from queue import Queue
import speech_recognition as sr

from Command import Command
from RobotContainer import RobotContainer
from ServoCommand import ServoCommand
from DriveCommand import DriveCommand

class SpeechRecognition:
    TEXT_MODE = True

    def __init__(self, queue: Queue, robot_container: RobotContainer):
        self.robot_container = robot_container
        self.speed = 1
        listening_thread = threading.Thread(target=self.listen, args=[queue])
        listening_thread.setDaemon(True)
        listening_thread.start()

    def listen(self, queue:Queue):
        while True:
            if self.TEXT_MODE:
                print("Waiting for text input: ")
                word = input()
            else:
                with sr.Microphone() as source:
                    r = sr.Recognizer()
                    r.adjust_for_ambient_noise(source)
                    r.dynamic_energy_threshold = True
                    try:

                        print("Listening")

                        audio = r.listen(source)
                        print("Got audio")
                        word = r.recognize_google(audio).lower()
                    except sr.UnknownValueError:
                        print("I don't know that command")
                        word = ""
            print(word)
            command = self.process_word(word)
            if command is None:
                continue
            elif isinstance(command, Command):
                queue.put(command)
            else:
                for c in command:
                    queue.put(c)

    def process_word(self, word):
        if word == "look left":
            print('look left')
            #move head left
            return ServoCommand(self.robot_container.head_twist, -1)
        elif word == "look right":
            print('look right')
            #move head right
            return ServoCommand(self.robot_container.head_twist, 1)
        elif word  == "look up":
            print('look up')
            #move head up
            return ServoCommand(self.robot_container.head_tilt, 1)
        elif word == "look down":
            print('look down')
            #move head down
            return ServoCommand(self.robot_container.head_tilt, -1)
        elif word == "body left":
            print('body left')
            #move waist left
            return ServoCommand(self.robot_container.waist, -1)
        elif word == "body right":
            print('body right')
            #move waist right
            return ServoCommand(self.robot_container.waist, 1)
        elif word == "move forward":
            print('move forward')
            #move forward
            return DriveCommand(self.robot_container.drivetrain, .5, self.speed, self.speed)
        elif word == "move back":
            print('move backwards')
           # c.stop_thread_driving()
            #move backwards
            return DriveCommand(self.robot_container.drivetrain, .5, -self.speed, -self.speed)
        elif word == "stop":
            print("STOPING")
            return DriveCommand(self.robot_container.drivetrain, 0, 0, 0)
        elif word == "turn left":
            print('rotate left')
            #c.increment_joint('motor_dir', reverse = False)
            return DriveCommand(self.robot_container.drivetrain, .5, -self.speed, self.speed)
        elif word == "turn right":
            print('rotate right')
            return DriveCommand(self.robot_container.drivetrain, .5, self.speed, -self.speed)
        elif word == "reset":
            print('reset positions')
            #reset servo and motor positions
            return [ServoCommand(self.robot_container.head_twist, 0), ServoCommand(self.robot_container.head_tilt, 0),
                    ServoCommand(self.robot_container.waist, 0), DriveCommand(self.robot_container.drivetrain, 0, 0, 0)]
        elif word == "speed one" or word == "speed 1":
            print("Speed 1...")
            self.speed = 1
            return
        elif word == "speed two" or word == "speed 2" or word == "speed to" or word == "speed too":
            print("Speed 2")
            self.speed = 2
            return
        elif word == "speed three" or word == "speed 3":
            print("Speed 3")
            self.speed = 3
            return
        else:
            print("Unknown Command")

