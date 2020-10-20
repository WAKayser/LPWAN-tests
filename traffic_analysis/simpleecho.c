// Simple serial echo towards modem
// Used to create a simple interface to send AT commands from a PC

#if defined(ARDUINO_SODAQ_SARA)
#define DEBUG_STREAM SerialUSB
#define MODEM_STREAM Serial1

#else
#error "Please select the SODAQ SARA as your board"
#endif

unsigned long baud = 115200;

void setup() {
  pinMode(SARA_ENABLE, OUTPUT);
  pinMode(SARA_TX_ENABLE, OUTPUT);
  pinMode(SARA_R4XX_TOGGLE,OUTPUT);

  digitalWrite(SARA_ENABLE,HIGH);
  digitalWrite(SARA_TX_ENABLE,HIGH);
  digitalWrite(SARA_R4XX_TOGGLE,LOW);


  // Start communication
  DEBUG_STREAM.begin(baud);
  MODEM_STREAM.begin(baud);
}

// Forward every message to the other serial
void loop() {
  while (DEBUG_STREAM.available()) {
    MODEM_STREAM.write(DEBUG_STREAM.read());
  }

  while (MODEM_STREAM.available()) {     
    DEBUG_STREAM.write(MODEM_STREAM.read());
  }
} 
