import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit

listener = sr.Recognizer()
player = pyttsx3.init()

with sr.Microphone() as input_device:
    print("I am ready, Listening ....")
    voice_content = listener.listen(input_device)
    text_command = listener.recognize_google(voice_content, language= 'id')
    text_command = text_command.lower()
    print(text_command)


