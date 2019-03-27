/*******************************************************************************
Titre : OpenCR
Date : 6 février 2019
Auteur : Maxime Desmarais-Laporte
Descritpion : 

Specifications :
Baud for motors : 57600 b/s
Adress for motors : 11 and 12

List of function creation :

                              Functions                       |Function State / test / Implementation / test
  help                                                        |
  begin  (BAUD)                                               |Done / yes
  scan   (RANGE)                                              |Done / yes
  ping   (ID)                                                 |Done / yes
  control_table (ID)                                          |
  id     (ID) (NEW_ID)                                        |
  baud   (ID) (NEW_BAUD)                                      |
  torque_on (ID)                                              |
  torque_off (ID)                                             |
  joint  (ID) (GOAL_POSITION)                                 |
  wheel  (ID) (GOAL_VELOCITY)                                 |Done / yes
  write  (ID) (ADDRESS_NAME) (DATA)                           |
  read   (ID) (ADDRESS_NAME)                                  |
  sync_write_handler (Ref_ID) (ADDRESS_NAME)                  |
  sync_write (ID_1) (ID_2) (HANDLER_INDEX) (PARAM_1) (PARAM_2)|
  sync_read_handler (Ref_ID) (ADDRESS_NAME)                   |
  sync_read (ID_1) (ID_2) (HANDLER_INDEX)                     |
  bulk_write_handler                                          |
  bulk_write_param (ID) (ADDRESS_NAME) (PARAM)                |
  bulk_write                                                  |
  bulk_read_handler                                           |
  bulk_read_param (ID) (ADDRESS_NAME)                         |
  bulk_read                                                   |
  reboot (ID)                                                 |
  reset  (ID)                                                 |
  end                                                         |
  
*******************************************************************************/

#include <DynamixelWorkbench.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define STRING_BUF_NUM 64
String cmd[STRING_BUF_NUM];

DynamixelWorkbench dxl_wb;
uint8_t get_id[16];
uint8_t scan_cnt = 0;
uint8_t ping_cnt = 0;

const char *NULL_POINTER = NULL;

// Motors Propertys :
uint8_t idX = 11;
uint8_t idY = 12;
uint8_t idZ = 13;

// Mecanicals propertys:
float pouleyPitch = 2;  //mm
float nbTheets = 20;
int resMotorTick = 4096;  //Ticks per revolution

// Limit Switch propertys
int xSwitchPin = 8;
int ySwitchPin = 9;
int zSwitchPin = 10;
int emergencySwitchPin = 2; // intrupt pin

// Homing variables
bool homing = 0;
bool homingX = 0;
bool homingY = 0;
bool homingZ = 0;

int offsetX = 10; //mm
int offsetY = 10; //mm
int offsetZ = 10; //mm

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
void EmergencyStop();
void HomeAxe(uint8_t id, int offset);
void LimiteSwitch();

int mmToTick(float value_mm, float pouleyPitch, float nbTheets, int resMotorTick);
int MovingTick(uint8_t id, int32_t value);
int MovingDistance(float value_mm, uint8_t id);
int Homing();

// Initialisation :
void setup() 
{

  // Initialisation des pins :
  pinMode(xSwitchPin, INPUT_PULLUP);
  pinMode(ySwitchPin, INPUT_PULLUP);
  pinMode(zSwitchPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(emergencySwitchPin), LimiteSwitch, RISING);
  
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
  
  Write(idX, (uint32_t)4,"Operating_Mode");
  Write(idY, (uint32_t)4,"Operating_Mode");
  Write(idZ, (uint32_t)4,"Operating_Mode");

  Torque_on(idX);
  Torque_on(idY);
  Torque_on(idZ);
}

