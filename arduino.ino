// date: 11.11.2021 author: eth, bar.Ver.:2
// update: 08.06.2022, Erweiterung: ADS1115
// update: 25.10.2022, Cooling system added
// Target: Arduino Uno + 2 x MCP4725 Board
// Liest 6 Analogkanäle in 8 Bit ein und setzt 2x12 Bit DAC
// update: 24.06.2022, Erweiterung um die Befehle ALL?, H2?

/********************************************************************/ // cooling init
// LED_temp
#include <OneWire.h> 
#include <DallasTemperature.h> 
#define ONE_WIRE_BUS 2 
OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);
#define RT0 10000   // Ω
#define B 3434      // K
#define VCC 5    //Supply voltage
#define R 10000  //R=10KΩ
float RT, VR, ln, TX, T0, VRT;

float analog_to_celcius(float inp){
  T0 = 25 + 273.15;
  inp = (5.00 / 1023.00) * inp;      //Conversion to voltage
  VR = VCC - inp;
  RT = inp / (VR / R);               //Resistance of RT
  ln = log(RT / RT0);
  TX = (1 / ((ln / B) + (1 / T0))); //Temperature from thermistor
  TX = TX - 273.15;                 //Conversion to Celsius
  return (TX);
}

int set_state(float t, bool state, int low, int high){
 if (t < -200){ //if temp_LED not working
  state = HIGH; }
 else{ //if working
  if(t >= high){
    state=HIGH;  }
  else if(t<low && state==HIGH){
    state=LOW;  } }
  return state;
}

#include <math.h> 
#include <stdbool.h>
float state = HIGH;
float temp_led;
float temp_act;

int pinOut = 2; //set out digital pin to temp_act
int set_high=15; //set temp high
int set_low=8;   //set temp low
#define ntc_pin A6         // Pin, to which the voltage divider is connected
#define relay_out 3
#define samplingrate 5    // Number of samples
int samples = 0;   //array to store the samples
int Delay = 500; //delay in in ms

/********************************************************************/ // DAC_ADC

#include <Wire.h>
#include <stdio.h>
#include <Adafruit_MCP4725.h>
#include <Adafruit_ADS1X15.h>

// Defines
// Analog in: Voltage Supervision
#define AI0         A0 // 
#define AI1         A1 // 
#define AI2         A2 //
#define AI3         A3 // 
#define AI4         A4 //
#define AI5         A5 // 

//Variables
Adafruit_MCP4725 DAC_CH0;         //Erzeugen eines MCP4725 Objekts für Channel 1
Adafruit_MCP4725 DAC_CH1; 
Adafruit_ADS1115 ADC1;   // ADC object at I2C address 0x48 for addr pin = GND

float fVCC = 5.0;                  //Versorgungsspannung Vcc
float fLSB = fVCC/4095;            //least significant bit, Auflösung DAC
String sMsg = "";                  //Erzeuge Nachricht vom UART
// float const multiplier = 0.1875F; // ADS1115  @ +/- 6.144V gain = 0.1875mV/step 
float fVolt = 0;

void setup() {
  // DAC_ADC_init
  Serial.begin(115200);
  Serial.setTimeout(10);   
  DAC_CH0.begin(0x60);
  DAC_CH0.setVoltage(0,false);
  DAC_CH1.begin(0x61);//VOLT
  DAC_CH1.setVoltage(0,false);
  // ADC1.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV

  // cooling_init
  sensors.begin(); 
  pinMode(relay_out, OUTPUT);
  ADC1.begin(0x48);  // Initialize ads1115 at address 0x49

}

