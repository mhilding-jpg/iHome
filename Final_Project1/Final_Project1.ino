#include <DHT.h>
#include <WiFiS3.h>
#include "ThingSpeak.h"
#define DHTPIN 2
#define DHTTYPE DHT11
#define PIRPIN 4
#define LEDPIN 13
#define SECRET_SSID "Max iPhone" // Add network id here
#define SECRET_PASS "00000000" // Add password here
#define SECRET_CH_ID 3312636 // Set the id of ThingSpeak 
#define SECRET_WRITE_APIKEY "2E61GHIR6Y102ZS2" // Set the api key of the ThingSpeak channel 
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
WiFiClient theClient;
unsigned long myChannelNumber = SECRET_CH_ID;
const char myWriteAPIKey[] = SECRET_WRITE_APIKEY;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ThingSpeak.begin(theClient); //Initialize a connection to 
  dht.begin();
  pinMode(PIRPIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:  
  if(WiFi.status()!=WL_CONNECTED){
    Serial.print("Attempting to connect to SSID:");
    Serial.println(SECRET_SSID);
    // Check if Wifi is connected
    while (WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid, pass);      
      delay(5000);
    }
  } 
  float humd = dht.readHumidity();
  float temp = dht.readTemperature();
  float motion = digitalRead(PIRPIN); //0 or 1
  Serial.print("<temp=");
  Serial.print(temp);
  Serial.print(",humd=");
  Serial.print(humd);
  Serial.print(",motion=");
  Serial.print(motion);
  Serial.println(">");

  if (motion) {
    digitalWrite(LEDPIN, HIGH);
  }
  else {
    digitalWrite(LEDPIN, LOW);
  }
  ThingSpeak.setField(1, humd); // Set Field 1 to the value of 
  ThingSpeak.setField(2, temp); // Set Field 2 to the value of
  ThingSpeak.setField(3, motion); // Set Field 3 to the value of
  
  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey); // Write 
  if (x==200){
   Serial.println("Channel update successful ");
  }
  else{
   Serial.println("Problem updating channel.");
  }
  delay(15000);

}
