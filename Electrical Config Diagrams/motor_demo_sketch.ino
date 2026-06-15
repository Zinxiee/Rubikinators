// Raspberry Pi Pico + Stepper Motor Example

#define STEP_PIN 2 // 4, 6, 8, 12
#define DIR_PIN 3 // 5, 7, 9, 13

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);
}

void loop() {
  // Move 200 steps (one rotation) CW over one second
  digitalWrite(DIR_PIN, HIGH);
  for (int i = 0; i < 200; i++) {
    digitalWrite(STEP_PIN, HIGH);
    digitalWrite(STEP_PIN, LOW);
    delay(5); // 5 ms * 200 = 1 second
  }

  delay(500); // Wait half a second

  // Move 200 steps (one rotation) CCW over 400 millis
  digitalWrite(DIR_PIN, LOW); 
  for (int i = 0; i < 200; i++) {
    digitalWrite(STEP_PIN, HIGH);
    digitalWrite(STEP_PIN, LOW);
    delay(2); // 2 ms * 200 = 0.4 seconds
  }

  delay(1000); // Wait another second
}
