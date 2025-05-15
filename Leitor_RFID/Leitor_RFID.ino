#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Configurações do WiFi
const char* ssid = "NOME_DA_REDE_WIFI";
const char* password = "SENHA";

// Configurações do servidor Django
const String serverUrl = "ENDERECO_IP_DO_ENDPOINT";

// Configurações de hardware
#define SS_PIN    5   // RFID SDA
#define RST_PIN  21   // RFID RST
#define BUZZER_PIN 22 // Buzzer passivo
#define LED_PIN   2   // LED interno para feedback

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  
  connectWiFi();
  Serial.println("Sistema RFID Pronto");
}

void loop() {
  // Verifica conexão WiFi
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Verifica nova leitura de cartão
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  digitalWrite(LED_PIN, HIGH);
  String tagUID = getTagUID();
  Serial.print("UID Lido: ");
  Serial.println(tagUID);

  // Envia para o servidor
  String response = sendToServer(tagUID);
  handleServerResponse(response);

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  digitalWrite(LED_PIN, LOW);
  delay(1000); // Delay para evitar leituras múltiplas
}

// Função para conectar/reconectar ao WiFi
void connectWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConectado! IP: " + WiFi.localIP().toString());
}

// Gera o UID da tag em formato string
String getTagUID() {
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  return uid;
}

// Envia dados para o servidor
String sendToServer(String tagUID) {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"tag_uid\":\"" + tagUID + "\"}";
  int httpCode = http.POST(payload);
  String response = http.getString();
  
  Serial.print("Status Code: ");
  Serial.println(httpCode);
  Serial.print("Resposta: ");
  Serial.println(response);

  http.end();
  return response;
}

// Controla o buzzer baseado na resposta
void handleServerResponse(String response) {
  if (response.indexOf("entry_registered") != -1) {
    // Entrada registrada - tom alto
    playTone(1500, 200);
    playTone(2000, 200);
  } else if (response.indexOf("exit_registered") != -1) {
    // Saída registrada - tom baixo
    playTone(1000, 200);
    playTone(500, 200);
  } else {
    // Erro - tom intermitente
    for(int i=0; i<3; i++) {
      playTone(800, 100);
      delay(100);
    }
  }
}

// Toca um tom no buzzer passivo
void playTone(int frequency, int duration) {
  tone(BUZZER_PIN, frequency, duration);
  delay(duration);
  noTone(BUZZER_PIN);
}