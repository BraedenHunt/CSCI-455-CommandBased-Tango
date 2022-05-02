import threading

from Command import Command
from TTSEngine import TTSEngine
import pyttsx3

class SayPhraseCommand(Command):

    def __init__(self, tts_engine, phrase):
        self.phrase = phrase
        self.tts_engine = tts_engine
        self.start_time = None
        self.finished = False
        self.elaspsed_time = 0

    def initialize(self, time):
        self.initialized = True
        self.start_time = time
        self.say_phrase()
        
    def say_phrase(self):
        if not self.finished:
            self.tts_engine.say_phrase(self.phrase, self.finish)

    def update(self, time):
        self.elaspsed_time = time-self.start_time

    def finish(self, name:str, completed: bool):
        print("finish called")
        self.finished = True

    def is_finished(self):
        return self.finished
