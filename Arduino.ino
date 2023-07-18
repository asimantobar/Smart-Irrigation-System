const int SERIAL_SPEED_9600 = 9600.0;
const int SECOND  = 1000.0;
const int humidPin = A1;
const int tempPin = A2;
const int pinLedTemp = 2;
const int pinLedSun = 3;
const int waterPin = A3;
int humid_percent;
int sun_status;
int contH=0;
int contL=0;
String command;

void setup() {
  // put your setup code here, to run once:
  
Serial.begin(SERIAL_SPEED_9600);
pinMode(pinLedTemp, OUTPUT);
digitalWrite(pinLedTemp, LOW);
pinMode(pinLedSun, OUTPUT);
digitalWrite(pinLedSun, LOW);
pinMode(waterPin, OUTPUT);
digitalWrite(waterPin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  
int tempVal = analogRead(tempPin);
float voltage = (tempVal / 1024.0) * 5.0;
float temperature = (voltage - 0.5) * 100;

int humedad = analogRead(humidPin);
humid_percent = map(humedad, 100,1023, 100,0);

Serial.print("<temp=");
Serial.print(temperature);
Serial.print(",humid=");
Serial.print(humid_percent);
Serial.println(">");

if (Serial.available()) {
  command = Serial.readStringUntil('\n'); //read until ‘\n’
  command.trim(); // Remove extraneous whitespace characters if any
  if (command.equals("dry")) {
    digitalWrite(waterPin, HIGH);
  }
  else if (command.equals("humid")) {
    digitalWrite(waterPin, LOW);
  }
  else if (command.equals("cold")) {
    digitalWrite(pinLedTemp, HIGH);
  }
  else if (command.equals("warm")) {
    digitalWrite(pinLedTemp, LOW);
  }
   if (command.equals("indoor")) {
    digitalWrite(pinLedSun, HIGH);
    sun_status="HIGH";
  }
  else if (command.equals("outdoor")) {
    digitalWrite(pinLedSun, LOW);
    sun_status="None";
  }
}
if (sun_status == "HIGH"){
  contH=contH+1;
  if (contH==10){ //10 is equal to 5 seconds in order to visualise the change, in theory would be 12 hours
    digitalWrite(pinLedSun, LOW);
    sun_status="LOW";
    contH=0;
  }
}
if (sun_status == "LOW"){
  contL=contL+1;
  if (contL==10){ //10 is equal to 5 seconds in order to visualise the change, in theory would be 12 hours
    digitalWrite(pinLedSun, HIGH);
    sun_status="HIGH"; 
    contL=0;
  }
}
delay(0.5*SECOND);
}
