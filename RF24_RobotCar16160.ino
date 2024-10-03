/*
Robot Car mit Motor Shield V2, Code für Stillstand = 16160
je 15 Stufen vor/zurück, je 15 Stufen rechts/links
letzte Ziffer für Taster (Buttons) mit Wertigekten 1 (z.B. Blaulicht),
Wertigkeit 2 (z.B. für Sirene) und 4 (z.B. für Umschalten in autonomen Modus)
noch nicht implementiert
Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
github: Bernd54Albrecht
This is based on a test sketch for the Adafruit assembled Motor Shield for Arduino v2
It won't work with v1.x motor shields! Only for the v2's with built in PWM control
For use with the Adafruit Motor Shield v2
---->	http://www.adafruit.com/products/1438
*/

#include <Adafruit_MotorShield.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(9, 10); // CE, CSN
const byte address[7] = "B54ALB";

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

// Select which 'ports' M1, M2, M3 and/or M4.
Adafruit_DCMotor *rightMotor = AFMS.getMotor(1);
Adafruit_DCMotor *leftMotor = AFMS.getMotor(4);


// define variables for speed control
float vBatt = 9;     // for 6 AA batteries
int x = 0; 
int y = 0;
int left = 0;
int right = 0;  
int code = 16160;
int speedL = 0;
float factor = 6/vBatt;      // correction for battery voltage 6/vBatt

  
void setup() {
  Serial.begin(115200);       // set up Serial Monitor at 115200 bps
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  if (!AFMS.begin()) {         // create with the default frequency 1.6KHz
  // if (!AFMS.begin(1000)) {  // OR with a different frequency, say 1KHz
    Serial.println("Could not find Motor Shield. Check wiring.");
    while (1);
  }
  Serial.println("Motor Shield found.");

  // initialize radio nRF24L01
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening(); 
  }  // end of setup

void motor()  {
  y = int(code / 1000);
  x = int((code - 1000*y) / 10);
  y = y - 16;
  x = x - 16;
  Serial.print("code = ");
  Serial.print(code);
  Serial.print(" y = ");
  Serial.print(y);
  Serial.print(" x = ");
  Serial.print(x);

  if (y > 2){
    right = 16 * (y + x/2);
    if (right > 255)  right = 255;
    left = 16 * (y - x/2);
    if (left > 255)  left = 255;    
  }
  else if (y < -2){
    right = 16 * (y - x/2);
    if (right < -255)  right = -255;
    left = 16 * (y + x/2);
    if (left < -255)  left = -255;   
  }
  else {
    right = 16 * x;
    if (right > 0 && right < 64)   right = 0;
    if (right < 0 && right > -64)   right = 0;  
    left = -16 * x;
    if (left > 0 && left < 64)   left = 0; 
    if (left < 0 && left > -64)   left = 0; 
  }
  //input of rate of speed for  "left" and "right"
  Serial.print("  left = ");
  Serial.print(left);
  Serial.print("  right = ");
  Serial.println(right);

    // Set the speed to start, from 0 (off) to 255 (max speed)
  rightMotor->setSpeed(abs(right)*factor);
  leftMotor->setSpeed(abs(left)*factor);
  if (right > 0)   {
    rightMotor->run(FORWARD);   }
  if (right < 0)  {
    rightMotor->run(BACKWARD);   }
  if (left > 0)   {
    leftMotor->run(FORWARD);  }
  if (left < 0)   {
    leftMotor->run(BACKWARD);   }
  if (right = 0)   {
    leftMotor->run(RELEASE);  }
  if (left = 0)   {
    leftMotor->run(RELEASE);   }
}   // end of motor()

void loop() {
  if (radio.available()) {
    code = 0;
    radio.read(&code, sizeof(code));
    Serial.println(code);
    motor(); 
  }
  delay(20);   //little delay for better serial communication
}  // end of loop

