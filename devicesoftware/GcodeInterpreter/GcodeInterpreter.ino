/*******************************************************************************
Titre : OpenCR
Date : 6 février 2019
Auteur : Maxime Desmarais-Laporte
Descritpion : 

Specifications :
Baud for motors : 57600 b/s
Adress for motors : 11 and 12 and 13
*******************************************************************************/
#include <DynamixelWorkbench.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3"
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define STRING_BUF_NUM 64
#define MINTICK 0
#define MAXTICK 1048575

// 0 = not reverse, 1 = reverse
uint8_t X_REVERSE = 0;
uint8_t Y_REVERSE = 1;
uint8_t Z_REVERSE = 0;

const String HOMING_OFFSET = "Homing_Offset";
const String OPERATING_MODE = "Operating_Mode";
const String PRESENT_POSITION = "Present_Position";
const String GOAL_POSITION = "Goal_Position";

String cmd[STRING_BUF_NUM];

DynamixelWorkbench dxl_wb;
uint8_t get_id[16];
uint8_t scan_cnt = 0;
uint8_t ping_cnt = 0;

const char *NULL_POINTER = NULL;

bool isEmegencyState = false;

// Motors Propertys :
uint8_t idX = 11;
uint8_t idY = 12;
uint8_t idZ = 13;

// Mecanicals propertys:
const float pouleyPitch = 2;  //mm
const int nbTheets = 20;
const int resMotorTick = 4096;  //Ticks per revolution

int32_t tickFromMm = resMotorTick/(pouleyPitch*nbTheets);

// Limit Switch propertys
const int xSwitchPin = 8;
const int ySwitchPin = 9;
const int zSwitchPin = 10;
const int emergencySwitchPin = 2; // intrupt pin

// Homing variables
bool homing = false;

const int homeOffsetX = 10*tickFromMm;
const int homeOffsetY = 10*tickFromMm;
const int homeOffsetZ = 10*tickFromMm;

// Fonctions prototypes : 
void Begin(uint32_t baud);
void Ping(int identification);
void Scan();
void Joint(uint8_t id, uint16_t goal);
void Wheel(uint8_t id, int32_t goal);
void Torque_on(uint8_t id);
void Torque_off(uint8_t id);
void Write(uint8_t id, uint32_t value, String commande);
int32_t Read(uint8_t id, String commande);
void Led(uint8_t id, bool state);
void TorqueOffAll();
void OffsetAxe(uint8_t id, int offset);
void LimiteSwitch();
int MovingTick(uint8_t id, int32_t value);
int Homing();
int HomingAxis(uint8_t id, int speed, int switchPin, int offset);
uint8_t getIdFromChar(char letter);

// Initialisation :
void setup() 
{

  // Initialisation des pins :
  pinMode(xSwitchPin, INPUT_PULLUP);
  pinMode(ySwitchPin, INPUT_PULLUP);
  pinMode(zSwitchPin, INPUT_PULLUP);
  pinMode(emergencySwitchPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(emergencySwitchPin), LimiteSwitch, FALLING);
  
  Serial.begin(57600);
  while(!Serial); // Open a Serial Monitor  

    //Motor Initialisation Section :
  Begin((uint32_t)57600);
  Ping(idX);
  Ping(idY);
  Ping(idZ);
  Scan();
  
  delay(1000);
  
  Torque_off(idX);
  Torque_off(idY);
  Torque_off(idZ);
  
  Write(idX, 4, OPERATING_MODE);
  Write(idY, 4, OPERATING_MODE);
  Write(idZ, 4, OPERATING_MODE);

  Write(idX, 0, HOMING_OFFSET);
  Write(idY, 0, HOMING_OFFSET);
  Write(idZ, 0, HOMING_OFFSET);

  dxl_wb.writeRegister(idX, 10, 1, &  , &NULL_POINTER);
  dxl_wb.writeRegister(idY, 10, 1, &Y_REVERSE, &NULL_POINTER);
  dxl_wb.writeRegister(idZ, 10, 1, &Z_REVERSE, &NULL_POINTER);

  Torque_on(idX);
  Torque_on(idY);
  Torque_on(idZ);
}

// Main Program
void loop() 
{
  if(isEmegencyState)
    setEmergency();
  
  if (Serial.available())
  {
    String read_string = Serial.readStringUntil('\n');
    if(!isEmegencyState)
    {
      String words[] = {"", "", ""};
      
      int start = 0;
      int wordIndex = 0;
      int statut[3] = {0, 0, 0};
      
      for(int i = 1; i < read_string.length(); i++)
      {
        if(read_string.charAt(i) == ' ')
        {
          words[wordIndex++] = read_string.substring(start, i);
          start = i+1;
        }
      }
      words[wordIndex] = read_string.substring(start, read_string.length());
      
      Serial.println("2"); 

      if(words[0] == "G0")
      {
          for(int i = 1; i < wordIndex+1; i++)
          {
              if(words[i].length() > 1)
              {
                  float value = words[i].substring(1, words[i].length()).toFloat();
                  uint8_t idMotor = getIdFromChar((char)words[i].charAt(0));
                  if(idMotor == -1)
                      Serial.println("-1");
                  else
                      statut[i] = MovingTick(idMotor, value*tickFromMm);
              }
              else
                  Serial.println("-1");
          }
          if((statut[0] == 1 || statut[0] == 0) && (statut[1] == 1 || statut[1] == 0) && (statut[2] == 1|| statut[2] == 0)){
              Serial.println("1");
          }
          else{
              Serial.println("-1");
          }
      }
      
      else if(words[0] == "G28"){
        Serial.println(Homing());
      }
      else if(words[0] == "M18"){
          TorqueOffAll();
          Serial.println("1");
      }
      else if(words[0] == "M112"){
          setEmergency();

          Led(idX, 1);
          Led(idY, 1);
          Led(idZ, 1);

          Serial.println("1");
      }
      else if(words[0] == "M1")
      {
        TorqueOffAll();
        
        Write(idX, -Read(idX, PRESENT_POSITION), HOMING_OFFSET);
        Write(idY, -Read(idY, PRESENT_POSITION), HOMING_OFFSET);
        Write(idZ, -Read(idZ, PRESENT_POSITION), HOMING_OFFSET);
        
        TorqueOnAll();
        Serial.println("1");
      }
      else
      { 
        Serial.println("-1");
      }
    }
    else
    {
      Serial.println("-2");
    }
  }
}

