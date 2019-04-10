#ifndef FUNCTIONS_H
#define FUNCTIONS_H

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
void HomingAxis(uint8_t id, int speed);
uint8_t getIdFromChar(char letter);
bool isInRange(int curPos, int goal);
void resetMovingVariables();
void changeMode(uint8_t id);

#endif
