// xboxArduino - as in the script living on the Arduino that will recieve and interpret xbox
// contoller inputs

#include <XBOXRECV.h> // From USB Host shield library 2.0

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#include <SPI.h>
#endif

USB Usb;
XBOXRECV Xbox(&Usb);

void setup() {
  Serial.begin(9600);
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  if (Usb.Init() == -1) {
    
    while (1); //halt
  }
  Serial.print(F("\r\nXbox Wireless Receiver Library Started"));
}
int allOff = 0;
int right = 3;
int left = 4;
int back = 2;
int backRight = 5;
int backLeft = 6;
int forward = 1;
int forwardRight = 7;
int forwardLeft = 8;
int buttonStateR2 = 0;
int buttonStateL2 = 0;
int buttonStateRStick = 0;
int carCmd = 0;
int lastCarCmd = 9;

 
void loop() {
  Usb.Task();
  
  if (Xbox.XboxReceiverConnected) {

    buttonStateR2 = Xbox.getButtonPress(R2);
    buttonStateL2 = Xbox.getButtonPress(L2);
    buttonStateRStick = Xbox.getAnalogHat(LeftHatX);
       
        if (!(buttonStateR2 == 255 && buttonStateL2 == 255)) {
          
        
        if (buttonStateR2 == 255) {
           if (buttonStateRStick > 30000) {
              carCmd = forwardRight;
           } else if (buttonStateRStick < -30000) {
              carCmd = forwardLeft;
           } else {
              carCmd = forward;
           }
        } 
        else if (buttonStateL2 == 255) {
           if (buttonStateRStick > 30000) {
              carCmd = backRight;
           } else if (buttonStateRStick < -30000) {
              carCmd = backLeft;
           } else {
              carCmd = back;
           }
        }
        else {
           if (buttonStateRStick > 30000) {
              carCmd = right;
           } else if (buttonStateRStick < -30000) {
              carCmd = left;
           } else {
              carCmd = allOff;
           }
        }

       if (carCmd != lastCarCmd) {
          Serial.println(carCmd);
       }
       lastCarCmd = carCmd;
       }
  }
}
