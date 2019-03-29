/*
  LegoRC.h - Library for command Lego RC PowerFunctions
  Created by Artiom FEDOROV Mai 2012
  Released into the public domain.
*/

#ifndef LegoRC_h
#define LegoRC_h

#include "Arduino.h"

class LegoRC
{
  public:
    LegoRC(int irPin, long interval);
	
	void sendCommand(int n1, int n2, int n3);
	void sendSignalString(String msg);
	void autoSend();
	
  private:
    int _irPin;
	String _lastMsg;
	long _timeLastSend;
	long _autoSendInterval;
	
	String intToBinConvert(int pat);
	void sendBitHigh();
	void sendBitLow();
	void sendStartBit();
	void sendSixTop();
	
};

#endif
