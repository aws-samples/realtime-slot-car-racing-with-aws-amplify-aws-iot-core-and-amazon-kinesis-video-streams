/*
Scalextric Car Gforce Sensor Sketch

This sketch requires an Arduino Nano RP2040.

Samuel Waymouth, 2022-10-28

*/

#include <ArduinoBearSSL.h>
#include <ArduinoECCX08.h>
#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DSOX.h>
#include <ArduinoJson.h>
#include "RTClib.h"

float Ax, Ay, Az;
float Gx, Gy, Gz;

#include "arduino_secrets.h"

#define IMU_MESSAGE_RATE_MS 50 // delay between IMU readings

/////// Enter your sensitive data in arduino_secrets.h
const char ssid[]        = SECRET_SSID;
const char pass[]        = SECRET_PASS;
const char broker[]      = SECRET_BROKER;
const char* certificate  = SECRET_CERTIFICATE;

WiFiClient    wifiClient;            // Used for the TCP socket connection
BearSSLClient sslClient(wifiClient); // Used for SSL/TLS connection, integrates with ECC508
MqttClient    mqttClient(sslClient);
//RTC_Micros mrtc;
RTC_Millis millirtc;
DateTime dtn;

unsigned long lastMicros = 0;  // microseconds
unsigned long startMicros = 0;  // microseconds
unsigned long currentMicros = 0;  // microseconds

unsigned long lastMillis = 0;  // microseconds
unsigned long startMillis = 0;  // microseconds
unsigned long currentMillis = 0;  // microseconds

bool timeStarted = false; //set the initial clock state

void setup() {
  
  Serial.begin(9600);

  if (!ECCX08.begin()) {
    Serial.println("No ECCX08 present!");
    while (1);
  }

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  //startMicros = micros();
  startMillis = millis();

  ArduinoBearSSL.onGetTime(getTime);

  sslClient.setEccSlot(0, certificate);

  mqttClient.setId("carid6");

  mqttClient.onMessage(onMessageReceived);

  // set the LED pins for the RGP Led
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  digitalWrite(LEDR, LOW);
  digitalWrite(LEDG, LOW);
  digitalWrite(LEDB, LOW);

}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LEDR, HIGH);
    connectWiFi();
  }

  if (!mqttClient.connected()) {
    // MQTT client is disconnected, connect
    digitalWrite(LEDR, HIGH);
    connectMQTT();
  }

  if (!timeStarted){ // start the clock
    startClock();
  }

  digitalWrite(LEDR, LOW);

  //currentMicros = micros();
  currentMillis = millis();

  //lastMicros = (currentMicros - startMicros) % 1000000;
  lastMillis = (currentMillis - startMillis) % 1000;

  publishMessage();

  delay(IMU_MESSAGE_RATE_MS);

}

unsigned long getTime() {
  // get the current time from the WiFi module
  return WiFi.getTime();
}

void connectWiFi() {
  Serial.print("Attempting to connect to SSID: ");
  Serial.print(ssid);
  Serial.print(" ");

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println();

  Serial.println("You're connected to the network");
  Serial.println();
}

void connectMQTT() {
  Serial.print("Attempting to MQTT broker: ");
  Serial.print(broker);
  Serial.println(" ");

  while (!mqttClient.connect(broker, 8883)) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println();

  Serial.println("You're connected to the MQTT broker");
  Serial.println();

  // subscribe to a topic
  mqttClient.subscribe("carid6/incoming");

}

void startClock(){
    DateTime thisTime = getTime();
    //mrtc.begin(thisTime);
    millirtc.begin(thisTime);
    //DateTime thatTime = mrtc.now();
    DateTime thatTime = millirtc.now();
    Serial.println(String(thatTime.timestamp(DateTime::TIMESTAMP_FULL)));
    timeStarted = true;
}

void publishMessage() {

  digitalWrite(LEDB, HIGH);

  //Serial.println("Publishing message");
  IMU.readAcceleration(Ax, Ay, Az);
  IMU.readGyroscope(Gx, Gy, Gz);

  // send message, the Print interface can be used to set the message contents
  StaticJsonDocument<256> doc; // create a new json document
  //DateTime dtn = mrtc.now();
  DateTime dtn = millirtc.now();
  doc["time"] = String(dtn.timestamp(DateTime::TIMESTAMP_FULL) + "." + lastMillis);
  doc["Ax"] = Ax;
  doc["Ay"] = Ay;
  doc["Az"] = Az;
  doc["Gx"] = Gx;
  doc["Gy"] = Gx;
  doc["Gz"] = Gz;

  Serial.print("INFO: Sending IMU data to IoT core: ");
  serializeJson(doc, Serial);
  Serial.println();

  mqttClient.beginMessage("carid6/gforce");
  serializeJson(doc, mqttClient);
  mqttClient.endMessage();

  digitalWrite(LEDB, LOW);

}

void onMessageReceived(int messageSize) {
  // we received a message, print out the topic and contents
  Serial.print("Received a message with topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");

  // use the Stream interface to print the contents
  while (mqttClient.available()) {
    Serial.print((char)mqttClient.read());
  }
  Serial.println();

  Serial.println();
}