void loop() {

  //cooling back code
  sensors.requestTemperatures(); 
  temp_act = sensors.getTempCByIndex(0); 
  temp_led=analog_to_celcius(analogRead(ntc_pin));  
  state=set_state(temp_led,state,set_low,set_high); //set state
  digitalWrite(relay_out,state);//send state

  

  String sCmd = "";
  sMsg = Serial.readStringUntil('\n');                                  
  if (sMsg == "") {}                                                  
  else if (sMsg == "*IDN?")  // ------------------------------    Befehl: *IDN? Antwort = "<STRING>"
  {
    Serial.println("YSICD: Inbetriebnahme: HW:Arduino Uno, 2xMCP4725,1xADS1115 SW:0.3");       // Rückgabe der SW und Platinenkennung auf Serial Std
  }
  else if (sMsg == "TEMP0?")  // ------------------------------    Befehl: *IDN? Antwort = "<STRING>"
  {
     Serial.println(temp_act);  
   }
   else if (sMsg == "TEMP1?")
   {
     Serial.println(temp_led);
   }
  else if (sMsg == "VOLT?") //---------------------------- VoltageRead
    {
    int iAI0 = analogRead(AI0);
    int iAI1  = analogRead(AI1);
    int iAI2 = analogRead(AI2);
    int iAI3  = analogRead(AI3);
    int iAI4 = analogRead(AI4);
    int iAI5  = analogRead(AI5);
    Serial.print("AI0 = ");
    Serial.print(iAI0);
    Serial.print(" AI1 = ");
    Serial.print(iAI1);
    Serial.print(" AI2 = ");
    Serial.print(iAI2);
    Serial.print(" AI3 = ");
    Serial.print(iAI3);
    Serial.print(" AI4 = ");
    Serial.print(iAI4);
    Serial.print(" AI5 = ");
    Serial.println(iAI5);
  }
  else if (sMsg == "CURR?")
  {
    //int iADC23 = ADC1.readADC_SingleEnded(1);
    int iADC23 = ADC1.readADC_Differential_0_1();  
    Serial.print("CURR = ");
    Serial.println(iADC23); 
  }
  else if (sMsg == "H2?")
  {
    int iADC2 = ADC1.readADC_SingleEnded(2);
    //int iADC23 = ADC1.readADC_Differential_0_1();  
    Serial.print("H2 = ");
    //Serial.println(iADC2);
    Serial.print(21.00); 
  }
  else if (sMsg == "ALL?")
  {
    int iADC2 = ADC1.readADC_SingleEnded(2);
    int iADC23 = ADC1.readADC_Differential_0_1();  
    Serial.print("H2 = ");
    Serial.print(iADC2);
    Serial.print(" CURR = ");
    Serial.println(iADC23);  
  }
  else if (sMsg.substring(0, 10) == "DACVOLT:0=") //-------------------------------------------------------------------------------------------- Volt:Ch0= %f!
  {
    String sVoltCh0 = sMsg.substring(10,15); 
    float fVoltCh0 = sVoltCh0.toFloat();
    if ((fVoltCh0 < 0)||(fVoltCh0 > 5.0))
      {
      Serial.println("Limits exceeded!");
      }
    else if (fVoltCh0 == 0)
      { //Abfangen, ob die Null auch eine Zahl ist
      if ((isdigit(sVoltCh0[0]))||(isdigit(sVoltCh0[2]))||(isdigit(sVoltCh0[3]))||(isdigit(sVoltCh0[4])))
         {
          Serial.println(" OK");
          fVolt = fVoltCh0;
          DAC_CH0.setVoltage(0,false);
         } 
      else 
         {
         Serial.println("No Number");
         }
    }
    else
    {
     fVolt = fVoltCh0;
     DAC_CH0.setVoltage((int)floor(fVolt/fLSB), false);
     Serial.print((int)floor(fVolt/fLSB));
     Serial.println("OK");
    } 
  }
    else if (sMsg.substring(0, 10) == "DACVOLT:1=") //-------------------------------------------------------------------------------------------- Volt:Ch1= %f! %.3f 0.000!
  {
    String sVoltCh1 = sMsg.substring(10,15); 
    float fVoltCh1 = sVoltCh1.toFloat();
    if ((fVoltCh1 < 0)||(fVoltCh1 > 2.2))
      {
      Serial.println("Limits exceeded!");
      }
    else if (fVoltCh1 == 0)
      { //Abfangen, ob die Null auch eine Zahl ist
      if ((isdigit(sVoltCh1[0]))||(isdigit(sVoltCh1[2]))||(isdigit(sVoltCh1[3]))||(isdigit(sVoltCh1[4])))
         {
          Serial.println(" OK");
          fVolt = fVoltCh1;
          DAC_CH1.setVoltage(0,false);
         } 
      else 
         {
         Serial.println("No Number");
         }
    }
    else
    {
     fVolt = fVoltCh1;
     DAC_CH1.setVoltage((int)floor(fVolt/fLSB), false);
     Serial.print((int)floor(fVolt/fLSB));
     Serial.println("OK");
    } 
  }
  
}
