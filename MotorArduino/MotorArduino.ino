// Motoriuno - As in the script that lives on the Arduino within the RC Car (tasked to recieve instruction and run the DC motors)
// pwm - Pulse Width Modulation - aka power, amount of current 
// dir - direction - direction of current (i.e forward/reverse)


int pwm_a = 3;  //PWM control for motor outputs 1 and 2 
int pwm_b = 9;  //PWM control for motor outputs 3 and 4
int dir_a = 2;  //direction control for motor outputs 1 and 2 
int dir_b = 8;  //direction control for motor outputs 3 and 4 
int myData = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(pwm_a, OUTPUT);  //Set control pins to be outputs
  pinMode(dir_a, OUTPUT);
  pinMode(pwm_b, OUTPUT);  //Set control pins to be outputs
  pinMode(dir_b, OUTPUT);
  analogWrite(pwm_a, 255);  //set both motors to run at (100/255 = 39)% duty cycle (slow)
  analogWrite(pwm_a, 0);
  analogWrite(pwm_b, 255);  //set both motors to run at (100/255 = 39)% duty cycle (slow)
  analogWrite(pwm_b, 0);
}
int lastData = 9;
void loop()
{ 
  //Serial.print("in Loop");
  if(Serial.available() > 0) {
      myData = Serial.read() - '0';
      
      //delay(200);
      Serial.println("read data");
      Serial.println(myData);


      // protect against data overload 
      if(myData != lastData){ 

      if(myData == 0 && myData != lastData){ 
         analogWrite(pwm_a, 0);
         analogWrite(pwm_b, 0);
      }
      
      if(myData == 1 && myData != lastData ){
         digitalWrite(dir_a, LOW); 
         analogWrite(pwm_a, 255);
         analogWrite(pwm_b, 0);
       
      }
      if(myData == 2 && myData != lastData ){
         digitalWrite(dir_a, HIGH); 
         analogWrite(pwm_a, 255);
         analogWrite(pwm_b, 0);
       
      }
      if(myData == 3 && myData != lastData ){
         digitalWrite(dir_b, LOW); 
         analogWrite(pwm_b, 250);
         analogWrite(pwm_a, 0);
       
      }
      if(myData == 4 && myData != lastData ){
         digitalWrite(dir_b, HIGH); 
         analogWrite(pwm_b, 250);
         analogWrite(pwm_a, 0);
       
      }

      if(myData == 5 && myData != lastData ){
         digitalWrite(dir_b, LOW); 
         analogWrite(pwm_b, 255);
         digitalWrite(dir_a, HIGH); 
         analogWrite(pwm_a, 255);
       
      }
      
      if(myData == 6 && myData != lastData ){
         digitalWrite(dir_b, HIGH); 
         analogWrite(pwm_b, 255);
         digitalWrite(dir_a, HIGH); 
         analogWrite(pwm_a, 255);
       
      }
      if(myData == 7 && myData != lastData ){
         digitalWrite(dir_b, LOW); 
         analogWrite(pwm_b, 255);
         digitalWrite(dir_a,LOW); 
         analogWrite(pwm_a, 255);
       
      }
      if(myData == 8 && myData != lastData ){
         digitalWrite(dir_b, HIGH); 
         analogWrite(pwm_b, 255);
         digitalWrite(dir_a, LOW); 
         analogWrite(pwm_a, 255);
       
      }
      }
      
      lastData = myData;
      delay(100);
    
      
      //Serial.flush();
      
    //} else {
    //  analogWrite(pwm_a, 0);
    //}
    //delay(200);
    //Serial.print("myData = " + myData);
}
}
