import speech_recognition as sr
def SpeechToText():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Luisteren...")
        r.pause_treshhold = 1
        audio = r.listen(source)
    print("Recognizing...")
    antwoord = r.recognize_google(audio, language='nl-NL')
    print(f"Je zei: {antwoord}")

    return antwoord
SpeechToText()