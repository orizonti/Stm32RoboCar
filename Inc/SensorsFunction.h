#ifndef SENS_FUNCTION
#define SENS_FUNCTION
#include <stdint.h>
#include "gpio.h"

#define cs_set() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_11, GPIO_PIN_SET)
#define cs_reset() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_11, GPIO_PIN_RESET)
#define cs_strob() cs_set();cs_reset()

#define CLR_set() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_1, GPIO_PIN_SET)
#define CLR_reset() HAL_GPIO_WritePin(GPIOD, GPIO_PIN_1, GPIO_PIN_RESET)

class VoltageIndicatorClass
{
  public:
  VoltageIndicatorClass()
  {
 Data2[0] = 0x0;    Data[0] = 0x0;
 Data2[1] = 0x0;    Data[1] = 0x1;
 Data2[2] = 0x0;    Data[2] = 0x3;
 Data2[3] = 0x0;    Data[3] = 0x7;
 Data2[4] = 0x0;    Data[4] = 0xF;
 Data2[5] = 0x0;    Data[5] = 0x1F;
 Data2[6] = 0x0;    Data[6] = 0x3F;
 Data2[7] = 0x0;    Data[7] = 0x7F;
 Data2[8] = 0x0;    Data[8] = 0xFF;
 Data2[9] = 0x8;    Data[9] = 0xFF;
 Data2[10] = 0xC;   Data[10] = 0xFF;
 Data2[11] = 0xFF;  Data[11] = 0xFF;

  cs_reset();
 }

  uint8_t Data[12];
  uint8_t Data2[12];
  uint8_t CurrentLevel = 0;

  void ShowLevel(uint8_t Level);
};
#endif
