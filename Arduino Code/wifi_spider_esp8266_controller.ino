char val ;

#define EN1 A3
#define IN1 A2
#define EN2 A5
#define IN2 A4

// IN1/IN2 Low -- ENA1/ENA2 - Forward
// K stopped motion
// S moves forward


int S;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600) ;

  pinMode( A1, OUTPUT ) ;
  pinMode( EN1, OUTPUT ) ;
  pinMode( IN1, OUTPUT ) ;
  pinMode( EN2, OUTPUT ) ;
  pinMode( IN2, OUTPUT ) ;

  digitalWrite( A1, LOW ) ;
    
}

void loop() {
  // put your main code here, to run repeatedly:

  if( Serial.available() ) {

    Serial.println( "Reading Input: " ) ;

    delay( 100 ) ;
    while( Serial.available() > 0 ) {

      val = Serial.read()  ;
      if( val != 0 )
        break ;
      
    }

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
}

void stp() {

  digitalWrite( IN1, HIGH ) ;
  digitalWrite( IN2, HIGH ) ;
  digitalWrite( EN1, HIGH ) ;
  digitalWrite( EN2, HIGH ) ;
  Serial.println( "Stopping" ) ;
  
}

void fwd() {

  digitalWrite( IN1, LOW ) ;
  digitalWrite( IN2, HIGH ) ;
  digitalWrite( EN1, HIGH ) ;
  digitalWrite( EN2, HIGH ) ;
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
  digitalWrite( IN2, LOW ) ;
  digitalWrite( EN1, LOW ) ;
  digitalWrite( EN2, LOW ) ;
  Serial.println( "Moving Backward" ) ;
  
}

void lft() {

  digitalWrite( IN1, HIGH ) ;
  digitalWrite( IN2, LOW ) ;
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

