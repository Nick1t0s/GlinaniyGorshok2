int dataPin = 5;    // к выводу 14 регистра SD
int clockPin = 6;  // к выводу 11 регистра (SH_CP)
int latchPin = 7;  // к выводу 12 регистра (ST_CP)
int i = 0;
byte sine_table[32] = {0b11100000, 0b10000000, 0b10010000, 0b10010000, 0b10100000, 0b10100000, 0b10110000, 0b10110000, 0b10110000, 0b10110000, 0b10110000, 0b10100000, 0b10100000, 0b10010000, 0b10010000,
0b10000000, 0b10000000, 0b11100000, 0b11000000, 0b11000000, 0b10100000, 0b10100000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10000000, 0b10100000, 0b10100000, 0b11000000, 0b11000000, 0b11100000};

void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  digitalWrite(latchPin, LOW);
}

void loop() {
  if (i < 32){
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, sine_table[i]);
    digitalWrite(latchPin, HIGH);
    delayMicroseconds(8);
    i += 1;
  }
  else{
    i = 0;
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, sine_table[i]);
    digitalWrite(latchPin, HIGH);
    delayMicroseconds(8);
  }
}
