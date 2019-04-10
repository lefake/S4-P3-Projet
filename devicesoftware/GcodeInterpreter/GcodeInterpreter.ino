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
#include "functions.h"
#include "models.h"

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3"
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define STRING_BUF_NUM 64
#define MINTICK 0
#define MAXTICK 1048575
const int ACCEPTABLE_RANGE[3] = { 2, 2, 3 };

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
bool homingX = false;
bool homingY = false;
bool homingZ = false;
int homingState = 0;

const int homeOffsetX = /*28*/48*tickFromMm;
const int homeOffsetY = /*19.5*/40*tickFromMm;
const int homeOffsetZ = 2.5*tickFromMm;

// Debounce timer variables
bool isFalling = false;
long debounceTimeFalling = 250;
long lastTimeXFalling = 0;
long lastTimeYFalling = 0;
long lastTimeZFalling = 0;

bool isRising = false;
long debounceTimeRising = 250;
long lastTimeXRising = 0;
long lastTimeYRising = 0;
long lastTimeZRising = 0;

bool isXSwitchPress = false;
bool isYSwitchPress = false;
bool isZSwitchPress = false;

// Moving variables
bool isMoving = false;
bool currentMoveDone = false;
bool hasFailed = false;
int currentMove = 0;
int nbsMovements = 0;
int32_t currentPosition = 0;
MovingCommand commands[3];

// Initialisation :
void setup() 
{
  // Initialisation des pins :
  pinMode(xSwitchPin, INPUT_PULLUP);
  pinMode(ySwitchPin, INPUT_PULLUP);
  pinMode(zSwitchPin, INPUT_PULLUP);
  pinMode(emergencySwitchPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(emergencySwitchPin), LimiteSwitch, CHANGE);
  
  Serial.begin(57600);

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

  dxl_wb.writeRegister(idX, 10, 1, &X_REVERSE, &NULL_POINTER);
  dxl_wb.writeRegister(idY, 10, 1, &Y_REVERSE, &NULL_POINTER);
  dxl_wb.writeRegister(idZ, 10, 1, &Z_REVERSE, &NULL_POINTER);
  

  Torque_on(idX);
  Torque_on(idY);
  Torque_on(idZ);

  resetMovingVariables();
}

