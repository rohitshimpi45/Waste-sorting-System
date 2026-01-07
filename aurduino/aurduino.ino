// Pin Definitions
const int motorPWM = 9;
const int motorDir = 8;
const int sensorPin = 2;
const int pistonPin = 5;    // existing piston
const int piston2Pin = 6;   // new piston for plastic detection

void setup() {
  pinMode(motorPWM, OUTPUT);
  pinMode(motorDir, OUTPUT);
  pinMode(sensorPin, INPUT);
  pinMode(pistonPin, OUTPUT);
  pinMode(piston2Pin, OUTPUT);

  digitalWrite(pistonPin, LOW);
  digitalWrite(piston2Pin, LOW);

  // Start motor moving forward
  digitalWrite(motorDir, LOW);
  analogWrite(motorPWM, 100);

  // Start Serial Communication
  Serial.begin(9600);
}

void loop() {
  int sensorState = digitalRead(sensorPin);

  // Existing piston (sensor-based)
  if (sensorState == LOW) {
    delay(1700);
    digitalWrite(pistonPin, HIGH);
    delay(500);
    digitalWrite(pistonPin, LOW);
  }

  // === Serial Input from PyCharm ===
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'P') {
      // Plastic detected -> actuate piston 2
      digitalWrite(piston2Pin, HIGH);
      delay(500);
      digitalWrite(piston2Pin, LOW);
      Serial.println("Piston 2 actuated (Plastic detected)");
    } 
    else if (command == 'R') {
      // Paper detected (optional action)
      Serial.println("Paper detected, no piston action");
    }
  }
}