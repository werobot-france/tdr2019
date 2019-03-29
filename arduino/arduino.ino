#include <Encoder.h>

#include "LegoRC.h"

// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder myEnc(5, 6); //pin de l'encoder sur l'arduino. les fils blans et bleus je pense
//   avoid using pins with LEDs attached

int pinIrLed = 0;
LegoRC lego(pinIrLed, 50);

void setup() {
  Serial.begin(9600);
  Serial.println("INIT");
}

void triggerElectron() {
  lego.sendCommand(1, 4, 9); // 1 --> ChanneL switch 2 ; 4 --> Single output mode - rouge ; 9 --> PWM backward step 7 (avance chariot)
}

long oldPosition  = -999;

String command = "";

void loop() {
  long newPosition = myEnc.read();
  if (newPosition != oldPosition) {
    oldPosition = newPosition;
    Serial.println(newPosition);
  }
  command = Serial.readStringUntil('\n');
  if (command != ""){
    triggerElectron();
  }
}