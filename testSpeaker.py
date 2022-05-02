from TTSEngine import TTSEngine

def main():
    tts = TTSEngine()
    tts.say_phrase("hi", callback)
    tts.say_phrase("bye", callback)
    tts.say_phrase("nope", callback)


def callback(a,b):
    pass

if __name__ == "__main__":
    main()