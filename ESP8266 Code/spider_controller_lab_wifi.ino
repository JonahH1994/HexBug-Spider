  #include <ESP8266WiFi.h>

  //const char* ssid     = "HexBugSpi";
  //const char* password = "hexhexbug";

  const char* ssid      = "Mark_AP_N" ;
  const char* password  = "ASL Nerd Herd!" ;

  #define MAX_SRV_CLIENTS 1
  
  //IPAddress host(192, 168, 1, 8 ) ;
  const int portOne = 80 ;
  
  // IP for HexBugSpi:
  //IPAddress ip( 10, 84, 189, 149 )  ;
  //IPAddress gateway( 128, 84, 189, 1 ) ;
  //IPAddress ip( 199, 168, 1, 4 ) ;
  //IPAddress gateway(199, 168, 1, 120);
  //IPAddress subnet(255, 255, 255, 0);
  
  WiFiServer server( portOne ) ;
  WiFiClient serverClients[MAX_SRV_CLIENTS] ;
  
  byte packetBuffer[512] ;
  
  char val ;
  char prevVal = 'y' ;
  int count ;
  
  // 15, 0, 16, 2
  
  #define EN1 14 // A3
  #define IN1 5 // A2
  #define EN2 12 // A5
  #define IN2 13 // A4
  
  // IN1/IN2 Low -- ENA1/ENA2 - Forward
  // K stopped motion
  // S moves forward
  
  
  int S;

  void startWIFI(void) {
    
    // Connect to WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);
    delay(10);

    WiFi.persistent(false);
    WiFi.mode(WIFI_OFF);
    WiFi.mode(WIFI_STA);

    //WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("");
    Serial.println("WiFi connected");

    delay(100) ;
    server.begin() ;
    delay(50) ;

    // Print the IP address
    Serial.print("ESP8266 IP: ");
    Serial.println(WiFi.localIP());
}

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

    //WiFi.config(ip, gateway, subnet);
    WiFi.begin(ssid, password);
      
    //WiFi.config(ip, gateway, subnet);
    //WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      yield() ;
      Serial.print(".");
    }
    Serial.print("Connected!");
    Serial.print(WiFi.localIP()) ;
  
    delay( 1000 ) ;
    yield();
    server.begin() ;
      
  }

  unsigned long tim = millis() ;
  int check = 0 ;
  void loop() {
    // put your main code here, to run repeatedly:
  
    if( server.hasClient() ) {
  
      serverClients[0] = server.available() ;
      Serial.println( "Have Client" ) ;

    }

    if (WiFi.status() != WL_CONNECTED) {
      startWIFI() ;
    }

  //Serial.println( serverClients[0].available() ) ;
  while( serverClients[0].connected() ) {
    Serial.println( "Reading Input: " ) ;
    /*
    if (check == 1) {
      tim = millis() ;
      check= 0 ;
    } else if ( prevVal == 'i' || prevVal =='I' ) {
      Serial.println( "Timeout has occured!!!" ) ;
      if (millis()-tim >= 200) {
        stp() ;
        //tim = millis() ;
      }
    } else {
      if (millis() -tim >= 250 ) {
        stp() ; 
        //tim = millis() ;
      }
    }
    */

    delay(100);
    yield();

    //delay( 100 ) ;
    //val = 0 ;
    //while( val == 0 || val == (char)0 ) 
       //val = serverClients[0].read() ;

    count = 0 ;
    //Serial.println( val == 's' ) ;
    /*
    while ( val == 0 ) {
      val = serverClients[0].read() ;
      count += 1 ;
      if( count == 25) {
        stp() ;
      }
    }
    */
    //stream.flush() ;
    val = serverClients[0].read() ;
    serverClients[0].flush() ;
    Serial.println(val) ;
    Serial.println(tim) ;
    //serverClients[0].write('3') ;

    if ( val == 'S' || val == 's' ) {
      stp() ;
      check= 1 ;
      prevVal = val ;
    }

    // Move the bot forward
    if ( val == 'I' || val == 'i' ) {
      fwd() ;
      check =1 ;
      prevVal = val ;
    }
  
    // Move the bot to the right
    if( val == 'L' || val == 'l' ) {
      rt() ;
      check = 1;

      if (prevVal != val ) {
        prevVal = val ;
      } else {
        check = 0 ;
      }
    }
  
    // Move the bot to the left
    if( val == 'J' || val == 'j' ) {
      lft() ;
      check = 1 ;
      if (prevVal != val ) {
        prevVal = val ;
      } else {
        check = 0 ;
      }
    }
  
    // Move the bot backward
    if( val == 'K' || val == 'k' ) {
      Serial.println( "Evaluated K correctly" ) ;
      bkwd() ;
      check =1 ;
      prevVal = val ;
    }
  
    // Bot spins in circles toward the right
    if( val == 'O' || val == 'o' ) {
      diagonal_right() ;
      check =  1 ;
      if (prevVal != val ) {
        prevVal = val ;
      } else {
        check = 0 ;
      }
    }
  
    // Bot spins in circles toward the left
    if( val == 'U' || val == 'u' ) {
      diagonal_left() ;
      check =1;
      if (prevVal != val ) {
        prevVal = val ;
      } else {
        check = 0 ;
      }
    }
  }

  serverClients[0].stop() ;

  if (!server.hasClient()){
    stp() ; 
  }
  
}

void stp() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Stopping" ) ;

}

void fwd() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Moving Forward" ) ;

}

void rt() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, HIGH ) ;
Serial.println( "Move Right" ) ;

}

void bkwd() {

digitalWrite( IN1, LOW ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, HIGH ) ;
Serial.println( "Moving Backward" ) ;

}

void lft() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, LOW ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, HIGH ) ;
Serial.println( "Move Left" ) ;

}

void diagonal_left() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, LOW ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Diagonal Left" ) ;

}

void diagonal_right() {

digitalWrite( IN1, HIGH ) ;
digitalWrite( IN2, HIGH ) ;
digitalWrite( EN1, HIGH ) ;
digitalWrite( EN2, LOW ) ;
Serial.println( "Diagonal Right" ) ;

}