// Main Program
void loop() 
{
  if(isFalling)
  {
    if(digitalRead(xSwitchPin))
    {
      if(millis() - lastTimeXFalling > debounceTimeFalling)
      {
        lastTimeXFalling = millis();
        isFalling = false;
        isXSwitchPress = true;

        if(homingX)
        {
          homingX = false;
          OffsetAxe(idX, homeOffsetX);
          Torque_off(idX);
          Write(idX, 4, OPERATING_MODE);
          Torque_on(idX);
          
          currentMove = 0;
          nbsMovements = 1;
          commands[currentMove]._motorId = idX;
          commands[currentMove]._goalPosition = 0;
          isMoving = true;
          Write(commands[currentMove]._motorId, commands[currentMove]._goalPosition, GOAL_POSITION); 
        }
        else
          isEmegencyState = true;
      }
    }
    else
    {
      lastTimeXFalling = millis();
      isXSwitchPress = false;
    }

    if(digitalRead(ySwitchPin))
    {
      if(millis() - lastTimeYFalling > debounceTimeFalling)
      {
        lastTimeYFalling = millis();
        isFalling = false;
        isYSwitchPress = true;

        if(homingY)
        {
          homingY = false;
          OffsetAxe(idY, homeOffsetY);
          Torque_off(idY);
          Write(idY, 4, OPERATING_MODE);
          Torque_on(idY);
          
          currentMove = 0;
          nbsMovements = 1;
          commands[currentMove]._motorId = idY;
          commands[currentMove]._goalPosition = 0;
          isMoving = true;
          Write(commands[currentMove]._motorId, commands[currentMove]._goalPosition, GOAL_POSITION);
        }
        else
          isEmegencyState = true;
      }
    }
    else
    {
      lastTimeYFalling = millis();
      isYSwitchPress = false;
    }

    if(digitalRead(zSwitchPin))
    {
      if(millis() - lastTimeZFalling > debounceTimeFalling)
      {
        lastTimeZFalling = millis();
        isFalling = false;
        isZSwitchPress = true;
        
        if(homingZ)
        {
          homingZ = false;
          OffsetAxe(idZ, homeOffsetZ);
          Torque_off(idZ);
          Write(idZ, 4, OPERATING_MODE);
          Torque_on(idZ);

          currentMove = 0;
          nbsMovements = 1;
          commands[currentMove]._motorId = idZ;
          commands[currentMove]._goalPosition = 0;
          isMoving = true;          
          Write(commands[currentMove]._motorId, commands[currentMove]._goalPosition, GOAL_POSITION);
        }
        else
          isEmegencyState = true;
      }
    }
    else
    {
      lastTimeZFalling = millis();
      isZSwitchPress = false;
    }

    if(!digitalRead(xSwitchPin) && !digitalRead(ySwitchPin) && !digitalRead(zSwitchPin))
      isFalling = false;
  }

  if(isRising)
  {
    if(!digitalRead(xSwitchPin))
    {
      if(millis() - lastTimeXRising > debounceTimeRising)
      {
        lastTimeXRising = millis();
        isRising = false;
        isXSwitchPress = false;
      }
    }
    else
      lastTimeXRising = millis();

    if(!digitalRead(ySwitchPin))
    {
      if(millis() - lastTimeYRising > debounceTimeRising)
      {
        lastTimeYRising = millis();
        isRising = false;
        isYSwitchPress = false;
      }
    }
    else
      lastTimeYRising = millis();

    if(!digitalRead(zSwitchPin))
    {
      if(millis() - lastTimeZRising > debounceTimeRising)
      {
        lastTimeZRising = millis();
        isRising = false;
        isZSwitchPress = false;
      }
    }
    else
      lastTimeZRising = millis();

    if(digitalRead(xSwitchPin) && digitalRead(ySwitchPin) && digitalRead(zSwitchPin))
    {
      isRising = false;
    }
  }

  if(isMoving)
  {
    currentPosition = Read(commands[currentMove]._motorId, PRESENT_POSITION);
    if(isInRange(currentPosition, commands[currentMove]._goalPosition, commands[currentMove]._motorId))
    {
      currentMoveDone = true;
    }
  }

  if(isMoving && currentMoveDone)
  {
    if(currentMove+1 >= nbsMovements)
    {
      if(homing)
      {
        if(commands[currentMove]._motorId == idZ)
        {
          homingY = true;
          HomingAxis(idY, -100);
          homingState++;
        }
        else if(commands[currentMove]._motorId == idY)
        {
          homingX = true;
          HomingAxis(idX, -100);
          homingState++;
        }
        else if(commands[currentMove]._motorId == idX)
        {
          homingState++;
          homing = false;
          Serial.println(homingState == 3 ? "1" : "-1");
          homingState = 0;
        }
        resetMovingVariables();
      }
      else
      {
        resetMovingVariables();
        Serial.println("1");
      }
    }
    else
    {
      currentMoveDone = false;
      currentMove++;
      Write(commands[currentMove]._motorId, commands[currentMove]._goalPosition, GOAL_POSITION);
    }
  }
  
  if(isEmegencyState)
    setEmergency();
  
  if (!homing && !isMoving && Serial.available())
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
      nbsMovements = wordIndex;
      Serial.println("2");

      if(words[0] == "G0")
      {
        int i;
        for(i = 1; i < wordIndex+1; i++)
        {
            if(words[i].length() > 1)
            {
                float value = words[i].substring(1, words[i].length()).toFloat();
                uint8_t idMotor = getIdFromChar((char)words[i].charAt(0));
                if(idMotor == -1)
                {
                  Serial.println("-1");
                  break;
                }
                else
                {
                  commands[i-1]._motorId = idMotor;
                  commands[i-1]._goalPosition = value*tickFromMm;
                }
            }
            else
            {
              Serial.println("-1");
              break;
            }
        }
        
        if(i == wordIndex+1)
        {
          isMoving = true;
          currentMove = 0;
          Write(commands[currentMove]._motorId, commands[currentMove]._goalPosition, GOAL_POSITION);
        }
      }
      
      else if(words[0] == "G28")
      {
        homing = true;
        homingZ = true;
        HomingAxis(idZ, -50);
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
      else if(words[0] == "G90")
      {
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

bool isInRange(int goal, int curPos, uint8_t id)
{
  return (abs(goal - curPos) <= ACCEPTABLE_RANGE[id-idX]);
}

void resetMovingVariables()
{
  isMoving = false;
  currentMoveDone = false;
  currentMove = 0;
  nbsMovements = 0;
  currentPosition = 0;
  hasFailed = false;

  for(int i = 0; i < 3; i++)
  {
    commands[i]._motorId = i+idX;
    commands[i]._goalPosition = Read(i+idX, PRESENT_POSITION);
  }
}

void HomingAxis(uint8_t id, int speed)
{
  Torque_off(id);
  Write(id, 0, HOMING_OFFSET);
  Torque_on(id);
  Wheel(id, speed);
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
  Torque_on(id);
}

void LimiteSwitch(){
  if(!digitalRead(emergencySwitchPin))
    isRising = true;
  else
    isFalling = true;
}

void setEmergency()
{
  isMoving = false;
  TorqueOffAll();
  Led(idX, digitalRead(xSwitchPin));
  Led(idY, digitalRead(ySwitchPin)); 
  Led(idZ, digitalRead(zSwitchPin));
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
