#include <Servo.h>

// --------------- ANGLES ---------------

// Define angles associated with each state.


// Default State
#define BASE_ROTATION_DEFAULT 70
#define JOINT1_DEFAULT 60
#define JOINT2_DEFAULT 20
#define JOINT3_DEFAULT 100
#define ARM_ROTATION_DEFAULT 60
#define HAND_OPEN 0


// Picking State
#define JOINT1_PICKING 78
#define JOINT2_PICKING 5
#define HAND_CLOSED 30


// Dropping State
#define JOINT1_DROPPING 70
#define JOINT2_DROPPING 5


// After-Picking State
#define JOINT1_AFTERPICKING 45
#define JOINT2_AFTERPICKING 20


// Rotated-Right State
#define BASE_ROTATION_RIGHT 130


// Rotated-Left State
#define BASE_ROTATION_LEFT 10

// --------------------------------------


// Pins for each servo
#define BASE_ROTATION_PIN 3
#define JOINT1_PIN 5
#define JOINT2_PIN 6
#define JOINT3_PIN 9
#define ARM_ROTATION_PIN 10
#define HAND_PIN 11


Servo base_rotation;
Servo joint1;
Servo joint2;
Servo joint3;
Servo arm_rotation;
Servo hand;


// --------------- STATES ---------------


// Go down and close hand.
void pickingState() {
  joint1.write(JOINT1_PICKING);
  joint2.write(JOINT2_PICKING);
  delay(1000);
  hand.write(HAND_CLOSED);
}


// Go down and open hand.
void droppingState() {
  joint1.write(JOINT1_DROPPING);
  joint2.write(JOINT2_DROPPING);
  delay(1000);
  hand.write(HAND_OPEN);
}


// Go up after holding fruit.
void afterPickingState() {
  joint1.write(JOINT1_AFTERPICKING);
  joint2.write(JOINT2_AFTERPICKING);
}


// Rotate base to the right.
void rotatedRightState() {
  base_rotation.write(BASE_ROTATION_RIGHT);
}


// Rotate base to the left.
void rotatedLeftState() {
  base_rotation.write(BASE_ROTATION_LEFT);
}


// Default waiting state.
void defaultState() {
  base_rotation.write(BASE_ROTATION_DEFAULT);
  joint1.write(JOINT1_DEFAULT);
  joint2.write(JOINT2_DEFAULT);
  joint3.write(JOINT3_DEFAULT);
  arm_rotation.write(ARM_ROTATION_DEFAULT);
  hand.write(HAND_OPEN);
}

// --------------------------------------


// Pick up, rotate to the left, drop the fruit, then go up.
void pickToLeftBowl() {
  pickingState();
  delay(1000);
  afterPickingState();
  delay(1000);
  rotatedLeftState();
  delay(500);
  droppingState();
  delay(500);
  afterPickingState();
  delay(500);
}

// Pick up, rotate to the right, drop the fruit, then go up.
void pickToRightBowl() {
  pickingState();
  delay(1000);
  afterPickingState();
  delay(1000);
  rotatedRightState();
  delay(500);
  droppingState();
  delay(500);
  afterPickingState();
  delay(500);
}

// Set all servos to default state then attach them to the pins.
void initServos() {

  defaultState();

  delay(2000);
  base_rotation.attach(BASE_ROTATION_PIN);
  delay(500);
  joint1.attach(JOINT1_PIN);
  delay(500);
  joint2.attach(JOINT2_PIN);
  delay(500);
  joint3.attach(JOINT3_PIN);
  delay(500);
  arm_rotation.attach(ARM_ROTATION_PIN);
  delay(500);
  hand.attach(HAND_PIN);
}

void setup() {
  Serial.begin(9600);

  initServos();

  delay(3000);

}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == 'S') {
      Serial.println("Arduino Ack");
    }
    
    if (data == '1') {
      delay(500);
      pickToRightBowl();
      defaultState();
    }
    else if (data == '0') {
      delay(500);
      pickToLeftBowl();
      defaultState();

    }
  }
  delay(20);
}
