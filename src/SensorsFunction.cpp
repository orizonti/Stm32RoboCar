#include "SensorsFunction.h"
#include "cmsis_os.h"
extern SPI_HandleTypeDef hspi1;
extern SPI_HandleTypeDef hspi3;

  void VoltageIndicatorClass::ShowLevel(uint8_t Level)
  {

	  CurrentLevel = Level;
          HAL_SPI_Transmit_IT(&hspi3, Data2, 1);
          HAL_SPI_Transmit_IT(&hspi3, Data, 1);
          cs_strob();

          HAL_SPI_Transmit_IT(&hspi3, Data2 + Level, 1);
          HAL_SPI_Transmit_IT(&hspi3, Data + Level, 1);
          cs_strob();
          osDelay(500);
  }

void VoltageIndicatorClass::ShowNextLevel()
{
  CurrentLevel++;
	if(CurrentLevel > 11)
	  CurrentLevel = 0;
  ShowLevel(CurrentLevel);
}


