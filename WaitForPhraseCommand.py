from Command import Command
from SpeechRecognition import SpeechListener

class WaitForPhraseCommand(Command):

    def __init__(self, speech:SpeechListener, phrase:str):
        self.phrase = phrase
        self.speech = speech

    def initialize(self, time):
        self.initialized = True
        self.speech.clear_history()

    def is_finished(self):
        return self.speech.has_heard(self.phrase)