
from fungsi import *
import serial
from keras.models import load_model

def response(chat) :
    prechat = text_preprocessing_process(chat)
    input_text_tokenized = bert_tokenizer.encode(prechat,
                                             truncation=True,
                                             padding='max_length',
                                             return_tensors='tf')

    bert_predict = bert_load_model(input_text_tokenized)          # Lakukan prediksi
    bert_predict = tf.nn.softmax(bert_predict[0], axis=-1)         # Softmax function untuk mendapatkan hasil klasifikasi
    output = tf.argmax(bert_predict, axis=1)


    response_tag = le.inverse_transform([output])[0]
    respons = random.choice(responses[response_tag])

    if(response_tag == 'SaVi.maju'):
        arduino.write(str.encode('{"chatbot":"Maju"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.mundur'):
        arduino.write(str.encode('{"chatbot":"Mundur"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.stop'):
        arduino.write(str.encode('{"chatbot":"Stop"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.slow'):
        arduino.write(str.encode('{"chatbot":"lambat"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.medium'):
        arduino.write(str.encode('{"chatbot":"sedang"}'))
        print(respons)
        speak(respons)
        time.sleep(1)

    elif(response_tag == 'SaVi.fast'):
        arduino.write(str.encode('{"chatbot":"cepat"}'))
        print(respons)
        speak(respons)
        time.sleep(1)
    
    elif(response_tag == 'SaVi.kanan'):
        arduino.write(str.encode('{"mode":"hall", "direct":"right"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.kiri'):
        arduino.write(str.encode('{"mode":"hall", "direct":"left"}'))
        print(respons)
        speak(respons)

    elif(response_tag == 'SaVi.suhu'):
        arduino.write(str.encode('{"chatbot":"temp"}'))
        data = arduino.readline().decode("utf-8").strip('\n').strip('\r')
        data = Replace(data)
        print(data)
        print(respons + " " + data + " " + "derajat celcius")
        speak(respons + " " + data + " " + "derajat celcius")

    elif(response_tag == 'SaVi.hump'):
        arduino.write(str.encode('{"chatbot":"hum"}'))
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