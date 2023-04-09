//Starter code by
// Stepper Motor
// Michael Klements
// The DIY Life
// 25/01/2017
//https://www.the-diy-life.com/arduino-stepper-motor-pololu-driver/
//Modified by Jeff for 18500
    
int motorPin = 3;        //Assign pin numbers 
int dirPin = 2;
int motorEnPin = 4;
int analogPin = A3;
int threshold = 30;
int val = 0;  // variable to store the light detection value read
int motorSpe = 50;      //Assign the motor speed, a smaller number is a faster speed (shorter delay between pulses) (setting to 0 is bad, 5 is best)
int rotation = 203;     //Assign the motor rotation in pulses (203 is a full circle)

void setup()
{
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);  //Assign Pins
  pinMode(dirPin, OUTPUT);
  pinMode(motorEnPin, OUTPUT);
}

void loop()
{
  //Turn motor driver off to prevent overheating
  digitalWrite(motorEnPin, HIGH);
  digitalWrite(dirPin, LOW);
  digitalWrite(motorPin, LOW);

  //Wait for command
  Serial.println("Motor Available: ");
  while (Serial.available() == 0) {}     //wait for data available

  //Parse Command
  String teststr = Serial.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String

  int commaIndex = teststr.indexOf(",");
  int strLength = teststr.length();
  String dirStr = teststr.substring(0, commaIndex);
  String rotateStr = teststr.substring(commaIndex + 1, strLength);
  rotation = rotateStr.toInt();
  if (teststr == "light") {
    val = analogRead(analogPin);          // read the input pin
    //Serial.println((val < threshold));    // return light detection info
    Serial.println((val));    // return light detection info
  } else if ((dirStr == "forward") || (dirStr == "backward")) {
    if(dirStr == "forward"){
      digitalWrite(dirPin, HIGH);
    } else {
      digitalWrite(dirPin, LOW);
    }
    Serial.println("Enter Loop");
    digitalWrite(motorEnPin, LOW);
    for(int j = 0 ; j < rotation ; j++)  //Run the motor to the input rotation at the input speed.
    {
      if(Serial.available()){
        //interrupt handling
        teststr = Serial.readString();
        teststr.trim();
        if(teststr == "stop") {
          Serial.println(rotation-j);
          break;
        } else {
          Serial.println("Invalid interrupt");
          //turn motor
          digitalWrite(motorPin, HIGH);
          delay(motorSpe);
          digitalWrite(motorPin, LOW);
        }
      } else {
        //turn motor
        digitalWrite(motorPin, HIGH);
        delay(motorSpe);
        digitalWrite(motorPin, LOW);
      }
    }
  } else {
    Serial.println("Invalid command");
  }

}
