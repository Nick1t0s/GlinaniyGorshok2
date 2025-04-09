int dataPin = 0;// к выводу 14 регистра SD
int clockPin = 1;// к выводу 11 регистра (SH_CP)
int latchPin = 2;// к выводу 12 регистра (ST_CP)

void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  PORTB &= ~(1 << PB2);
}

void loop() {
  PORTB &= ~(1 << PB2);
  shiftOut(dataPin, clockPin, LSBFIRST, 0b10000000);
  PORTB |= (1 << PB2);
  delayMicroseconds(500);
}