char val ;

#define forward A2
#define backward A3
#define right A4
#define left A5

int S;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600) ;

  pinMode( A1, OUTPUT ) ;
  pinMode( forward, OUTPUT ) ;
  pinMode( right, OUTPUT ) ;
  pinMode( backward, OUTPUT ) ;
  pinMode( left, OUTPUT ) ;

  digitalWrite( A1, LOW ) ;
  digitalWrite( forward, HIGH ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, HIGH ) ;

}

void loop() {
  // put your main code here, to run repeatedly:
  
  if( Serial.available() ) {

    Serial.print( "Reading Input: " ) ;

    delay(100) ;
    while( Serial.available() > 0 ) {
      
      val = Serial.read() ;
      Serial.print( val ) ;
      if( val != 0 ) {
        break ;
      }
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
      Serial.print( "Evaluated K correctly" ) ;
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
  val = 0 ;
}

void stp() {

  digitalWrite( forward, HIGH ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, HIGH ) ;
  Serial.print( "Stopping" ) ;
  
}

void fwd() {

  digitalWrite( forward, LOW ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, HIGH ) ;
  Serial.print( "Moving Forward" ) ;
  
}

void rt() {

  digitalWrite( forward, HIGH ) ;
  digitalWrite( right, LOW ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, HIGH ) ;
  Serial.print( "Move Right" ) ;
  
}

void bkwd() {

  digitalWrite( forward, HIGH ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, LOW ) ;
  digitalWrite( left, HIGH ) ;
  Serial.print( "Moving Backward" ) ;
  
}

void lft() {

  digitalWrite( forward, HIGH ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, LOW ) ;
  Serial.print( "Move Left" ) ;
  
}

void diagonal_left() {

  digitalWrite( forward, LOW ) ;
  digitalWrite( right, HIGH ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, LOW ) ;
  Serial.print( "Diagonal Left" ) ;
  
}

void diagonal_right() {

  digitalWrite( forward, LOW ) ;
  digitalWrite( right, LOW ) ;
  digitalWrite( backward, HIGH ) ;
  digitalWrite( left, HIGH ) ;
  Serial.print( "Diagonal Right" ) ;
  
}

