#include <ArduinoJson.h>
#include <DHT.h>
// GPIO mappings for Arduino Mega 2560

int m1_EL_Start_Stop=7;  //EL 
int m1_Signal_hall=6;   // Signal - Hall sensor
int m1_ZF_Direction=5;  // ZF 
int m1_VR_speed=4;    //VR 

int m2_EL_Start_Stop=11;  //EL 
int m2_Signal_hall=10;   // Signal - Hall sensor
int m2_ZF_Direction=9;  // ZF 
int m2_VR_speed=8;    //VR 

DHT dht(3, DHT11);

int pos1=0;
int steps1=0;
int speed1=0;

int pos2=0;
int steps2=0;
int speed2=0;

String direction1; 
String direction2;

void plus1() {
  pos1++; //count steps
  Serial.println(pos1);
    if(pos1>=steps1){
    wheel1Stop();
    pos1=0;
  }
}

void plus2() {
  pos2++; //count steps
  Serial.println(pos2);
    if(pos2>=steps2){
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
  attachInterrupt(digitalPinToInterrupt(m2_Signal_hall), plus2, CHANGE);
  //Hall sensor detection - Count steps
  attachInterrupt(digitalPinToInterrupt(m1_Signal_hall), plus1, CHANGE);

   dht.begin();

}


void drive(){
  // {"direction2":"forward","steps2":"30","speed2":"50"}
  // {"direction1":"forward","steps1":"30","speed1":"50","direction2":"forward","steps2":"30","speed2":"50"}
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


void wheel1Stop(){
  digitalWrite(m1_EL_Start_Stop,LOW);
}

void wheel2Stop(){
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
  float suhu = dht.readTemperature();
  float kelembapan = dht.readHumidity();
  Serial.println(suhu);
  Serial.println(kelembapan);
  delay(1000);
  if (Serial.available()>0) 
  {
    String command=Serial.readString();
    DynamicJsonBuffer jsonBuffer;
    JsonObject& root= jsonBuffer.parseObject(command);
    if (root.success()) {
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
