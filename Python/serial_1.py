import pandas as pd
import numpy as np
import re
import pickle
import nltk
import serial
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from fungsi import *
from joblib import load
import random


import speech_recognition as sr
import pyttsx3
import gtts
import playsound
import wikipedia
import pywhatkit

import keyboard

import warnings
warnings.filterwarnings("ignore")


def forward_150():
    forward_150 = arduino.write(str.encode('{"direction1":"forward","steps1":"30","speed1":"150","direction2":"forward","steps2":"30","speed2":"250"}'))

def speak(text):
    tts = gtts.gTTS(text=text, lang='id')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_response(intent):
  respons = random.choice(responses[intent])
  return respons

def chatbot ():
    global max_idx
    chat = input("🧑 Kamu\t: ")       
    chat = text_preprocessing_process(chat)
    print(chat)
    chat = vocab.transform([chat])
    print(chat)
    res = model.predict_proba(chat)
    max_prob = max(res[0])                # Ambil nilai probabilitas & index lokasinya
    max_idx = np.argmax(res[0])
    print(f"Max Prob : {max_prob}\nMax Index: {max_idx}\nLabel: {model.classes_[max_idx]}")
    respons = random.choice(responses[model.classes_[max_idx]])
    print(respons)
    speak(respons)
    #print(f"🤖 Bot\t: {get_response(model.classes_[max_idx])}")

def response() :
    if(model.classes_[max_idx] == 'Wahana Maju'):
        #forward_150()
        print("Wahana Majuuu")
        time.sleep(1)

    if(model.classes_[max_idx] == 'Wahana Berhenti'):
        #stop_0()
        print("Wahana Berhenti")


def voice ():
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




if __name__ == '__main__':
    listener = sr.Recognizer()
    player = pyttsx3.init()

    #arduino = serial.Serial('COM3',115200)
    time.sleep(1)

    tf_idf = TfidfVectorizer(ngram_range=(1,1))
    vocab = pickle.load(open('Python/Model/Token_TFIDF1.pickle', 'rb'))
    model = load('Python/Model/DT.model')
    
    while True:
        print("tekan a untuk chat, tekan b untuk voice, tekan q untuk quit")
        if keyboard.read_key()== "a":
            chatbot()
            response()  
        
        elif keyboard.read_key()== "b":
            voice()
            response()
        
        elif keyboard.read_key()== "q":
            break

        else:
            print("Perintah tidak ada")

         