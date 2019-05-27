#define step_pin 9  // Pin 9 connected to Steps pin on EasyDriver
#define dir_pin 13   // Pin 13 connected to Direction pin
#define MS1 10       // Pin 10 connected to MS1 pin
#define MS2 11       // Pin 11 connected to MS2 pin
#define SLEEP 12     // Pin 12 connected to SLEEP pin

#define step_pin_2 3 // Pin 3 connected to Steps pin on EasyDriver
#define dir_pin_2 7 // Pin 7 connected to Direction pin
#define MS1_2 5       // Pin 5 connected to MS1 pin
#define MS2_2 6       // Pin 6 connected to MS2 pin
#define SLEEP_2 8     // Pin 8 connected to SLEEP pin

#define Limit01 2  // Pin 2 connected to Limit switch 1 out
#define Limit02 4  // Pin 4 connected to Limit switch 2 out

#define Onswitch 1 //Pin 1 connected to "on"
int step_speed = 1;  // Speed of Stepper motor (higher = slower)
int count = 0;
int count_max = 0;
int y = 0;
int y_max = 0;
int dir = 0;
int ok = 1;
int ok_2 = 1;
int wait_time = 500; // time for each picture in millisecs
int delta_t = 100; //Still have to experiment how much motor 2 moves the camera up
int i = 0;
int h = 0;
int yes =0;
char py_input;
void setup() {
   pinMode(MS1, OUTPUT);
   pinMode(MS2, OUTPUT);
   pinMode(dir_pin, OUTPUT);
   pinMode(step_pin, OUTPUT);
   pinMode(SLEEP, OUTPUT);

   pinMode(MS1_2, OUTPUT);
   pinMode(MS2_2, OUTPUT);
   pinMode(dir_pin_2, OUTPUT);
   pinMode(step_pin_2, OUTPUT);
   pinMode(SLEEP_2, OUTPUT);
   
   pinMode(Limit01, INPUT_PULLUP);
   pinMode(Limit02, INPUT_PULLUP);
   pinMode(Onswitch, INPUT_PULLUP);
   
   
   
   digitalWrite(SLEEP, HIGH);  // Wake up EasyDriver
   delay(5);  // Wait for EasyDriver wake up
   digitalWrite(SLEEP_2, HIGH);  // Wake up EasyDriver
   delay(5);  // Wait for EasyDriver_2 wake up
/* Configure type of Steps on EasyDriver:
// MS1 MS2
//
// LOW LOW = Full Step //
// HIGH LOW = Half Step //
// LOW HIGH = A quarter of Step //
// HIGH HIGH = An eighth of Step //
*/

   digitalWrite(MS1, LOW);      // Configures to Full Steps
   digitalWrite(MS2, LOW);    // Configures to Full Steps

   digitalWrite(MS1_2, LOW);      // Configures to Full Steps
   digitalWrite(MS2_2, LOW);    // Configures to Full Steps
   Serial.begin(9600);
   Serial.write('1');
   

}
void (* resetFunc) (void) =0;

void loop() {
  if (Serial.available()>0) {
    
  while(1){
  digitalWrite(dir_pin, LOW);  // (HIGH = anti-clockwise / LOW = clockwise)
  digitalWrite(step_pin, HIGH);
  delay(step_speed);
  digitalWrite(step_pin, LOW);
  delay(step_speed);
  count=count + 1;
  if (!digitalRead(Limit01)) {  // check if limit switch is activated
    count_max=count;
    dir=0;
    
    while (ok==1) {
    digitalWrite(dir_pin_2, LOW);  // (HIGH = anti-clockwise / LOW = clockwise)
    digitalWrite(step_pin_2, HIGH);
    delay(step_speed);
    digitalWrite(step_pin_2, LOW);
    delay(step_speed);
    y=y+1;

    
    if (!digitalRead(Limit02)) {  // check if limit switch 2 is activated
    y_max=y;
    dir=0;
    delta_t=y_max/4;
    Serial.write('2');
    //delay(1000);
    //Serial.write('0');
 y=0;
   while (ok_2==1){
    
    py_input=Serial.read();
    if (py_input=='1'){
      yes=1;
    }
      while (yes==1){
    if (dir==0){
      if (count>0){
        digitalWrite(dir_pin, HIGH);  // (HIGH = anti-clockwise / LOW = clockwise)
        digitalWrite(step_pin, HIGH);
        delay(step_speed);
        digitalWrite(step_pin, LOW);
        delay(step_speed);
        count=count- 1;
        h=h+1;
        //Serial.write('1');
        if(h==count_max/2){
          yes=0;
         //Serial.write('0'); 
         h=0;
        }
        if(count==0){
          yes=0;
         Serial.write('0');
         h=0; 
        }
      }
        py_input=Serial.read();
        if (count==0){
          py_input=Serial.read();
          if (py_input=='1'){
            yes=1;
          }
          if (yes==1){
          while (i<=delta_t){
           digitalWrite(dir_pin_2, HIGH);  // (HIGH = anti-clockwise / LOW = clockwise)
           digitalWrite(step_pin_2, HIGH);
           delay(step_speed);
           digitalWrite(step_pin_2, LOW);
           delay(step_speed);
           y=y-1;
           i=i+1;
           //Serial.write('1'); 
           if (y<=0){
            
            
              while(1){
                Serial.write('3');
                py_input=Serial.read();
               if (py_input=='4'){
              
              
              resetFunc();
               }
              
            }
          }
          }
          yes=0;
          i=0;
          dir=1;
          }
         
    }
    }
   if(yes==1){
    if (dir==1){
      if (count<count_max){
        digitalWrite(dir_pin, LOW);  // (HIGH = anti-clockwise / LOW = clockwise)
        digitalWrite(step_pin, HIGH);
        delay(step_speed);
        digitalWrite(step_pin, LOW);
        delay(step_speed);
        count=count+ 1;
         h=h+1;
         //Serial.write('1');
        if(h==count_max/2 ){
         //Serial.write('0'); 
         yes=0;
         h=0;
        }
        if(count==count_max){
          //Serial.write('0');
          yes=0;
          h=0;
        }
      }
        if (count==count_max){
          //yes=0;
        py_input=Serial.read();    
           if (py_input=='1'){
            yes=1;
           }
           if(yes==1){
           while (i<=delta_t){
           digitalWrite(dir_pin_2, HIGH);  // (HIGH = anti-clockwise / LOW = clockwise)
           digitalWrite(step_pin_2, HIGH);
           delay(step_speed);
           digitalWrite(step_pin_2, LOW);
           delay(step_speed);
           y=y-1;
           i=i+1;
           //Serial.write('1');
           
           if (y<=0){
            //Serial.write('0');
            yes=0;
            while (1){
              py_input=Serial.read();
            if (py_input=='1'){
              yes=1;
            }
            h=0;
            while(yes==1){
             digitalWrite(dir_pin, HIGH);  // (HIGH = anti-clockwise / LOW = clockwise)
            digitalWrite(step_pin, HIGH);
            delay(step_speed);
            digitalWrite(step_pin, LOW);
            delay(step_speed);
            count=count- 1;
            //Serial.write('1');
             h=h+1;
             if(h==count_max/2){
            //Serial.write('0'); 
            yes=0;
             h=0;
            }
            if (count==0){
              
              while(1){
                Serial.write('3');
                py_input=Serial.read();
               if (py_input=='4'){
              
              
              resetFunc();
               }
              }

            }
            
              
            }
          }
           }
           }
           yes=0;
           i=0;
          dir=0; 
           }
          }
         
          
            }
   }
          }
   }
        }
    }
    
  }
}
  }
}