uint8_t getIdFromChar(char letter)
{
    if(letter == 'X')
        return idX;
    else if(letter == 'Y')
        return idY;
    else if(letter == 'Z')
        return idZ;
    else
        return -1;
}

int Homing()
{
  int state = 0;
  homing = true;
  
  //state += HomingAxis(idZ, -50, zSwitchPin, homeOffsetZ);
  state += HomingAxis(idY, -100, ySwitchPin, homeOffsetY);
  state += HomingAxis(idX, -100, xSwitchPin, homeOffsetX);
  
  homing = false;
  return state == 2 ? 1 : -1;
}

int HomingAxis(uint8_t id, int speed, int switchPin, int offset)
{
  Torque_off(id);
  Write(id, 0, HOMING_OFFSET);
  Torque_on(id);
  Wheel(id, speed);
  while(!digitalRead(switchPin));
  OffsetAxe(id, offset);
  Write(id, 4, OPERATING_MODE);
  return MovingTick(id, 0);
}

void OffsetAxe(uint8_t id, int offset){
  int32_t posPresent = Read(id, PRESENT_POSITION);
  int32_t homePosition = - posPresent - offset;
  Torque_off(id); 

  if(id == idX && X_REVERSE)
    homePosition *= -1;
  else if(id == idY && Y_REVERSE)
    homePosition *= -1;
  else if(id == idZ && Z_REVERSE)
    homePosition *= -1;
  
  Write(id, homePosition, HOMING_OFFSET);
}

int MovingTick(uint8_t id, int32_t value){
  int32_t CurrentPosition = Read(id, PRESENT_POSITION);
  bool Forward = value > CurrentPosition;
  
  if((Forward && (CurrentPosition < MAXTICK)) || (!Forward && (CurrentPosition > MINTICK)))
  {
    Torque_on(id);
    Write(id, value, GOAL_POSITION); 
  }
  else
  {
    Torque_off(id); 
    return -1;
  }
  
  if(Forward){
    while(CurrentPosition < value-1  && !isEmegencyState){
      CurrentPosition = Read(id, PRESENT_POSITION);
      if(CurrentPosition >= MAXTICK && !homing){
        Torque_off(id);
        return -1;
      }
    }
  }
  else {
    while(CurrentPosition > value+1 && !isEmegencyState){
      CurrentPosition = Read(id, PRESENT_POSITION);
      if(CurrentPosition <= MINTICK && !homing){
        Torque_off(id);
        return -1;
      }
    }
  }

  return 1;
}

void LimiteSwitch(){
  if(!homing){
    isEmegencyState = true;
  }
}

void setEmergency()
{
  TorqueOffAll();
  Led(idX, !digitalRead(xSwitchPin));
  Led(idY, !digitalRead(ySwitchPin)); 
  Led(idZ, !digitalRead(zSwitchPin)); 
}


//########################
// Low Levels functions :
//########################

void Begin(uint32_t baud){
  if (cmd[1] == '\0')
  cmd[1] = String("57600");
  
  dxl_wb.init(DEVICE_NAME, baud);
}

void Ping(int identification){
  get_id[ping_cnt] = identification;
  uint16_t model_number = 0;
  dxl_wb.ping(get_id[ping_cnt], &model_number, &NULL_POINTER); 
}

void Scan(){
  uint8_t range = 253;
  dxl_wb.scan(get_id, &scan_cnt, range);  
}

void Joint(uint8_t id, int32_t goal){
  dxl_wb.jointMode(id, 0, 0, &NULL_POINTER);
  dxl_wb.goalPosition(id, goal, &NULL_POINTER);
}

void Wheel(uint8_t id, int32_t goal){
  dxl_wb.wheelMode(id, 0, &NULL_POINTER);
  dxl_wb.goalVelocity(id, goal, &NULL_POINTER);
}

void Torque_on(uint8_t id){
  dxl_wb.torqueOn(id, &NULL_POINTER);
}

void Torque_off(uint8_t id){
  dxl_wb.torqueOff(id, &NULL_POINTER);
}

void Write(uint8_t id, uint32_t value, String commande){
  dxl_wb.writeRegister(id, commande.c_str(), value, &NULL_POINTER);
}

int32_t Read(uint8_t id, String commande){
  int32_t data = 0;
  dxl_wb.readRegister(id, commande.c_str(), &data, &NULL_POINTER);
  return data;
}

void Led(uint8_t id, bool state){
  Write(id, (uint32_t)state, "LED");
}

void TorqueOffAll(){
      Torque_off(idX);
      Torque_off(idY);
      Torque_off(idZ);
}

void TorqueOnAll(){
      Torque_on(idX);
      Torque_on(idY);
      Torque_on(idZ);
}
