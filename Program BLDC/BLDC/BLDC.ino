#include <ArduinoJson.h>
#include <DHT.h>

// Inisialisasi port BLDC
//int m1_EL_Start_Stop=7;  //EL 
//int m1_Signal_hall=3;   // Signal - Hall sensor
//int m1_ZF_Direction=5;  // ZF 
//int m1_VR_speed=4;    //VR 

//int m2_EL_Start_Stop=11;  //EL 
//int m2_Signal_hall=2;   // Signal - Hall sensor
//int m2_ZF_Direction=9;  // ZF 
//int m2_VR_speed=8;    //VR

//int m1_EL_Start_Stop=11;  //EL 
//int m1_Signal_hall=3;   // Signal - Hall sensor
//int m1_ZF_Direction=9;  // ZF 
//int m1_VR_speed=8;    //VR 

//int m2_EL_Start_Stop=6;  //EL 
//int m2_Signal_hall=2;   // Signal - Hall sensor
//int m2_ZF_Direction=5;  // ZF 
//int m2_VR_speed=4;    //VR

int m1_EL_Start_Stop=8;  //EL 
int m1_Signal_hall=3;   // Signal - Hall sensor
int m1_ZF_Direction=10;  // ZF 
int m1_VR_speed=11;    //VR 

int m2_EL_Start_Stop=4;  //EL 
int m2_Signal_hall=2;   // Signal - Hall sensor
int m2_ZF_Direction=5;  // ZF 
int m2_VR_speed=6;    //VR

// Inisialisasi port DHT11
DHT dht(13, DHT11);

// Define value variable 
int pos1=0;
int steps1=0;
int speed1=0;

int pos2=0;
int steps2=0;
int speed2=0;

String direction1; 
String direction2;
String chatbot;

void plus1() {
  pos1++; //count steps
  Serial.print("Pos 1 : ");
  Serial.println(pos1);
  if(pos1>=steps1)
  {
    wheel1Stop();
    pos1=0;
  }
}

