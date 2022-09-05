#include <string.h>
using namespace std;

int pins[55];
bool status[55];
bool sp_state;

int SHIFTA = 11;
int SHIFTB = 21;
int SYM1A = 20;
int SYM1B = 22;
int SYM2 = 3;
int CONTROL = 0;
int ALT = 2;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 33; i++) {
    pins[i] = i + 2;
  }
  for (int i = 33; i < 51; i++) {
    pins[i] = i + 3;
  }
  
  pins[51] = A0;
  pins[52] = A1;
  pins[53] = A2;
  pins[54] = A3;
  
  for (int i = 0; i < 55; i++) {
    pinMode(pins[i], INPUT_PULLUP);
    status[i] = false;
  }
  sp_state = false;
}

void loop() {
  // check for modifiers
  bool is_shift = !digitalRead(pins[SHIFTA]) || !digitalRead(pins[SHIFTB]);
  bool is_sym1 =!digitalRead(pins[SYM1A]) || !digitalRead(pins[SYM1B]);
  bool is_sym2 =!digitalRead(pins[SYM2]);
  bool is_control = !digitalRead(pins[CONTROL]);
  bool is_alt = !digitalRead(pins[ALT]);
  
  // make list of changes
  bool situationChanged = false;
  String turnedOff;
  String turnedOn;
  
  for (int i = 0; i < 55; i++) {
    if (i != 4 && i != 5 && i != 6) {
      bool previousState = status[i];
      bool currentState = !digitalRead(pins[i]);
      
      // detect change in keys
      if (previousState != currentState) {
        situationChanged = true;
        
        if (i != SHIFTA && i != SHIFTB && i != SYM1A && i != SYM2 && i != SYM1B && i != CONTROL && i != ALT) {
          // add key to a list to either press or unpress
          if (currentState == false) {
            turnedOff += i;
            turnedOff += ",";
          } 
          else {
            turnedOn += i;
            turnedOn += ",";
          }
        }  
      }
      
      // update status array
      status[i] = currentState;
    } 
    else {
      // This is if i is one of the spacebar keys
      status[i] = !digitalRead(pins[i]);
      if (sp_state == false && (status[i] == true)) {
        situationChanged = true;
        sp_state = true;
        turnedOn += 4;
        turnedOn += ",";
      } else if (sp_state == true && status[4] == false && status[5] == false && status[6] == false) {
        situationChanged = true;
        sp_state = false;
        turnedOff += 4;
        turnedOff += ",";
      }
    }
    
  }
  
  if (situationChanged) {
    // print modifier status string
    String output;
    output +=(is_shift ? "Y" : "N");
    output +=(is_sym1 ? "Y" : "N");
    output +=(is_sym2 ? "Y" : "N");
    output += (is_control ? "Y" : "N");
    output += (is_alt ? "Y" : "N");
    output +="/";
    // print released keys
    output +=turnedOff;
    output += "/";
    
    // print newly pressed keys
    output += turnedOn;
    Serial.println(output);
    
  }
  
}
