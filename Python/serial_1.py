import numpy as np
import pickle
import time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from fungsi import *
from joblib import load
import random
import serial

import speech_recognition as sr
import pyttsx3
import gtts
import playsound

import keyboard

import warnings
warnings.filterwarnings("ignore")

def Replace(value):
    value1 = float(value)
    value1 = round(value1,0)
    value1 = int(value1)
    value1 = str(value1)
    return value1

def speak(text):
    tts = gtts.gTTS(text=text, lang='id')
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    tts.save(filename)
    playsound.playsound(filename)

def chatbot ():
    #global chat
    chat = input("🧑 Kamu\t: ")
    return chat

def voice ():
    r = sr.Recognizer()
     
    with sr.Microphone(device_index=1) as source:
        r.adjust_for_ambient_noise(source)
        print("Berbicara")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Mengolah")   
        query = r.recognize_google(audio, language ='id')
        print("Kamu Berbicara: " + query)
  
    except Exception as e:
        print(e)
        print("Tidak dapat mendengar apapun") 
        return "None"
     
    return query       

def response(chat) :
    prechat = text_preprocessing_process(chat)
    vocabchat = vocab.transform([prechat])
    res = model.predict_proba(vocabchat)
    max_prob = max(res[0])                
    max_idx = np.argmax(res[0])
    print(f"Max Prob : {max_prob}\nMax Index: {max_idx}\nLabel: {model.classes_[max_idx]}")
    respons = random.choice(responses[model.classes_[max_idx]])
    
    #if(model.classes_[max_idx] == 'Wahana Maju'):
        #forward_150()
        #print("Wahana Majuuu")
        #time.sleep(1)

    #if(model.classes_[max_idx] == 'Wahana Berhenti'):
        #stop_0()
        #print("Wahana Berhenti")

    if(model.classes_[max_idx] == 'wardas.suhu'):
        arduino.write(str.encode('{"chatbot":"temp"}'))
        data = arduino.readline().decode("utf-8").strip('\n').strip('\r')
        data = Replace(data)
        print(data)
        print(respons + " " + data + " " + "derajat celcius")
        speak(respons + " " + data + " " + "derajat celcius")

    if(model.classes_[max_idx] == 'wardas.hump'):
        arduino.write(str.encode('{"chatbot":"hump"}'))
        data = arduino.readline().decode("utf-8").strip('\n').strip('\r')
        data = Replace(data)
        print(data)
        print(respons + " " + data + " " + "RH")
        speak(respons + " " + data + " " + "RH")

    else:
        speak(respons)

if __name__ == '__main__':
    listener = sr.Recognizer()
    player = pyttsx3.init()

    arduino = serial.Serial('COM3',115200)
    time.sleep(1)

    tf_idf = TfidfVectorizer(ngram_range=(1,1))
    vocab = pickle.load(open('Python/Model/Token_TFIDF1.pickle', 'rb'))
    model = load('Python/Model/DT.model')
    
    while True:
        print("tekan a untuk chat, tekan b untuk voice, tekan q untuk quit")
        if keyboard.read_key()== "a":
            response(chatbot())  
        
        elif keyboard.read_key()== "b":
            response(voice())
        
        elif keyboard.read_key()== "q":
            break

        else:
            print("Perintah tidak ada")

         