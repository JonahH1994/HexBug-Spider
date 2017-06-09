  #include <ESP8266WiFi.h>
  
  const char* ssid     = "HexBugSpi";
  const char* password = "hexhexbug";

  #define MAX_SRV_CLIENTS 1
  
  IPAddress host(192, 168, 1, 8 ) ;
  const int portOne = 80 ;
  
  // IP for HexBugSpi:
  IPAddress ip( 192, 168, 137, 103 ) ;
  IPAddress gateway(192, 168, 43, 1);
  IPAddress subnet(255, 255, 255, 0);
  
  WiFiServer server( portOne ) ;
  WiFiClient serverClients[MAX_SRV_CLIENTS] ;
  
  byte packetBuffer[512] ;
  
  char val ;
  
  // 15, 0, 16, 2
  
  #define EN1 13 // A3
  #define IN1 12 // A2
  #define EN2 5 // A5
  #define IN2 14 // A4
  
  // IN1/IN2 Low -- ENA1/ENA2 - Forward
  // K stopped motion
  // S moves forward
  
  
  int S;
  
  void setup() {
    // put your setup code here, to run once:
  
    Serial.begin(115200) ;
  
    //pinMode( 0, OUTPUT ) ;
    //pinMode( 
    //digitalWrite( 0, LOW ) ;
  
    delay( 100 ) ;
  
    pinMode( 4, OUTPUT ) ;
    pinMode( EN1, OUTPUT ) ;
    pinMode( IN1, OUTPUT ) ;
    pinMode( EN2, OUTPUT ) ;
    pinMode( IN2, OUTPUT ) ;
  
    digitalWrite( 13, LOW ) ;
    digitalWrite( 4, LOW ) ;
  
    WiFi.persistent(false);
    WiFi.mode(WIFI_OFF);
    WiFi.mode(WIFI_STA);
  
    WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  
    delay( 1000 ) ;
    server.begin() ;
      
  }
  
  void loop() {
    // put your main code here, to run repeatedly:
  
    if( server.hasClient() ) {
  
      serverClients[0] = server.available() ;
      Serial.println( "Have Client" ) ;

    }

  //Serial.println( serverClients[0].available() ) ;
  while( serverClients[0].connected() ) {
    Serial.println( "Reading Input: " ) ;

    delay( 100 ) ;
    //val = 0 ;
    //while( val == 0 || val == (char)0 ) 
       //val = serverClients[0].read() ;

    //Serial.println( val == 's' ) ;
    val = serverClients[0].read() ;

    if ( val == 'S' || val == 's' ) {
      stp() ;
    }

    // Move the bot forward
    if ( val == 'I' || val == 'i' ) {
      fwd() ;
    }
  
    // Move the bot to the right
    if( val == 'L' || val == 'l' ) {
      rt() ;
    }
  
    // Move the bot to the left
    if( val == 'J' || val == 'j' ) {
      lft() ;
    }
  
    // Move the bot backward
    if( val == 'K' || val == 'k' ) {
      Serial.println( "Evaluated K correctly" ) ;
      bkwd() ;
    }
  
    // Bot spins in circles toward the right
    if( val == 'O' || val == 'o' ) {
      diagonal_right() ;
    }
  
    // Bot spins in circles toward the left
    if( val == 'U' || val == 'u' ) {
      diagonal_left() ;
    }
  }

  serverClients[0].stop() ;
  
}

void stp() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Stopping" ) ;

}

void fwd() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Moving Forward" ) ;

}

void rt() {

digitalWrite( IN1, HIGH ) ; 
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, HIGH ) ;
Serial.println( "Move Right" ) ;

}

void bkwd() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Moving Backward" ) ;

}

void lft() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Move Left" ) ;

}

void diagonal_left() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Diagonal Left" ) ;

}

void diagonal_right() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, HIGH ) ;
Serial.println( "Diagonal Right" ) ;

}

