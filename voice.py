import pyttsx3

def speak(text):
    if text and text.strip():

        engine = pyttsx3.init()

        voices = engine.getProperty('voices')

        # 🔥 select female voice (Windows usually index 1 = Zira)
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        # 🎯 tune voice to match CASCA personality
        engine.setProperty("rate", 160)   # slower = calmer
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()