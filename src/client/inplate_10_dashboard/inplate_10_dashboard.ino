#include <Inkplate.h>
#include "secrets.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

Inkplate display(INKPLATE_3BIT);
int count = 0;
char str[20];
const char* DASHBOARD_URL = "192.168.178.42";

int getTimingInfo() {
    Serial.println("Getting timing info...");
    HTTPClient http;
    http.begin("http://192.168.178.42:8000/timing/");
    int httpResponseCode = http.GET();

    if (httpResponseCode == 200) {
        String payload = http.getString();
        http.end();

        // Deserialize JSON
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, payload);

        // Access "time_to_sleep" from JSON response
        int sleep_duration = doc["time_to_sleep"].as<int>() * 1000;
        return sleep_duration;

    } else {
        Serial.printf("Could not get timing info: %d\n", httpResponseCode);
        http.end();
        return 10;
    }
}

void setup() {
    Serial.begin(115200);

  display.begin();
  while (!display.connectWiFi(ssid, pass)) {
    Serial.println("Connecting to wifi...");
    delay(1000);
  }
  Serial.println("Connected to wifi!");
  display.clearDisplay();
}

void loop() {
  Serial.println("Starting Loop!");
  Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());

  HTTPClient http;
  http.begin("http://192.168.178.42:8000/dashboard/");
  int httpResponseCode = http.POST("");
  Serial.println("Triggered dashboard construction!");
  delay(30000);

  display.clearDisplay();
  Serial.println("Cleared Display!");

  display.drawBitmapFromWeb("http://192.168.178.42:8000/dashboard/", 0, 0);
  Serial.println("drew bitmap!");
  display.display();
  Serial.println("Displayed dashboard!");
  int sleep_duration = getTimingInfo();
  Serial.printf("sleeping for %d ms...\n", sleep_duration);
  delay(sleep_duration);
}
