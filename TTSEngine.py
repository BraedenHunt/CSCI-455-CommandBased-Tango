import threading

import pyttsx3

class TTSEngine:

    def __init__(self):
        self.engine = pyttsx3.init()
        self.speaking_thread = None
        voices = self.engine.getProperty('voices')
        self.voice_num = 2
        self.engine.setProperty('voice', voices[self.voice_num].id)

    def say_phrase(self, phrase, callback: callable):
        self.speaking_thread = threading.Thread(target=self.speak, args=[phrase])
        self.engine.connect("finished-utterance", callback)
        self.speaking_thread.start()

    def speak(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()
        print("finished speaking")