#include "Arduino.h"
#include "LegoRC.h"

// Constructeur
LegoRC::LegoRC(int irPin, long interval = 100) {
	_irPin = irPin;
	_autoSendInterval = interval;
	pinMode(_irPin, OUTPUT);
	_lastMsg = "";
}

void LegoRC::autoSend() {
	if (_lastMsg != "") {
		if ((millis() - _timeLastSend) > _autoSendInterval) {
			sendSignalString(_lastMsg);
		}
	}
}


void LegoRC::sendCommand(int n1, int n2, int n3) {
  int nibble1 = n1;
  int nibble2 = n2;
  int nibble3 = n3;
  int lrc =  15 ^ nibble1 ^ nibble2 ^ nibble3;
  String msg = "";
  msg += intToBinConvert(nibble1);
  msg += intToBinConvert(nibble2);
  msg += intToBinConvert(nibble3);
  msg += intToBinConvert(lrc);
  sendSignalString(msg);
}

// exemple de msg: msg = "1000000100010111"; //ch1 red forward
void LegoRC::sendSignalString(String msg) {
  
  sendStartBit();
  for (int i=0; i < msg.length(); i ++) {
     if (msg[i] == '1') {
        sendBitHigh(); 
     } else {
        sendBitLow();
     }
  }
  sendStartBit();
  
  _lastMsg = msg;
  _timeLastSend = millis();
  
}



void LegoRC::sendBitHigh() {
  sendSixTop();
  delayMicroseconds(685); 
}

void LegoRC::sendBitLow() {
  sendSixTop();
  delayMicroseconds(395);
}


void LegoRC::sendStartBit() {
  sendSixTop();
  delayMicroseconds(1158);
}


void LegoRC::sendSixTop() {
  for (int i = 0; i < 6; i++) {
    digitalWrite(_irPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(_irPin, LOW);
    delayMicroseconds(10);
  }  
}

// gestion chaine de carractere
String LegoRC::intToBinConvert(int pat) {
 switch (pat) {
  case 0:
   return "0000";
  break; 
  case 1:
   return "0001";
  break; 
  case 2:
   return "0010";
  break; 
  case 3:
   return "0011";
  break; 
  case 4:
   return "0100";
  break;   
  case 5:
   return "0101";
  break; 
  case 6:
   return "0110";
  break;   
  case 7:
   return "0111";
  break; 
 case 8:
   return "1000";
  break; 
  case 9:
   return "1001";
  break;   
  case 10:
   return "1010";
  break; 
    case 11:
   return "1011";
  break; 
  case 12:
   return "1100";
  break; 
  case 13:
   return "1101";
  break; 
  case 14:
   return "1110";
  break; 
  case 15:
   return "1111";
  break; 
  
 }
 
}
 
