int dataPin = 0;    // к выводу 14 регистра SD
int clockPin = 1;  // к выводу 11 регистра (SH_CP)
int latchPin = 2;  // к выводу 12 регистра (ST_CP)
int i = 0;
int sine_table[16][4] = {{1, 0, 0, 1}, {1, 0, 1, 1}, {1, 1, 0, 1}, {1, 1, 1, 1}, {1, 1, 1, 1}, {1, 1, 1, 0}, {1, 1, 0, 0}, {1, 0, 0, 1}, {0, 1, 1, 0}, {0, 0, 1, 1}, {0, 0, 0, 1}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 1}, {0, 0, 1, 1}, {0, 1, 1, 0}};
void setup() {
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  PORTB &= ~(1 << PB2);
}

void loop() {
  if (i < 16){
    PORTB &= ~(1 << PB2);
    for (int j=0;j<4; j++){
      if (sine_table[i][j] == 1){
        PORTB |= (1 << PB0);
      }
      else{
        PORTB &= ~(1 << PB0);
      }
      PORTB |= (1 << PB1);
      PORTB &= ~(1 << PB1);
    }
    PORTB |= (1 << PB2);
    i ++;
    delayMicroseconds(6);
  }
  else{
    i = 0;
    PORTB &= ~(1 << PB2);
    for (int j=0;j<4; j++){
      if (sine_table[i][j] == 1){
        PORTB |= (1 << PB0);
      }
      else{
        PORTB &= ~(1 << PB0);
      }
      PORTB |= (1 << PB1);
      PORTB &= ~(1 << PB1);
    }
    PORTB |= (1 << PB2);
    delayMicroseconds(6);
  }
}