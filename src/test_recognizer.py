import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Zeg iets...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="nl-NL")
    print("Je zei:", text)
except sr.UnknownValueError:
    print("Kon de spraak niet herkennen.")
except sr.RequestError:
    print("Er is een probleem met de Google API.")
