import numpy as np
import time
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from transformers import BertTokenizer
from transformers import TFBertForSequenceClassification

from keras.models import load_model
import random
import serial

import speech_recognition as sr
import pyttsx3

import keyboard

from fungsi import *
from Waktu import *

import warnings
warnings.filterwarnings("ignore")

def Replace(value):
    value1 = float(value)
    value1 = round(value1,0)
    value1 = int(value1)
    value1 = str(value1)
    return value1
    
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()

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

def arduino_write(write,read):
    #arduino.write(command)
    print("test")       

def response(chat) :
    prechat = text_preprocessing_process(chat)
    input_text_tokenized = bert_tokenizer.encode(prechat,
                                             truncation=True,
                                             padding='max_length',
                                             return_tensors='tf')

    bert_predict = bert_load_model(input_text_tokenized)          # Lakukan prediksi
    bert_predict = tf.nn.softmax(bert_predict[0], axis=-1)         # Softmax function untuk mendapatkan hasil klasifikasi
    output = tf.argmax(bert_predict, axis=1)
    print(bert_predict)
    print(output)

    
    response_tag = le.inverse_transform([output])[0]
    respons = random.choice(responses[response_tag])

    if(response_tag == 'SaVi.maju'):
        arduino_write(str.encode('{"chatbot":"Maju"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.mundur'):
        arduino_write(str.encode('{"chatbot":"Mundur"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.stop'):
        arduino_write(str.encode('{"chatbot":"Stop"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.slow'):
        arduino_write(str.encode('{"chatbot":"lambat"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.medium'):
        arduino_write(str.encode('{"chatbot":"sedang"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.fast'):
        arduino_write(str.encode('{"chatbot":"cepat"}'))
        print(respons)
        speak(respons)
        time.sleep(1)
    
    elif(response_tag == 'SaVi.kanan'):
        arduino_write(str.encode('{"mode":"hall", "direct":"right"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.kiri'):
        arduino_write(str.encode('{"mode":"hall", "direct":"left"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.suhu'):
        arduino_write(str.encode('{"chatbot":"temp"}'))
        data = arduino.readline().decode("utf-8").strip('\n').strip('\r')
        data = Replace(data)
        print(data)
        print(respons + " " + data + " " + "derajat celcius")
        speak(respons + " " + data + " " + "derajat celcius")

    elif(response_tag == 'SaVi.hump'):
        arduino_write(str.encode('{"chatbot":"hum"}'))
        data = arduino.readline().decode("utf-8").strip('\n').strip('\r')
        data = Replace(data)
        print(data)
        print(respons + " " + data + " " + "RH")
        speak(respons + " " + data + " " + "RH")

    elif(response_tag == 'SaVi.jam'):
        print(respons + ' ' + get_time("%H %M") + ' ' + part)
        speak(respons + ' ' + get_time("%H %M") + ' ' + part)

    elif(response_tag == 'SaVi.hari'):
        print(respons + ' ' + get_time("%A"))
        speak(respons + ' ' + get_time("%A")) 

    elif(response_tag == 'SaVi.tanggal'):
        print(respons + ' ' + get_time("%d %B %Y"))
        speak(respons + ' ' + get_time("%d %B %Y")) 

    else:
        print(respons)
        speak(respons)

if __name__ == '__main__':
    listener = sr.Recognizer()
    player = pyttsx3.init()

    #arduino = serial.Serial('COM3',115200)

    #Pretrained Model
    PRE_TRAINED_MODEL = 'indobenchmark/indobert-base-p2'

    #Load tokenizer dari pretrained model
    bert_tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL)

    # Load hasil fine-tuning
    bert_load_model = TFBertForSequenceClassification.from_pretrained(PRE_TRAINED_MODEL, num_labels=35)
    bert_load_model.load_weights('Python/Model/bert-SAVI_1.h5')

    speak(random.choice(responses[classes[11]]))
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

         