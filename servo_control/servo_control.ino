#include <Servo.h>

//////////// SERVO /////////////////////////

Servo servo;

void servo_RotateTo(int angle) {
  angle = angle > 180 ? 180 : angle;
  angle = angle < 0 ? 0 : angle;
  
  while (servo.read() < angle || servo.read() > angle) {
    if (servo.read() < angle) {
      servo.write(servo.read() + 1);
      delay(50);
    } else {
      servo.write(servo.read() - 1);
      delay(50);
    }
  }
}

void servo_Feed() {
  servo_RotateTo(servo.read() + 60);
}

void servo_Forward() {
  servo_RotateTo(servo.read() + 5);
}

void servo_Backward() {
  servo_RotateTo(servo.read() - 5);
}

void servo_Initialize() {
  servo.attach(9, 500, 2000);
  servo.write(0);
}

//////////// SERIAL ////////////////////////

void serial_Initialize() {
  Serial.begin(9600);
  while (!Serial) {}
  Serial.println("READY");
}

////////////////////////////////////////////

void setup() {
  serial_Initialize();
  servo_Initialize();
}

void loop() {
  if (Serial.available() > 0) {
    switch (Serial.read()) {
      case 'f':
        Serial.println("FEED");
        servo_Feed();
        break;
      case 'h':
        Serial.println("ALIVE");
        break;
      case 'a':
        Serial.println("FORWARD");
        servo_Forward();
        break;
      case 'b':
        Serial.println("BACKWARD");
        servo_Backward();
        break;
      case 'r':
        Serial.println("RESET");
        servo_Initialize();
        break;
    }
  }
}