// Main Program
void loop() {

if (Serial.available())
  {
    String read_string = Serial.readStringUntil('\n');
    //Serial.println("[CMD] : " + String(read_string));

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

    // Absolute Move G0
    // Call exemple : G0 X100 Y200 Z10
    if(words[0] == "G0")
    {
      Serial.println("2");
      for(int i = 1; i < wordIndex+1; i++)
      {
        float value = words[i].substring(1, words[i].length()).toFloat();

        switch ((char)words[i].charAt(0)){

          case 'X' :
            statut[i] = MovingDistance(value, idX);
          break;

          case 'Y' :
            statut[i] = MovingDistance(value, idY);
          break;

          case 'Z' :
            statut[i] = MovingDistance(value, idZ);
          break;

          default :
          Serial.println("-1");
          break;
        }
        
        
      }
      if((statut[0] == 1 || statut[0] == 0) && (statut[1] == 1 || statut[1] == 0) && (statut[2] == 1|| statut[2] == 0)){
        Serial.println("1");
      }
      else{
        Serial.println("-1");
      }
    }

    // Homing G28 (home all axes)
    // Call exemple : G28
    else if(words[0] == "G28"){
      Serial.println("2");
      Serial.println(Homing());
    }

    // Torque OFF all M18
    // Call exemple : M18
    else if(words[0] == "M18"){
      Serial.println("2");
      EmergencyStop();
      Serial.println("1");
    }
    
    // Emergency state M112
    // Call exemple : M112
    else if(words[0] == "M112"){
      Serial.println("2");
      EmergencyStop();

      for(int i=0; i<10; i++){
        Led(idX, 1);
        Led(idY, 1);
        Led(idZ, 1);
        delay(200);
        Led(idX, 0);
        Led(idY, 0);
        Led(idZ, 0);
        delay(200);
      }
      Serial.println("1");
    }

    // Request not recognized
    else{
      Serial.println("-1");
    }
  }
}

//---------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Functions :
//---------------------------------------------------------------------------------------------------------------------------------------------------------------------

//---------------------------------------------------------------------------------------------------------------------------------------------------------------------
// Functions of Robotics Engeneering UdeS :
//---------------------------------------------------------------------------------------------------------------------------------------------------------------------

//########################
// High level Functions :
//########################

int Homing(){
  homing = 1;
  // home Z :
  homingZ = true;
  homingY = false;
  homingX = false;
  Torque_on(idZ);
  Wheel(idZ, -50);
  
  // home y :
  homingZ = false;
  homingY = true;
  homingX = false;
  Torque_on(idY);
  Wheel(idY, -100);
  
  // home x :
  homingZ = false;
  homingY = false;
  homingX = true;
  Torque_on(idX);
  Wheel(idX, -100);

  return 1;
}

int MovingDistance(float value_mm, uint8_t id){
  return MovingTick(id, mmToTick(value_mm, pouleyPitch, nbTheets, resMotorTick));
}

int mmToTick(float value_mm, float pouleyPitch, float nbTheets, int resMotorTick){
  int32_t value = ((value_mm/(pouleyPitch*nbTheets))/resMotorTick);
  return value;
}

int MovingTick(uint8_t id, int32_t value){
  String commande = "Goal_Position";
  int32_t CurrentPosition = Read(id, "Present_Position");
  int MaxTick = 1048575;
  int MinTick = 0;

  bool Front_Back = 0;
  
  if(value > Read(id, "Present_Position")){
    Front_Back = 1;
  }
  else if(value < Read(id, "Present_Position")){
    Front_Back = 0;
  }

  if((Front_Back && (CurrentPosition < MaxTick)) || (!Front_Back && (CurrentPosition > MinTick)))
  {
    Torque_on(id);
    Write(id, value, commande); 
  }
  else
  {
    Torque_off(id); 
    Serial.println(CurrentPosition);
    return -1;
  }

  // Moving to front request
  if(Front_Back){
    while(CurrentPosition < value-1){
      CurrentPosition = Read(id, "Present_Position");
      if(CurrentPosition >= MaxTick){
        Torque_off(id);
        return -1;
      }
    }
  }

  // Moving to back request
  else {
    while(CurrentPosition > value+1){
      CurrentPosition = Read(id, "Present_Position");
      if(CurrentPosition <= MinTick){
        Torque_off(id);
        return -1;
      }
    }
  }

  return 1;
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

void EmergencyStop(){
      Torque_off(idX);
      Torque_off(idY);
      Torque_off(idZ);
      Serial.println(-1);
}

void HomeAxe(uint8_t id, int offset){
  Torque_off(id);
  Torque_on(id);
  MovingDistance(offset, id);
  int homingPosition = Read(id, "Present_Position");
  Write(id, (uint32_t)homingPosition, "Homing_Offset");
}

void LimiteSwitch(){
  if(homing){
    if(homingZ == HIGH && digitalRead(zSwitchPin) == HIGH){
      HomeAxe(idZ, offsetZ);
    }
    else if(homingY == HIGH && digitalRead(ySwitchPin) == HIGH){
      HomeAxe(idY, offsetY);
    }
    else if(homingX == HIGH && digitalRead(xSwitchPin) == HIGH){
      HomeAxe(idX, offsetX);
    }
  }
  else{
    EmergencyStop();
    Serial.flush();
    Serial.println("-1");
  }
}