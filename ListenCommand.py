from Command import Command
from SpeechRecognition import SpeechListener

class ListenCommand(Command):

    def __init__(self, speech:SpeechListener):
        self.speech = speech

    def initialize(self, time):
        self.initialized = True
        self.speech.clear_history()

    def is_finished(self):
        return not self.speech.phrases_heard.empty()