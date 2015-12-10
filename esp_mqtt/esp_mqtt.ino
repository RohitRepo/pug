#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <EEPROM.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DNSServer.h>
#include "WiFiManager.h"

// Update these with values suitable for your network.

const char* MQTT_SERVER = "m11.cloudmqtt.com";
const int MQTT_PORT = 12911;
const char* MQTT_USER = "device";
const char* MQTT_PASSWORD = "thelazypug";
const int device_id = 123;

WiFiClient espClient;
PubSubClient client(espClient);

const int ACTION_PIN = 2;
String device_status;
String STATUS_OFF = "off";
String STATUS_ON = "on";
char target_topic[30];

String getEEPROMString(int start, int len) {
  EEPROM.begin(512);
  delay(10);
  String string = "";
  for (int i = start; i < start + len; i++) {
    //Serial.println(i);
    string += char(EEPROM.read(i));
  }
  EEPROM.end();
  return string;
}

void setEEPROMString(int start, int len, String string) {
  EEPROM.begin(512);
  delay(10);
  int si = 0;
  for (int i = start; i < start + len; i++) {
    char c;
    if (si < string.length()) {
      c = string[si];
      //Serial.println("Wrote: ");
      //Serial.println(c);
    } else {
      c = 0;
    }
    EEPROM.write(i, c);
    si++;
  }
  EEPROM.end();
  Serial.println("Wrote " + string);
}

String getStatus() {
  Serial.println("Reading EEPROM Status");
  device_status = getEEPROMString(64, 67);
  Serial.println("Status: " + device_status);
  
  if (device_status == "") {
    device_status = STATUS_OFF;
  };
  
  return device_status;
}


void setStatus(String s) {
  device_status = s;
  setEEPROMString(64, 67, device_status);
}

void setup_wifi() {
    WiFiManager wifi;
    wifi.autoConnect("ALAZYPUG");
}

void publish_update() {
  sprintf(target_topic, "devices/updates/%d", device_id);
  Serial.println("Publish update: ");
  Serial.println(device_status);
  Serial.println(target_topic);
  client.publish(target_topic, device_status.c_str());
}

void update_device_status(const char* buffer) {
  if (strstr(buffer, STATUS_OFF.c_str())) {
    digitalWrite(ACTION_PIN, LOW);
    setStatus(STATUS_OFF);
  } else if (strstr(buffer, STATUS_ON.c_str())) {
    digitalWrite(ACTION_PIN, HIGH);
    setStatus(STATUS_ON);
  } else {
    Serial.print("Got invalid action:");
  }
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  char buffer[length];
  strncpy(buffer, (char *)payload, length);

  Serial.println("Got payload buffer");
  Serial.println(buffer);

  update_device_status(buffer);
  publish_update();

}

void setup() {
  pinMode(ACTION_PIN, OUTPUT);
  Serial.begin(115200);
  getStatus();
  update_device_status(device_status.c_str());
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(mqtt_callback);
}

void publish_connect() {
  Serial.println("connected");
  
  sprintf(target_topic, "devices/connects/%d", device_id);
  Serial.println("Publish connect to");
  Serial.println(target_topic);

  String localIp = String(WiFi.localIP()[0]) + "." + 
  String(WiFi.localIP()[1]) + "." + 
  String(WiFi.localIP()[2]) + "." + 
  String(WiFi.localIP()[3]);
  client.publish(target_topic, localIp.c_str());
}

void subscribe_topics() {
  sprintf(target_topic, "devices/actions/%d", device_id);
      
  Serial.println("Subscribe to");
  Serial.println(target_topic);
  client.subscribe(target_topic);
}

void mqtt_reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    sprintf(target_topic, "devices/last/%d", device_id);
    if (client.connect("ESP8266Client", MQTT_USER, MQTT_PASSWORD, target_topic, 1, 0, "")) {
      publish_connect();
      publish_update();
      subscribe_topics();
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  if (!client.connected()) {
    mqtt_reconnect();
  }
  client.loop();
}
