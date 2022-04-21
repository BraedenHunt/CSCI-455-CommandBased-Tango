import threading
from queue import Queue
import speech_recognition as sr


class SpeechListener:

    TEXT_MODE = False

    def __init__(self):
        self.phrases_heard : Queue = Queue()
        listening_thread = threading.Thread(target=self.listen)
        listening_thread.setDaemon(True)
        listening_thread.start()


    def has_heard(self, phrase: str):
        while not self.phrases_heard.empty():
            heard_phrase = self.phrases_heard.get()
            if phrase in heard_phrase:
                self.clear_history()
                return True
        return False

    def clear_history(self):
        self.phrases_heard.queue.clear()

    def listen(self):
        while True:
            if self.TEXT_MODE:
                print("Waiting for text input: ")
                word = input()
                print(word)
                self.phrases_heard.put(word)
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
                        print(word)
                        self.phrases_heard.put(word)
                    except sr.UnknownValueError:
                        print("I didn't understand that")


