const int LED1_R = 13;
const int LED1_G = 11;
const int LED1_B = 12;

const int LED2_R = 10;
const int LED2_G = 9;
const int LED2_B = 8;

const int LED3_R = 7 ;
const int LED3_G = 6;
const int LED3_B = 5;

const int LED4_R = 4;
const int LED4_G = 3;
const int LED4_B = 2;

const int I_R = 36;
const int I_Y = 42;
const int I_B = 46;
const int I_G = 38;



int FBD = 325;
int FDL = 8;
int FD = 30000 - 20000/9*FDL;
int FN = 3;
int ODL = 5;
int OD = 2000 - 500/3*ODL;

int w = 0;
int x = 0;
int y = 0;
int z = 0;

String answer = "";

int hoop_w = 0;
int hoop_x = 0;
int hoop_y = 0;
int hoop_z = 0;

char inByte;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(5000);
  
  pinMode(LED1_R, OUTPUT);
  pinMode(LED1_G, OUTPUT);
  pinMode(LED1_B, OUTPUT);

  pinMode(LED4_R, OUTPUT);
  pinMode(LED4_G, OUTPUT);
  pinMode(LED4_B, OUTPUT);

  pinMode(LED3_B, OUTPUT);
  pinMode(LED3_R, OUTPUT);
  pinMode(LED3_G, OUTPUT);

  pinMode(LED2_R, OUTPUT);
  pinMode(LED2_G, OUTPUT);
  pinMode(LED2_B, OUTPUT);

  pinMode(I_R, INPUT);
  pinMode(I_Y, INPUT);
  pinMode(I_G, INPUT);
  pinMode(I_B, INPUT);


}


