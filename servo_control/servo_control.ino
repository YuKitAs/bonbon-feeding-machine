#include <Servo.h>

const int UART_BPS = 9600;

const int SERVO_PORT_NUM = 9;
const int SERVO_NEUTRAL_POINT = 92;
const int SERVO_MOVING_POINT = 88;
const int SERVO_STEP_TIME_MS = 300;

Servo servo;

void setup() {
  initializeServo();
  initializeUartConnect();
}

void loop() {
  if (Serial.available() > 0) {
    char readChar = Serial.read();
    if (readChar == 'f') {
      Serial.println("START");
      servo.write(SERVO_MOVING_POINT);
      delay(SERVO_STEP_TIME_MS);
      servo.write(SERVO_NEUTRAL_POINT);
      Serial.println("STOP");
    } else {
      Serial.println("UNKNOWN");
    }
  }
}

void initializeServo() {
  servo.attach(SERVO_PORT_NUM);
}

void initializeUartConnect() {
  Serial.begin(UART_BPS);
  // Actively wait for connecting:
  while (!Serial) {}
}

