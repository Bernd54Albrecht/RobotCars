/*
Joystick-Shield V1A als Robot Car Controller, Stillstand = 16160
je 15 Stufen vor/zurück, je 15 Stufen rechts/links
3 Taster (Buttons) mit Wertigkeit 1 (beide blauen B und D),
Wertigkeit 2 für gelbe Taster (A und C) und 4 für Joystick-Button
Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
github: Bernd54Albrecht
*/
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
RF24 radio(9, 10); // CE, CSN
const byte address[7] = "B54ALBR";

int x = 16;   // x-Achse = links/rechts
int y = 16;   // y-Achse = vor/zurück
int code = 16160;
const int yellow1button = 2;
const int yellow2button = 4;
const int blue1button = 3;
const int blue2button = 5;
const int joybutton = 8;  // Joystick button
float faktor = 1.0;   // für Anpassung bei unterschiedlicher Spannung oder ADC

void setup() {
  pinMode(joybutton,INPUT_PULLUP);
  pinMode(yellow1button,INPUT_PULLUP);
  pinMode(yellow2button,INPUT_PULLUP);
  pinMode(blue1button,INPUT_PULLUP);
  pinMode(blue2button,INPUT_PULLUP);
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void sendcode()  {
  radio.write(&code, sizeof(code));
  delay(100);  // little delay for next button press
  }

void loop() {
  float A0 = faktor * analogRead (0); 
  float A1 = faktor * analogRead (1); 
  int button3 = 4 * !digitalRead(joybutton);
  int button1 = 1 * (!digitalRead(blue1button) || !digitalRead(blue2button));
  int button2 = 2 * (!digitalRead(yellow1button) || !digitalRead(yellow2button));
  int button = button1 + button2 + button3;

  Serial.print("x-Achse: ");
  Serial.print(A0);
  Serial.print("y-Achse: ");
  Serial.print(A1);
  Serial.print("  Buttons pressed ");
  Serial.println(button);

  x = map((A0+10),0,1023,1,31);      // little corrections
  Serial.print("  x = ");
  Serial.println(x);  
  y = map((A1-7),0,1023,1,(31+1));   // little corrections
  Serial.print("  y = ");
  Serial.println(y);  
  code = 1000*y + 10*x + button;
  Serial.print("  Code = ");
  Serial.println(code);
  sendcode();
}
