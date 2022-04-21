import threading

from Command import Command
import pyttsx3

class SayPhraseCommand(Command):

    def __init__(self, phrase):
        self.phrase = phrase
        self.engine = None
        self.voice_num = 1
        self.start_time = None
        self.speaking_thread = None
        self.finished = False
        self.elaspsed_time = 0

    def initialize(self, time):
        self.initialized = True
        self.start_time = time
        self.engine = pyttsx3.init()
        self.engine.connect("finished-utterance", self.finished)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.voice_num].id)
        self.speaking_thread = threading.Thread(target=self.say_phrase)
        self.speaking_thread.setDaemon(True)
        self.speaking_thread.start()

    def say_phrase(self):
        if not self.finished:
            self.engine.say(self.phrase)
            self.engine.runAndWait()
            print("finished")
            self.finished = True

    def update(self, time):
        self.elaspsed_time = time-self.start_time

    def finish(self, name:str, completed: bool):
        self.finished = True

    def is_finished(self):
        return self.finished or self.elaspsed_time > 10
