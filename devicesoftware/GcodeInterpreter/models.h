#ifndef MODELS_H
#define MODELS_H

typedef struct MovingCommand
{
  uint8_t _motorId = 0;
  uint32_t _goalPosition = 0;
};

#endif
