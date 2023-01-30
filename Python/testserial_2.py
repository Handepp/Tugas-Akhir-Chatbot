import pandas as pd
import numpy as np
import re
import pickle
import nltk
import serial
import time
from sklearn.feature_extraction.text import CountVectorizer
from fungsi import *
from joblib import load
import numpy

import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit

listener = sr.Recognizer()
player = pyttsx3.init()

#cek123

arduino = serial.Serial('COM3',115200)
time.sleep(2)
model = load('testwahana.model')
vocab = pickle.load(open('bow.pickle', 'rb'))
bow = CountVectorizer(ngram_range=(1,1))  

def forward_150():
    forward_150 = arduino.write(str.encode('{"direction1":"forward","steps1":"30","speed1":"150","direction2":"forward","steps2":"30","speed2":"250"}'))

def stop_0():
    stop_0=arduino.write(str.encode('{"direction1":"stop","steps1":"0","speed1":"0","direction2":"stop","steps2":"0","speed2":"0"}--'))


def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source)
        print("Now listening")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Deciphering")   
        query = r.recognize_google(audio, language ='id')
        print("You Said: " + query)
  
    except Exception as e:
        print(e)
        print("Did not hear anything") 
        return "None"
     
    return query

takeCommand()


    
chat = input("🧑 Kamu\t: ")       
chat = text_preprocessing(chat)
chat = vocab.transform([chat])          # Feature extraction. Mengubah teks menjadi vektor

res = model.predict_proba(chat)         # Prediksi vektor teks kedalam model machine learning

max_prob = max(res[0])                # Ambil nilai probabilitas & index lokasinya
max_idx = np.argmax(res[0])
print(f"Max Prob : {max_prob}\nMax Index: {max_idx}\nLabel: {model.classes_[max_idx]}")

if(model.classes_[max_idx] == 'Wahana Maju'):
    forward_150()
    print("Wahana Maju")
    time.sleep(1)

if(model.classes_[max_idx] == 'Wahana Berhenti'):
    stop_0()
    print("Wahana Berhenti")



