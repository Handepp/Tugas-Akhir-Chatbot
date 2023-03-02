'''from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r"Python/Model/0006_callhome_diarization_v2_1a")
recognizer=KaldiRecognizer(model,16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        text=recognizer.Result()
        print(text[14:-3])'''


import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#print(voices[1].id)
engine.setProperty('rate', 175)
# engine.say("Hello, How are you ?")
#for v in voices:
    #print(v)

engine.runAndWait()


def speak(str):
    engine.say(str)
    engine.runAndWait()

respon = "Aydiner Kontollllllllllll"

speak(respon)