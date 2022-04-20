import threading
from queue import Queue
import speech_recognition as sr


class SpeechRecognition:
    TEXT_MODE = False

    def __init__(self, queue:Queue):
        listening_thread = threading.Thread(target=self.listen, args=queue)

    def listen(self, queue:Queue):
        while True:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dynamic_energy_threshold = True
                try:
                    if self.TEXT_MODE:
                        print("Waiting for text input")
                        word = input()
                    else:
                        print("Listening")

                        audio = r.listen(source)
                        print("Got audio")
                        word = r.recognize_google(audio).lower()
                    print(word)
                    command = self.process_word(word)
                    queue.put(command)
                except sr.UnknownValueError:
                    print("I don't know that command")


    def process_word(self, word):
        if word == "look left":
            print('look left')
            #move head left
            c.increment_joint('head_twist',reverse=False)
        elif word == "look right":
            print('look right')
            #move head right
            c.increment_joint('head_twist',reverse=True)
        elif word  == "look up":
            print('look up')
            #move head up
            c.increment_joint('head_tilt',reverse=False)
        elif word == "look down":
            print('look down')
            #move head down
            c.increment_joint('head_tilt',reverse=True)
        elif word == "body left":
            print('body left')
            #move waist left
            c.increment_joint('body_twist',reverse=False)
        elif word == "body right":
            print('body right')
            #move waist right
            c.increment_joint('body_twist',reverse=True)
        elif word == "move forward":
            print('move forward')
            #move forward
           # c.stop_thread_driving()
            c.start_thread_driving(reverse = False)
        elif word == "move back":
            print('move backwards')
           # c.stop_thread_driving()
            #move backwards
            c.start_thread_driving(reverse = True)
        elif word == "stop":
            print("STOPING")
            c.stop_drive()
            #c.stop_thread_driving()
        elif word == "turn left":
            print('rotate left')
            #c.increment_joint('motor_dir', reverse = False)
            c.turn(left = True)
            #rotate left
        elif word == "turn right":
            print('rotate right')
            c.turn(left = False)
            #c.increment_joint('right_motor', reverse = False)
            #rotate right
            #TODO add a call to c.____

        elif word == "reset":
            print('reset positions')
            #reset servo and motor positions
            c.reset_positions()
            try:
                _threading.start_new_thread(c.reset_positions(), ())
            except:
                print("Unable to start thread")
        elif word == "speed one" or word == "speed 1":
            print("Speed 1...")
            c.set_speed(1)
        elif word == "speed two" or word == "speed 2" or word == "speed to" or word == "speed too":
            print("Speed 2")
            c.set_speed(2)
        elif word == "speed three" or word == "speed 3":
            print("Speed 3")
            c.set_speed(3)
        elif word == "exit":
            c.kill_thread_driving()
            return 1
        else:
            print("Unknown Command")

on_begin()
