/*
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <EEPROM.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DNSServer.h>
#include "WiFiManager.h"

// Update these with values suitable for your network.

const char* ssid = "BEAM492148";
const char* password = "59549229";
const char* mqtt_server = "m11.cloudmqtt.com";
int device_id = 1;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
char target_topic[30];
int value = 0;

void setup_wifi() {

//  delay(10);
//  // We start by connecting to a WiFi network
//  Serial.println();
//  Serial.print("Connecting to ");
//  Serial.println(ssid);
//
//  WiFi.begin(ssid, password);
//
//  while (WiFi.status() != WL_CONNECTED) {
//    delay(500);
//    Serial.print(WiFi.status());
//    Serial.print(".");
//  }
//
//  Serial.println("");
//  Serial.println("WiFi connected");
//  Serial.println("IP address: ");
//  Serial.println(WiFi.localIP());
    WiFiManager wifi;
    wifi.autoConnect("ALAZYPUG");
}

void callback(char* topic, byte* payload, unsigned int length) {
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

  sprintf(target_topic, "devices/updates/%d", device_id);

  // Switch on the LED if an 1 was received as first character
  if (strstr(buffer, "off")) {
    digitalWrite(2, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)

    Serial.println("Publish update:off to");
    Serial.println(target_topic);
    client.publish(target_topic, "off");
    
  } else if (strstr(buffer, "on")) {
    digitalWrite(2, HIGH);  // Turn the LED off by making the voltage HIGH
    client.publish(target_topic, "on");
    Serial.println("Publish update:on to");
    Serial.println(target_topic);
  } else {
    Serial.print("Got invalid action:");
  }

}

void setup() {
  pinMode(2, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 12911);
  client.setCallback(callback);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client", "device", "thelazypug")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      sprintf(target_topic, "devices/connects/%d", device_id);
      Serial.println("Publish connect to");
      Serial.println(target_topic);

      String localIp = String(WiFi.localIP()[0]) + "." + 
        String(WiFi.localIP()[1]) + "." + 
        String(WiFi.localIP()[2]) + "." + 
        String(WiFi.localIP()[3]);
      client.publish(target_topic, localIp.c_str());
      // ... and resubscribe
      sprintf(target_topic, "devices/actions/%d", device_id);
      
      Serial.println("Subscribe to");
      Serial.println(target_topic);
      client.subscribe(target_topic);
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
    reconnect();
  }
  client.loop();

//  long now = millis();
//  if (now - lastMsg > 10000) {
//    lastMsg = now;
//    ++value;
//    snprintf (msg, 75, "hello world #%ld", value);
//    Serial.print("Publish message: ");
//    Serial.println(msg);
//    client.publish("devices/updates/1", msg);
//  }
}
