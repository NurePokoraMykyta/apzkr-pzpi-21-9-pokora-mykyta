#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length);
void sendSensorData();
void updateLCD(float temp, float ph, float salinity, float oxygen);
void updateStatusLCD(bool connected);
void feed();

#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define SERVO_PIN 2
#define PH_PIN 14
#define SALINITY_PIN 13
#define OXYGEN_PIN 12

LiquidCrystal_I2C lcd(0x27, 16, 2);

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* websockets_server = "host.wokwi.internal";
const uint16_t websockets_port = 8000;
const char* websockets_route = "/ws/ESP32_001";
const char* unique_address = "ESP32_001";


WebSocketsClient webSocket;
bool is_active = false;
bool is_connected = false;

void setup() {
  Serial.begin(115200);
  dht.begin();

  Wire.begin();
  lcd.init();
  lcd.backlight();

  pinMode(SERVO_PIN, OUTPUT);
  pinMode(34, INPUT);
  pinMode(32, INPUT);
  pinMode(35, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Підключення до WiFi...");
  }
  Serial.println("Підключено до WiFi");
  Serial.print("IP адреса: ");
  Serial.println(WiFi.localIP());

  Serial.print("Підключення до WebSocket: ");
  webSocket.begin(websockets_server, websockets_port, websockets_route);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();

  if (is_active) {
    static unsigned long lastTime = 0;
    unsigned long now = millis();
    if (now - lastTime > 600) {
      lastTime = now;
      sendSensorData();
    }
  } else {
    updateStatusLCD(is_connected);
  }
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  JsonDocument doc;

  switch(type) {
    case WStype_DISCONNECTED:
      Serial.println("Від'єднано від WebSocket сервера");
      is_connected = false;
      updateStatusLCD(is_connected);
      break;
    case WStype_CONNECTED:
      Serial.println("Підключено до WebSocket сервера");
      is_connected = true;
      updateStatusLCD(is_connected);
      webSocket.sendTXT("{\"action\":\"identify\",\"unique_address\":\"" + String(unique_address) + "\"}");
      break;
    case WStype_TEXT:
      Serial.printf("Отримано повідомлення: %s\n", payload);
      if (deserializeJson(doc, payload) == DeserializationError::Ok) {
        if (doc["action"] == "activate") {
          is_active = true;
          Serial.println("Пристрій активовано");
        } else if (doc["action"] == "deactivate") {
          is_active = false;
          Serial.println("Пристрій деактивовано");
          updateStatusLCD(is_connected);
        } else if (doc["action"] == "feed" && is_active) {
          feed();
        }
      } else {
        Serial.println("Помилка розбору JSON");
      }
      break;
    case WStype_ERROR:
      Serial.println("Помилка WebSocket з'єднання");
      break;
    case WStype_PING:
      Serial.println("Ping отримано");
      break;
    case WStype_PONG:
      Serial.println("Pong отримано");
      break;
  }
}

void sendSensorData() {
  if (!is_active) return;

  float rawPH = analogRead(34);
  float rawSalinity = analogRead(32);
  float rawOxygen = analogRead(35);
  float rawTemperature = dht.readTemperature();

  JsonDocument doc;
  doc["action"] = "water_parameters";
  doc["unique_address"] = unique_address;
  doc["parameters"]["ph"] = rawPH;
  doc["parameters"]["temperature"] = rawTemperature;
  doc["parameters"]["salinity"] = rawSalinity;
  doc["parameters"]["oxygen_level"] = rawOxygen;
  doc["parameters"]["measured_at"] = String(millis());

  String jsonString;
  serializeJson(doc, jsonString);
  webSocket.sendTXT(jsonString);

  updateLCD(rawTemperature, rawPH, rawSalinity, rawOxygen);

  Serial.printf("pH: %.2f, Temperature: %.2f°C, Salinity: %.2f ppt, Oxygen: %.2f mg/L\n",
                rawPH, rawTemperature, rawSalinity, rawOxygen);
}

void updateLCD(float temp, float ph, float salinity, float oxygen) {
  if (!is_active) return;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.printf("T:%.1f pH:%.1f", temp, ph);
  lcd.setCursor(0, 1);
  lcd.printf("S:%.1f O2:%.1f", salinity, oxygen);
}

void updateStatusLCD(bool connected) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(connected ? "WS: Connected" : "WS: Disconnected");
  lcd.setCursor(0, 1);
  lcd.print(is_active ? "Device: Active" : "Device: Inactive");
}

void feed() {
  if (is_active) {
    Serial.println("Годування...");
    for (int pos = 0; pos <= 180; pos += 1) {
      digitalWrite(SERVO_PIN, HIGH);
      delayMicroseconds(pos * 10 + 600);
      digitalWrite(SERVO_PIN, LOW);
      delay(20);
    }
    webSocket.sendTXT("{\"action\":\"feed_result\",\"success\":true,\"unique_address\":\"" + String(unique_address) + "\"}");
    Serial.println("Годування завершено");
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Feeding...");
    delay(2000);
    sendSensorData();
  }
}