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
const int device_id = 1;

WiFiClient espClient;
PubSubClient client(espClient);

const int ACTION_PIN = 2;
char device_status[5];
char target_topic[30];

void setup_wifi() {
    WiFiManager wifi;
    wifi.autoConnect("ALAZYPUG");
}

void publish_update() {
  sprintf(target_topic, "devices/updates/%d", device_id);
  Serial.println("Publish update: ");
  Serial.println(device_status);
  Serial.println(target_topic);
  client.publish(target_topic, device_status);
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

  if (strstr(buffer, "off")) {
    digitalWrite(ACTION_PIN, LOW);
    strncpy(device_status, "off", sizeof("off"));
    publish_update();
  } else if (strstr(buffer, "on")) {
    digitalWrite(ACTION_PIN, HIGH);
    strncpy(device_status, "on", sizeof("on"));
    publish_update();
  } else {
    Serial.print("Got invalid action:");
  }

}

void setup() {
  pinMode(ACTION_PIN, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  strncpy(device_status, "off", sizeof("off"));
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
    if (client.connect("ESP8266Client", MQTT_USER, MQTT_PASSWORD)) {
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
