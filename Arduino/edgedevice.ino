
// Include LED STRIP libraries and define LED STRIP constants
#include "FastLED.h"
#define NUM_LEDS 120
#define MAX_BRIGHTNESS 100
#define MIN_BRIGHTNESS 0
#define LED_STRIP_PIN 6

// Define constant and global variables associated with the potentiomenter
#include "TimerOne.h"
#define POTENTIOMETER_PIN A1
#define POTENTIOMETER_ERROR 8
double input;
int prev_output, output;

// Define constants associated with Button and LED
#include "stdbool.h"
#define BUTTON_PIN 3
#define DEBOUNCE_TIME 1000
int prev_press_time;
#define LED_PIN 7
bool power_state = true;

// Mic

#define MIC_INPUT A0
#define MIC_VAL 0
#define BAUD_RATE 9600
#define MIC_INTERRUPT_PIN 4
#define MIC_ERROR 0 
int prev_mic_val;

String str;

CRGB leds[NUM_LEDS] = {0};
CRGB colour = CRGB::Purple;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);
  FastLED.addLeds<NEOPIXEL, LED_STRIP_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(25);
  FastLED.clear();
  FastLED.show();

  pinMode(POTENTIOMETER_PIN, INPUT_PULLUP);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), set_power, RISING);

  digitalWrite(LED_PIN, power_state);

  pinMode(MIC_INPUT, INPUT);
  pinMode(MIC_INTERRUPT_PIN, INPUT);
  //  attachInterrupt(digitalPinToInterrupt(MIC_INTERRUPT_PIN), mic_on, HIGH);

  Timer1.initialize();
  Timer1.attachInterrupt(check_brightness, 500000);

  prev_mic_val = analogRead(MIC_INPUT);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {

  if (Serial.available() > 0) {
    str = Serial.readStringUntil('\n');
  
    if (str == "power") {
      set_power();
    } else if (str == "purple") {
      colour = CRGB::Purple;
    } else if (str == "blue") {
      colour = CRGB::Blue;
    } else if (str == "red") {
      colour = CRGB::Red;
    } else if (str == "green") {
      colour = CRGB::Green;
    }
  }
  
  if (power_state) {
    int sensorValue = analogRead(MIC_INPUT);
//    if (!in_range(prev_mic_val, sensorValue - MIC_ERROR, sensorValue + MIC_ERROR)) {
    int sensorValue_digital = digitalRead(MIC_INTERRUPT_PIN);   
    int max_leds = map(sensorValue, 50, 250, 0, NUM_LEDS);
    for (int i = 0; i < max_leds; i++) {
      leds[i] = colour;
    }
    for (int i = max_leds; i < NUM_LEDS; i++) {
      leds[i] = 0;
    }
    FastLED.show();
  }
}

void set_power() {
  if (millis() - prev_press_time > DEBOUNCE_TIME) {
    prev_press_time = millis();
    power_state = !power_state;
    digitalWrite(LED_PIN, power_state);
    if (!power_state) {
      FastLED.clear();
      FastLED.show();
    }
  }
}

void check_brightness() {
  output = map(analogRead(POTENTIOMETER_PIN), 0, 1023, MIN_BRIGHTNESS, MAX_BRIGHTNESS);
  if (!(in_range(prev_output, output - POTENTIOMETER_ERROR, output + POTENTIOMETER_ERROR))) {
    FastLED.setBrightness(output);
  }
  prev_output = output;
}

bool in_range(int val, int lowerLimit, int upperLimit) {
  return (val > lowerLimit & val < upperLimit);
}