void plus2() {
  pos2++; //count steps
  Serial.print("Pos 2 : ");
  Serial.println(pos2);
  if(pos2>=steps2)
  {
    wheel2Stop();
    pos2=0;
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  //wheel 1 - Setup pin mode
  pinMode(m1_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(m1_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(m1_ZF_Direction, OUTPUT); //direction  - ZF 
  
  //wheel 2 - Setup pin mode
  pinMode(m2_EL_Start_Stop, OUTPUT);//stop/start - EL 
  pinMode(m2_Signal_hall, INPUT);   //plus       - Signal  
  pinMode(m2_ZF_Direction, OUTPUT); //direction  - ZF 

  //Hall sensor detection - Count steps
  attachInterrupt(digitalPinToInterrupt(m1_Signal_hall), plus1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(m2_Signal_hall), plus2, CHANGE);

   dht.begin();

}


void drive(){
  // {"direction1":"forward","steps1":"30","speed1":"50","direction2":"forward","steps2":"30","speed2":"50"}
  // {"direction1":"forward","steps1":"2000","speed1":"100","direction2":"forward","steps2":"2000","speed2":"100"}
  // {"direction1":"backward","steps1":"30","speed1":"50","direction2":"backward","steps2":"30","speed2":"50"}
  // {"direction1":"stop","steps1":"0","speed1":"0","direction2":"stop","steps2":"0","speed2":"0"}--
  
  if(direction1=="forward" && pos1<steps1)
  {
    wheel1MoveForward();
  }
  
  if (direction2=="forward" && pos2<steps2)
  {
    wheel2MoveForward();
  }
  
  else if(direction1=="backward" && pos1<steps1)
  {
    wheel1MoveBackward();
  }
  
  else if(direction2=="backward" && pos2<steps2)
  {
    wheel2MoveBackward();
  }
  
  else if(direction1=="stop" && direction2=="stop")
  {
    Serial.println("Wheel 1 & 2 Stop");
    wheel1Stop();
    pos1=0;
    wheel2Stop();
    pos2=0;    
  }
 }

 
void bot(){
  // {"chatbot":"temp"}
  // {"chatbot":"hum"}
  // {"chatbot":"lambat"}
  // {"chatbot":"sedang"}
  // {"chatbot":"cepat"}
  // {"chatbot":"Maju"}
  // {"chatbot":"Mundur"}
  // {"chatbot":"Stop"}
  // {"direction1":"forward","steps1":"30","speed1":"50","direction2":"forward","steps2":"30","speed2":"50"}

  if(chatbot =="Maju" && steps1==0 && steps2==0)
  {
    Forward();
  }

  if(chatbot =="Mundur")
  {
    Backward();
  }

   if(chatbot =="Stop")
  {
    Backward();
  }
  
  if(chatbot =="temp")
  {
    float suhu = dht.readTemperature();
    Serial.println(suhu);
  }

  if (chatbot == "hum")
  {
    float kelembapan = dht.readHumidity();
    Serial.println(kelembapan);
  }
  
  if (chatbot == "lambat")
  {
    analogWrite(m1_VR_speed, 75);
    analogWrite(m2_VR_speed, 75);
  }

  if (chatbot == "sedang")
  {
    analogWrite(m1_VR_speed, 125);
    analogWrite(m2_VR_speed, 125);
  }

  if (chatbot == "cepat")
  {
    analogWrite(m1_VR_speed, 200);
    analogWrite(m2_VR_speed, 200);
  }
}


void wheel1Stop(){
  digitalWrite(m1_EL_Start_Stop,LOW);
}

void wheel2Stop(){
  digitalWrite(m2_EL_Start_Stop,LOW);
}


void Forward(){
  analogWrite(m1_VR_speed, 125);
  analogWrite(m2_VR_speed, 125);

  digitalWrite(m1_EL_Start_Stop,LOW);
  digitalWrite(m2_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m1_ZF_Direction,LOW);
  digitalWrite(m2_ZF_Direction,HIGH);
  delay(1000);
  digitalWrite(m1_EL_Start_Stop,HIGH);
  digitalWrite(m2_EL_Start_Stop,HIGH);
}

void Backward(){
  analogWrite(m1_VR_speed, 50);
  analogWrite(m2_VR_speed, 50);

  digitalWrite(m1_EL_Start_Stop,LOW);
  digitalWrite(m2_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m1_ZF_Direction,HIGH);
  digitalWrite(m2_ZF_Direction,LOW);
  delay(1000);
  digitalWrite(m1_EL_Start_Stop,HIGH);
  digitalWrite(m2_EL_Start_Stop,HIGH);
}

void Stop(){
  digitalWrite(m1_EL_Start_Stop,LOW);
  digitalWrite(m2_EL_Start_Stop,LOW);
}


void wheel1MoveForward(){
  analogWrite(m1_VR_speed, speed1);
  digitalWrite(m1_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m1_ZF_Direction,LOW);
  delay(1000);
  digitalWrite(m1_EL_Start_Stop,HIGH);
}

void wheel2MoveForward(){
  analogWrite(m2_VR_speed, speed2);
  digitalWrite(m2_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m2_ZF_Direction,HIGH);
  delay(1000);
  digitalWrite(m2_EL_Start_Stop,HIGH);
}

void wheel1MoveBackward(){
  analogWrite(m1_VR_speed, speed1);
  digitalWrite(m1_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m1_ZF_Direction,HIGH);
  delay(1000);
  digitalWrite(m1_EL_Start_Stop,HIGH);
}

void wheel2MoveBackward(){
  analogWrite(m2_VR_speed, speed2);
  digitalWrite(m2_EL_Start_Stop,LOW);
  delay(1000);
  digitalWrite(m2_ZF_Direction,LOW);
  delay(1000);
  digitalWrite(m2_EL_Start_Stop,HIGH);
}

void loop() {
  //float suhu = dht.readTemperature();
  //float kelembapan = dht.readHumidity();
  //float suhu = dht.readTemperature();
  //Serial.println(suhu);
  //Serial.println(kelembapan);
  //delay(1000);
  if (Serial.available()>0) 
  {
    String command=Serial.readString();
    DynamicJsonBuffer jsonBuffer;
    JsonObject& root= jsonBuffer.parseObject(command);
    if (root.success()) {
      chatbot = root["chatbot"].asString(); 
      bot();

      direction1 = root["direction1"].asString();
      Serial.println(direction1);
      direction2 = root["direction2"].asString();
      Serial.println(direction2);
      steps1 = atoi(root["steps1"]); //atoi mengubah string menjadi nilai integer
      Serial.println(steps1);
      steps2 = atoi(root["steps2"]); //atoi mengubah string menjadi nilai integer
      Serial.println(steps2);
      speed1 = atoi(root["speed1"]);
      Serial.println(speed1);
      speed2 = atoi(root["speed2"]);
      Serial.println(speed2);
      drive();
      }
  }
  
}
