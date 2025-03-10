String k;
#define buzzer 2
#define led1 3
#define led2 4
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(buzzer,OUTPUT);
pinMode(led1,OUTPUT);
pinMode(led2,OUTPUT);
digitalWrite(buzzer,LOW);
digitalWrite(led1,LOW);
digitalWrite(led2,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
while(Serial.available()>0)
{
  k = Serial.readStringUntil('\n');
  Serial.println(k);
  delay(1000);
  if(k=="wild")
  {
  Serial.println("Wlid");
  digitalWrite(buzzer,HIGH);
    delay(5000);
   digitalWrite(buzzer,LOW);
   digitalWrite(led1,HIGH);
   delay(5000);
   digitalWrite(led1,LOW);
//digitalWrite(led2,LOW);
digitalWrite(led2,HIGH);
   delay(5000);
digitalWrite(led2,LOW);
sendsms("Wild Animal detected");

  }
  else{
    digitalWrite(buzzer,LOW);
    digitalWrite(led1,LOW);
digitalWrite(led2,LOW);
      Serial.println("Not Matched");
  }
}

}
void sendsms(const char *message)
{
  
  Serial.println("AT\r\n");
  delay(2000);
  Serial.println("ATE0\r\n");
  delay(2000);
 Serial.println("AT+CMGF=1\r\n");
 delay(2000);
  Serial.println("AT+CMGS=\"09948490226\"");
  delay(1000);
   Serial.print(message);
  delay(1000);
  Serial.println((char)26);
 
  delay(1000);
}