void loop() {
  if (Serial.available() > 0) {
    inByte = Serial.read();
    
    if (inByte == '3') {
      digitalWrite(LED3_B, HIGH);
      digitalWrite(LED3_R, HIGH);
      digitalWrite(LED3_G, HIGH);
      delay(OD);
      digitalWrite(LED3_R, LOW);
      digitalWrite(LED3_G, LOW);
      digitalWrite(LED3_B, LOW);
    }
    if (inByte == '2') {
      digitalWrite(LED2_R, HIGH);
      digitalWrite(LED2_G, HIGH);
      digitalWrite(LED2_B, HIGH);

      delay(OD);
      digitalWrite(LED2_R, LOW);
      digitalWrite(LED2_G, LOW);
      digitalWrite(LED2_B, LOW);
    }
    if (inByte == '4') {
      digitalWrite(LED4_R, HIGH);
      digitalWrite(LED4_G, HIGH);
      digitalWrite(LED4_B, HIGH);
      delay(OD);
      digitalWrite(LED4_R, LOW);
      digitalWrite(LED4_G, LOW);
      digitalWrite(LED4_B, LOW);
    }
    if (inByte == '1') {
      digitalWrite(LED1_R, HIGH);
      digitalWrite(LED1_G, HIGH);
      digitalWrite(LED1_B, HIGH);
      delay(OD);

      digitalWrite(LED1_R, LOW);
      digitalWrite(LED1_G, LOW);
      digitalWrite(LED1_B, LOW);
    }
    
    if(inByte == '5'){
      while ((digitalRead(I_R) == HIGH)&&(digitalRead(I_Y) == HIGH)&&(digitalRead(I_B) == HIGH)&&(digitalRead(I_G) == HIGH)){}
      if(digitalRead(I_R) == LOW){
        Serial.println("1");
      }
      if(digitalRead(I_Y) == LOW){
        Serial.println("2");
      }
      if(digitalRead(I_B) == LOW){
        Serial.println("3");
      }
      if(digitalRead(I_G) == LOW){
        Serial.println("4");
      }

    }
    
    if (inByte == 'a') {
      digitalWrite(LED3_R, HIGH); 
      digitalWrite(LED3_G, HIGH); 
      digitalWrite(LED3_B, HIGH); 

      digitalWrite(LED2_R, HIGH);  
      digitalWrite(LED2_G, HIGH);  
      digitalWrite(LED2_B, HIGH);  

      digitalWrite(LED4_R, HIGH); 
      digitalWrite(LED4_G, HIGH); 
      digitalWrite(LED4_B, HIGH); 

      digitalWrite(LED1_R, HIGH);  
      digitalWrite(LED1_G, HIGH);
      digitalWrite(LED1_B, HIGH);
      delay(FBD);
      for(int i = 0; i <= FN; i++) {
      
        digitalWrite(LED1_R, LOW);  
        digitalWrite(LED1_G, LOW);  
        digitalWrite(LED1_B, LOW);  
        delay(FBD);
        digitalWrite(LED1_R, HIGH);  
        digitalWrite(LED1_G, HIGH);
        digitalWrite(LED1_B, HIGH);
        delay(FBD);
      }
      digitalWrite(LED3_R, LOW);  
      digitalWrite(LED3_G, LOW);  
      digitalWrite(LED3_B, LOW);  

      digitalWrite(LED2_R, LOW);  
      digitalWrite(LED2_G, LOW);  
      digitalWrite(LED2_B, LOW);  

      digitalWrite(LED4_R, LOW); 
      digitalWrite(LED4_G, LOW); 
      digitalWrite(LED4_B, LOW); 

      digitalWrite(LED1_R, LOW);  
      digitalWrite(LED1_G, LOW);  
      digitalWrite(LED1_B, LOW);  
    
      delay (100);

      long start_time = millis();
      long end_time = start_time + FD;

      while ((digitalRead(I_R) == HIGH)&&(digitalRead(I_Y) == HIGH)&&(digitalRead(I_B) == HIGH)&&(digitalRead(I_G) == HIGH)){if (end_time<millis()){break;}}
      if(digitalRead(I_R)==LOW){
        Serial.println("H1+");
        digitalWrite(LED1_R, HIGH);
        digitalWrite(LED1_G, HIGH);
        digitalWrite(LED1_B, HIGH);
        delay(1000);
        digitalWrite(LED1_R,LOW);
        digitalWrite(LED1_G,LOW);
        digitalWrite(LED1_B,LOW);
      }
      if(digitalRead(I_Y)==LOW){
        Serial.println("F+-");
        digitalWrite(LED2_R, HIGH);
        digitalWrite(LED2_G, HIGH);
        digitalWrite(LED2_B, HIGH);
        delay(1000);
        digitalWrite(LED2_R,LOW);
        digitalWrite(LED2_G,LOW);
        digitalWrite(LED2_B,LOW);
      }
      if(digitalRead(I_B)==LOW){
        Serial.println("F+-");
        digitalWrite(LED3_R, HIGH);
        digitalWrite(LED3_G, HIGH);
        digitalWrite(LED3_B, HIGH);
        delay(1000);
        digitalWrite(LED3_R,LOW);
        digitalWrite(LED3_G,LOW);
        digitalWrite(LED3_B,LOW);
      }
      if(digitalRead(I_G)==LOW){
        Serial.println("F+-");
        digitalWrite(LED4_R, HIGH);
        digitalWrite(LED4_G, HIGH);
        digitalWrite(LED4_B, HIGH);
        delay(1000);
        digitalWrite(LED4_R,LOW);
        digitalWrite(LED4_G,LOW);
        digitalWrite(LED4_B,LOW);
      }
      if(millis()>end_time){
        Serial.println("F+-");
        digitalWrite(LED1_R,HIGH);
        digitalWrite(LED1_G,HIGH);
        digitalWrite(LED1_B,HIGH);
        delay(1000);
        digitalWrite(LED1_R,LOW);
        digitalWrite(LED1_G,LOW);
        digitalWrite(LED1_B,LOW);
      }
    }
    if (inByte == 'b') {
      digitalWrite(LED3_R, HIGH); 
      digitalWrite(LED3_G, HIGH); 
      digitalWrite(LED3_B, HIGH); 

      digitalWrite(LED2_R, HIGH);  
      digitalWrite(LED2_G, HIGH);  
      digitalWrite(LED2_B, HIGH);  

      digitalWrite(LED4_R, HIGH); 
      digitalWrite(LED4_G, HIGH); 
      digitalWrite(LED4_B, HIGH); 

      digitalWrite(LED1_R, HIGH);  
      digitalWrite(LED1_R, HIGH);  
      digitalWrite(LED1_R, HIGH);  
     delay(FBD);
      for(int i = 0; i <= FN; i++) {
        
        digitalWrite(LED2_R, LOW);  
        digitalWrite(LED2_G, LOW);  
        digitalWrite(LED2_B, LOW);  

        delay(FBD);
        digitalWrite(LED2_R, HIGH);  
        digitalWrite(LED2_G, HIGH);  
        digitalWrite(LED2_B, HIGH);  

        delay(FBD);
      }
      digitalWrite(LED3_R, LOW);  
      digitalWrite(LED3_G, LOW);  
      digitalWrite(LED3_B, LOW);  

      digitalWrite(LED2_R, LOW); 
      digitalWrite(LED2_G, LOW); 
      digitalWrite(LED2_B, LOW); 

      digitalWrite(LED4_R, LOW);  
      digitalWrite(LED4_G, LOW);  
      digitalWrite(LED4_B, LOW);  

      digitalWrite(LED1_R, LOW);
      digitalWrite(LED1_G, LOW);
      digitalWrite(LED1_B, LOW);
      delay (100);

      long start_time = millis();
      long end_time = start_time + FD;

      while ((digitalRead(I_R) == HIGH)&&(digitalRead(I_Y) == HIGH)&&(digitalRead(I_B) == HIGH)&&(digitalRead(I_G) == HIGH)){if (end_time<millis()){break;}}

      if(digitalRead(I_R)==LOW){
        Serial.println("F+-");
        digitalWrite(LED1_R, HIGH);
        digitalWrite(LED1_G, HIGH);
        digitalWrite(LED1_B, HIGH);
        delay(1000);
        digitalWrite(LED1_R,LOW);
        digitalWrite(LED1_G,LOW);
        digitalWrite(LED1_B,LOW);
      }
      if(digitalRead(I_Y)==LOW){
        Serial.println("H2+");
        digitalWrite(LED2_R, HIGH);
        digitalWrite(LED2_G, HIGH);
        digitalWrite(LED2_B, HIGH);
        delay(1000);
        digitalWrite(LED2_R,LOW);
        digitalWrite(LED2_G,LOW);
        digitalWrite(LED2_B,LOW);
      }
      if(digitalRead(I_B)==LOW){
        Serial.println("F+-");
        digitalWrite(LED3_R, HIGH);
        digitalWrite(LED3_G, HIGH);
        digitalWrite(LED3_B, HIGH);
        delay(1000);
        digitalWrite(LED3_R,LOW);
        digitalWrite(LED3_G,LOW);
        digitalWrite(LED3_B,LOW);
      }
      if(digitalRead(I_G)==LOW){
        Serial.println("F+-");
        digitalWrite(LED4_R, HIGH);
        digitalWrite(LED4_G, HIGH);
        digitalWrite(LED4_B, HIGH);
        delay(1000);
        digitalWrite(LED4_R,LOW);
        digitalWrite(LED4_G,LOW);
        digitalWrite(LED4_B,LOW);
      }
      if(millis()>end_time){
        Serial.println("F+-");
        digitalWrite(LED2_R,HIGH);
        digitalWrite(LED2_G,HIGH);
        digitalWrite(LED2_B,HIGH);
        delay(1000);
        digitalWrite(LED2_R,LOW);
        digitalWrite(LED2_G,LOW);
        digitalWrite(LED2_B,LOW);
      }
    }
    if (inByte == 'c') {
      digitalWrite(LED3_G, HIGH);  
      digitalWrite(LED3_R, HIGH);  
      digitalWrite(LED3_B, HIGH);  

      digitalWrite(LED2_R, HIGH);  
      digitalWrite(LED2_G, HIGH);  
      digitalWrite(LED2_B, HIGH);  

      digitalWrite(LED4_R, HIGH);  
      digitalWrite(LED4_G, HIGH);  
      digitalWrite(LED4_B, HIGH);  

      digitalWrite(LED1_R, HIGH); 
      digitalWrite(LED1_G, HIGH); 
      digitalWrite(LED1_B, HIGH); 
      delay(FBD);
      for(int i = 0; i <= FN; i++) {
       
        digitalWrite(LED3_R, LOW);  
        digitalWrite(LED3_G, LOW);  
        digitalWrite(LED3_B, LOW);  
        delay(FBD);
        digitalWrite(LED3_R, HIGH); 
        digitalWrite(LED3_G, HIGH);
        digitalWrite(LED3_B, HIGH);
        delay(FBD);
      }
      digitalWrite(LED3_R, LOW); 
      digitalWrite(LED3_G, LOW); 
      digitalWrite(LED3_B, LOW); 

      digitalWrite(LED2_R, LOW);
      digitalWrite(LED2_G, LOW);
      digitalWrite(LED2_B, LOW);

      digitalWrite(LED4_R, LOW);  
      digitalWrite(LED4_G, LOW);  
      digitalWrite(LED4_B, LOW);  

      digitalWrite(LED1_R, LOW);
      digitalWrite(LED1_G, LOW);
      digitalWrite(LED1_B, LOW);
      delay (100);

      long start_time = millis();
      long end_time = start_time + FD;

      while ((digitalRead(I_R) == HIGH)&&(digitalRead(I_Y) == HIGH)&&(digitalRead(I_B) == HIGH)&&(digitalRead(I_G) == HIGH)){if (end_time<millis()){break;}}

      if(digitalRead(I_R)==LOW){
        Serial.println("F+-");
        digitalWrite(LED1_R, HIGH);
        digitalWrite(LED1_G, HIGH);
        digitalWrite(LED1_B, HIGH);
        delay(1000);
        digitalWrite(LED1_R,LOW);
        digitalWrite(LED1_G,LOW);
        digitalWrite(LED1_B,LOW);
      }
      if(digitalRead(I_Y)==LOW){
        Serial.println("F+-");
        digitalWrite(LED2_R, HIGH);
        digitalWrite(LED2_G, HIGH);
        digitalWrite(LED2_B, HIGH);
        delay(1000);
        digitalWrite(LED2_R,LOW);
        digitalWrite(LED2_G,LOW);
        digitalWrite(LED2_B,LOW);
      }
      if(digitalRead(I_B)==LOW){
        Serial.println("H3+");
        digitalWrite(LED3_R, HIGH);
        digitalWrite(LED3_G, HIGH);
        digitalWrite(LED3_B, HIGH);
        delay(1000);
        digitalWrite(LED3_R,LOW);
        digitalWrite(LED3_G,LOW);
        digitalWrite(LED3_B,LOW);
      }
      if(digitalRead(I_G)==LOW){
        Serial.println("F+-");
        digitalWrite(LED4_R, HIGH);
        digitalWrite(LED4_G, HIGH);
        digitalWrite(LED4_B, HIGH);
        delay(1000);
        digitalWrite(LED4_R,LOW);
        digitalWrite(LED4_G,LOW);
        digitalWrite(LED4_B,LOW);
      }
      if(millis()>end_time){
        Serial.println("F+-");
        digitalWrite(LED3_R,HIGH);
        digitalWrite(LED3_G,HIGH);
        digitalWrite(LED3_B,HIGH);
        delay(1000);
        digitalWrite(LED3_R,LOW);
        digitalWrite(LED3_G,LOW);
        digitalWrite(LED3_B,LOW);
      }
    }
    if (inByte == 'd') {
      digitalWrite(LED3_R, HIGH);  
      digitalWrite(LED3_G, HIGH);  
      digitalWrite(LED3_B, HIGH);  

      digitalWrite(LED2_R, HIGH); 
      digitalWrite(LED2_G, HIGH); 
      digitalWrite(LED2_B, HIGH); 

      digitalWrite(LED4_R, HIGH); 
      digitalWrite(LED4_G, HIGH); 
      digitalWrite(LED4_B, HIGH); 

      digitalWrite(LED1_R, HIGH); 
      digitalWrite(LED1_G, HIGH); 
      digitalWrite(LED1_B, HIGH); 
      delay(FBD);
      for(int i = 0; i <= FN; i++) {
        
        digitalWrite(LED4_R, LOW);
        digitalWrite(LED4_B, LOW); 
        digitalWrite(LED4_G, LOW);   
        delay(FBD);
        digitalWrite(LED4_R, HIGH);
        digitalWrite(LED4_G, HIGH);  
        digitalWrite(LED4_B, HIGH);  
        delay(FBD);
      }
      digitalWrite(LED3_R, LOW); 
      digitalWrite(LED3_G, LOW); 
      digitalWrite(LED3_B, LOW); 

      digitalWrite(LED2_R, LOW); 
      digitalWrite(LED2_G, LOW); 
      digitalWrite(LED2_B, LOW); 

      digitalWrite(LED4_R, LOW);  
      digitalWrite(LED4_G, LOW);  
      digitalWrite(LED4_B, LOW);  

      digitalWrite(LED1_R, LOW);  
      digitalWrite(LED1_G, LOW);  
      digitalWrite(LED1_B, LOW);  
      
      delay (100);

      long start_time = millis();
      long end_time = start_time + FD;

      while ((digitalRead(I_R) == HIGH)&&(digitalRead(I_Y) == HIGH)&&(digitalRead(I_B) == HIGH)&&(digitalRead(I_G) == HIGH)){if (end_time<millis()){break;}}

      if(digitalRead(I_R)==LOW){
        Serial.println("F+-");
        digitalWrite(LED1_R, HIGH);
        digitalWrite(LED1_G, HIGH);
        digitalWrite(LED1_B, HIGH);
        delay(1000);
        digitalWrite(LED1_R,LOW);
        digitalWrite(LED1_G,LOW);
        digitalWrite(LED1_B,LOW);
      }
      if(digitalRead(I_Y)==LOW){
        Serial.println("F+-");
        digitalWrite(LED2_R, HIGH);
        digitalWrite(LED2_G, HIGH);
        digitalWrite(LED2_B, HIGH);
        delay(1000);
        digitalWrite(LED2_R,LOW);
        digitalWrite(LED2_G,LOW);
        digitalWrite(LED2_B,LOW);
      }
      if(digitalRead(I_B)==LOW){
        Serial.println("F+-");
        digitalWrite(LED3_R, HIGH);
        digitalWrite(LED3_G, HIGH);
        digitalWrite(LED3_B, HIGH);
        delay(1000);
        digitalWrite(LED3_R,LOW);
        digitalWrite(LED3_G,LOW);
        digitalWrite(LED3_B,LOW);
      }
      if(digitalRead(I_G)==LOW){
        Serial.println("H4+");
        digitalWrite(LED4_R, HIGH);
        digitalWrite(LED4_G, HIGH);
        digitalWrite(LED4_B, HIGH);
        delay(1000);
        digitalWrite(LED4_R,LOW);
        digitalWrite(LED4_G,LOW);
        digitalWrite(LED4_B,LOW);
      }
      if(millis()>end_time){
        Serial.println("F+-");
        digitalWrite(LED4_R,HIGH);
        digitalWrite(LED4_G,HIGH);
        digitalWrite(LED4_B,HIGH);
        delay(1000);
        digitalWrite(LED4_R,LOW);
        digitalWrite(LED4_G,LOW);
        digitalWrite(LED4_B,LOW);
      }
    }


    if (inByte == 'e') {
      while(!Serial.available()){}
      
      int nextByte = Serial.read();
      
      if (nextByte == 10 || nextByte == 13) {
        while(!Serial.available()){}
        nextByte = Serial.read();
      }
      
      if (nextByte >= '0' && nextByte <= '9') {
        FN = nextByte - '0';
      }
      
      Serial.print("FN set to: ");
      Serial.println(FN);
    }
   if (inByte == 'f') {
      while(!Serial.available()){}
      
      int nextByte = Serial.read();
      
      if (nextByte == 10 || nextByte == 13) {
        while(!Serial.available()){}
        nextByte = Serial.read();
      }
      
      if (nextByte >= '0' && nextByte <= '9') {
        FDL = nextByte - '0';
        FD = 30000 - 20000/9*FDL;
      }
      
      Serial.print("FDL set to: ");
      Serial.println(FDL);
    }
    if (inByte == 'g') {
      while(!Serial.available()){}
      
      int nextByte = Serial.read();
      
      if (nextByte == 10 || nextByte == 13) {
        while(!Serial.available()){}
        nextByte = Serial.read();
      }
      
      if (nextByte >= '0' && nextByte <= '9') {
        ODL = nextByte - '0';
        OD = 2000 - 500/3*ODL;
      }
      
      Serial.print("ODL set to: ");
      Serial.println(ODL);
    }
      if (inByte == 'm') {
      while (!Serial.available()) {}

      int nextByte = Serial.read();

      if (nextByte == 10 || nextByte == 13) {
        while (!Serial.available()) {}
        w = Serial.read() - '0';
      } else {
        w = nextByte - '0';
      }


      while (!Serial.available()) {}

      nextByte = Serial.read();

      if (nextByte == 10 || nextByte == 13) {
        while (!Serial.available()) {}
        x = Serial.read() - '0';
      } else {
        x = nextByte - '0';
      }


      while (!Serial.available()) {}

      nextByte = Serial.read();

      if (nextByte == 10 || nextByte == 13) {
        while (!Serial.available()) {}
        y = Serial.read() - '0';
      } else {
        y = nextByte - '0';
      }


      while (!Serial.available()) {}

      nextByte = Serial.read();

      if (nextByte == 10 || nextByte == 13) {
        while (!Serial.available()) {}
        z = Serial.read() - '0';
      } else {
        z = nextByte - '0';
      }


      digitalWrite(LED1_R, HIGH);
      digitalWrite(LED1_G, HIGH);
      digitalWrite(LED1_B, HIGH);

      digitalWrite(LED2_R, HIGH);
      digitalWrite(LED2_G, HIGH);
      digitalWrite(LED2_B, HIGH);

      digitalWrite(LED4_R, HIGH);
      digitalWrite(LED4_G, HIGH);
      digitalWrite(LED4_B, HIGH);

      digitalWrite(LED3_R, HIGH);
      digitalWrite(LED3_G, HIGH);
      digitalWrite(LED3_B, HIGH);

      while (((hoop_w == 0) || (hoop_x == 0)) && ((hoop_y == 0) || (hoop_z == 0))) {
        while ((digitalRead(I_R) == HIGH) && (digitalRead(I_Y) == HIGH) &&
               (digitalRead(I_B) == HIGH) && (digitalRead(I_G) == HIGH)) {}

        if (digitalRead(I_R) == LOW) {
          if (w == 1) {
            hoop_w = 1;
            digitalWrite(LED1_R, LOW);
            digitalWrite(LED1_G, LOW);
            digitalWrite(LED1_B, LOW);
          }
          if (x == 1) {
            hoop_x = 1;
            digitalWrite(LED1_R, LOW);
            digitalWrite(LED1_G, LOW);
            digitalWrite(LED1_B, LOW);
          }
          if (y == 1) {
            hoop_y = 1;
            digitalWrite(LED1_R, LOW);
            digitalWrite(LED1_G, LOW);
            digitalWrite(LED1_B, LOW);
          }
          if (z == 1) {
            hoop_z = 1;
            digitalWrite(LED1_R, LOW);
            digitalWrite(LED1_G, LOW);
            digitalWrite(LED1_B, LOW);
          }
        }

        if (digitalRead(I_Y) == LOW) {
          if (w == 2) {
            hoop_w = 1;
            digitalWrite(LED2_R, LOW);
            digitalWrite(LED2_G, LOW);
            digitalWrite(LED2_B, LOW);
          }
          if (x == 2) {
            hoop_x = 1;
            digitalWrite(LED2_R, LOW);
            digitalWrite(LED2_G, LOW);
            digitalWrite(LED2_B, LOW);
          }
          if (y == 2) {
            hoop_y = 1;
            digitalWrite(LED2_R, LOW);
            digitalWrite(LED2_G, LOW);
            digitalWrite(LED2_B, LOW);
          }
          if (z == 2) {
            hoop_z = 1;
            digitalWrite(LED2_R, LOW);
            digitalWrite(LED2_G, LOW);
            digitalWrite(LED2_B, LOW);
          }
        }

        if (digitalRead(I_B) == LOW) {  
          if (w == 3) {
            hoop_w = 1;
            digitalWrite(LED4_R, LOW);
            digitalWrite(LED4_G, LOW);
            digitalWrite(LED4_B, LOW);
          }
          if (x == 3) {
            hoop_x = 1;
            digitalWrite(LED4_R, LOW);
            digitalWrite(LED4_G, LOW);
            digitalWrite(LED4_B, LOW);
          }
          if (y == 3) {
            hoop_y = 1;
            digitalWrite(LED4_R, LOW);
            digitalWrite(LED4_G, LOW);
            digitalWrite(LED4_B, LOW);
          }
          if (z == 3) {
            hoop_z = 1;
            digitalWrite(LED4_R, LOW);
            digitalWrite(LED4_G, LOW);
            digitalWrite(LED4_B, LOW);
          }
        }

        if (digitalRead(I_G) == LOW) { 
          if (w == 4) {
            hoop_w = 1;
            digitalWrite(LED3_R, LOW);
            digitalWrite(LED3_G, LOW);
            digitalWrite(LED3_B, LOW);
          }
          if (x == 4) {
            hoop_x = 1;
            digitalWrite(LED3_R, LOW);
            digitalWrite(LED3_G, LOW);
            digitalWrite(LED3_B, LOW);
          }
          if (y == 4) {
            hoop_y = 1;
            digitalWrite(LED3_R, LOW);
            digitalWrite(LED3_G, LOW);
            digitalWrite(LED3_B, LOW);
          }
          if (z == 4) {
            hoop_z = 1;
            digitalWrite(LED3_R, LOW);
            digitalWrite(LED3_G, LOW);
            digitalWrite(LED3_B, LOW);
          }
        }

        if ((hoop_w == 1) && (hoop_x == 1)) {
          answer = "R";
          answer += hoop_w;
          answer += hoop_x;
          answer += hoop_y;
          answer += hoop_z;
          Serial.print(answer);
          hoop_w = 0;
          hoop_x = 0;
          hoop_y = 0;
          hoop_z = 0;
          digitalWrite(LED1_R, LOW);
          digitalWrite(LED1_G, LOW);
          digitalWrite(LED1_B, LOW);

          digitalWrite(LED2_R, LOW);
          digitalWrite(LED2_G, LOW);
          digitalWrite(LED2_B, LOW);

          digitalWrite(LED3_R, LOW);
          digitalWrite(LED3_G, LOW);
          digitalWrite(LED3_B, LOW);
          digitalWrite(LED4_R, LOW);
          digitalWrite(LED4_G, LOW);
          digitalWrite(LED4_B, LOW);
          break;
        }
        if ((hoop_y == 1) && (hoop_z == 1)) {
          answer = "B";
          answer += hoop_w;
          answer += hoop_x;
          answer += hoop_y;
          answer += hoop_z;
          Serial.print(answer);
          hoop_w = 0;
          hoop_x = 0;
          hoop_y = 0;
          hoop_z = 0;
          digitalWrite(LED1_R, LOW);
          digitalWrite(LED1_G, LOW);
          digitalWrite(LED1_B, LOW);

          digitalWrite(LED2_R, LOW);
          digitalWrite(LED2_G, LOW);
          digitalWrite(LED2_B, LOW);
          
          digitalWrite(LED3_R, LOW);
          digitalWrite(LED3_G, LOW);
          digitalWrite(LED3_B, LOW);

          digitalWrite(LED4_R, LOW);
          digitalWrite(LED4_G, LOW);
          digitalWrite(LED4_B, LOW);
          break;
        }
      }
    }
  }
}