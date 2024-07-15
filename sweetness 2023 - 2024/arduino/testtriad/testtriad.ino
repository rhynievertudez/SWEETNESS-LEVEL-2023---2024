#include "SparkFun_AS7265X.h" //Click here to get the library: http://librarymanager/All#SparkFun_AS7265X
AS7265X sensor;

#include <Wire.h>
#define greenLed 28
#define yellowLed 32
#define redLed 30

void setup() {
  Serial.begin(9600);

  pinMode(greenLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(redLed, OUTPUT);

  digitalWrite(greenLed, LOW);
  digitalWrite(yellowLed, LOW);
  digitalWrite(redLed, LOW);
  

  if(sensor.begin() == false)
  {
    Serial.println("Triad failed freezing...");
    while(true) {
      delay(1000);
    };
  }

  //Once the sensor is started we can increase the I2C speed
  Wire.setClock(400000);

  sensor.disableIndicator();

//  Serial.println("A,B,C,D,E,F,G,H,I,J,K,L,R,S,T,U,V,W");
}

void loop() {
  
}


void serialEvent() {
  
  String cmd = Serial.readStringUntil('\n');

  if (cmd == "triad") {
    getTriadReading();
  }
  else {
    openLed(cmd);
  }
}


void getTriadReading() {
  
  sensor.takeMeasurementsWithBulb(); //This is a hard wait while all 18 channels are measured

  Serial.print(sensor.getCalibratedA());
  Serial.print(",");
  Serial.print(sensor.getCalibratedB());
  Serial.print(",");
  Serial.print(sensor.getCalibratedC());
  Serial.print(",");
  Serial.print(sensor.getCalibratedD());
  Serial.print(",");
  Serial.print(sensor.getCalibratedE());
  Serial.print(",");
  Serial.print(sensor.getCalibratedF());
  Serial.print(",");

  Serial.print(sensor.getCalibratedG());
  Serial.print(",");
  Serial.print(sensor.getCalibratedH());
  Serial.print(",");
  Serial.print(sensor.getCalibratedI());
  Serial.print(",");
  Serial.print(sensor.getCalibratedJ());
  Serial.print(",");
  Serial.print(sensor.getCalibratedK());
  Serial.print(",");
  Serial.print(sensor.getCalibratedL());
  Serial.print(",");


  Serial.print(sensor.getCalibratedR());
  Serial.print(",");
  Serial.print(sensor.getCalibratedS());
  Serial.print(",");
  Serial.print(sensor.getCalibratedT());
  Serial.print(",");
  Serial.print(sensor.getCalibratedU());
  Serial.print(",");
  Serial.print(sensor.getCalibratedV());
  Serial.print(",");
  Serial.print(sensor.getCalibratedW());

  Serial.println();
}


void openLed(String color) {
  if (color == "ledGreen") {
    ledUp(greenLed);
  }  
  else if (color == "ledRed") {
    ledUp(redLed);    
  }
  else if (color == "ledYellow") {
    ledUp(yellowLed);
  }
}

void ledUp(int pin) {
  digitalWrite(pin, HIGH);
  delay(5000);
  digitalWrite(pin, LOW);
}
