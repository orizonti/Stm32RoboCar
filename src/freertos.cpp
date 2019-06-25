/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * File Name          : freertos.c
  * Description        : Code for freertos applications
  ******************************************************************************
  * This notice applies to any and all portions of this file
  * that are not between comment pairs USER CODE BEGIN and
  * USER CODE END. Other portions of this file, whether 
  * inserted by the user or by software development tools
  * are owned by their respective copyright owners.
  *
  * Copyright (c) 2019 STMicroelectronics International N.V. 
  * All rights reserved.
  *
  * Redistribution and use in source and binary forms, with or without 
  * modification, are permitted, provided that the following conditions are met:
  *
  * 1. Redistribution of source code must retain the above copyright notice, 
  *    this list of conditions and the following disclaimer.
  * 2. Redistributions in binary form must reproduce the above copyright notice,
  *    this list of conditions and the following disclaimer in the documentation
  *    and/or other materials provided with the distribution.
  * 3. Neither the name of STMicroelectronics nor the names of other 
  *    contributors to this software may be used to endorse or promote products 
  *    derived from this software without specific written permission.
  * 4. This software, including modifications and/or derivative works of this 
  *    software, must execute solely and exclusively on microcontroller or
  *    microprocessor devices manufactured by or for STMicroelectronics.
  * 5. Redistribution and use of this software other than as permitted under 
  *    this license is void and will automatically terminate your rights under 
  *    this license. 
  *
  * THIS SOFTWARE IS PROVIDED BY STMICROELECTRONICS AND CONTRIBUTORS "AS IS" 
  * AND ANY EXPRESS, IMPLIED OR STATUTORY WARRANTIES, INCLUDING, BUT NOT 
  * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
  * PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY
  * RIGHTS ARE DISCLAIMED TO THE FULLEST EXTENT PERMITTED BY LAW. IN NO EVENT 
  * SHALL STMICROELECTRONICS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
  * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
  * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
  * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */     
#include "transfer_data_type.h"
#include "SensorsFunction.h"
#include "usart.h"
#include "gpio.h"
#include "spi.h"
#include "MPU9250.h"
#include "cstring"
#include "cstdlib"
/* USER CODE END Includes */

#include "FreeRTOS.h"
#include "task.h"
#include "main.h"
#include "cmsis_os.h"
/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
//   uint8_t Data[12];
//   uint8_t Data2[12];

VoltageIndicatorClass VoltageIndicator;
VoltageIndicatorClass* VoltageIndicator2;
extern SPI_HandleTypeDef hspi1;
extern SPI_HandleTypeDef hspi3;
extern char MESSAGE[50];
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
AccelDataStruct* AccelData;
GyroDataStruct*  GyroData;
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN Variables */


typedef struct 
{
  GPIO_PinState Line1;
  GPIO_PinState Line2;
  GPIO_PinState Line3;
  GPIO_PinState Line4;
} STEP_COMMAND;




void TakeStep(STEP_COMMAND* COMMAND)
{
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_0,COMMAND->Line1);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_2,COMMAND->Line2);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_4,COMMAND->Line3);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_6,COMMAND->Line4);

  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_1,COMMAND->Line1);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_3,COMMAND->Line2);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_5,COMMAND->Line3);
  HAL_GPIO_WritePin(GPIOD,GPIO_PIN_7,COMMAND->Line4);

  HAL_GPIO_WritePin(GPIOC,GPIO_PIN_0,COMMAND->Line1);
  HAL_GPIO_WritePin(GPIOC,GPIO_PIN_1,COMMAND->Line2);
  HAL_GPIO_WritePin(GPIOC,GPIO_PIN_2,COMMAND->Line3);
  HAL_GPIO_WritePin(GPIOC,GPIO_PIN_3,COMMAND->Line4);
}

void SetCommand(int in1,int in2,int in3,int in4,STEP_COMMAND* COMMAND)
{
 COMMAND->Line1 = GPIO_PIN_SET; 
 COMMAND->Line2 = GPIO_PIN_SET; 
 COMMAND->Line3 = GPIO_PIN_SET; 
 COMMAND->Line4 = GPIO_PIN_SET; 
 if(in1 == 0)
 COMMAND->Line1 = GPIO_PIN_RESET; 
 if(in2 == 0)
 COMMAND->Line2 = GPIO_PIN_RESET; 
 if(in3 == 0)
 COMMAND->Line3 = GPIO_PIN_RESET; 
 if(in4 == 0)
 COMMAND->Line4 = GPIO_PIN_RESET; 
}

 

  //osPoolDef(AccelDataPool, 20, AccelerometerDataStruct);                    // Define memory pool
  //#define osMessageQDef(name, queue_sz, type)   

  //QUEUES TO CONTROL MOTORS
  osMessageQDef(StepMotorCommandQueue, 8, StepMotorControlStruct);
  osMessageQDef(DCMotorCommandQueue, 8, DC_MotorControlStruct);

	osMessageQId DCMotorCommandQueueHandle;  //HANDLES TO INTERRACT TO QUEUES
	osMessageQId StepMotorCommandQueueHandle;

  //QUEUES TO SEND BLOCKS STATE
  osMessageQDef(AccelStateQueue, 8, AccelerometerDataStruct);
  osMessageQDef(StepMotorStateQueue, 8, StepMotorControlStruct);
  osMessageQDef(DCMotorStateQueue, 8, DC_MotorControlStruct);
  osMessageQDef(RangersStateQueue, 8, RangeControlStruct);
  osMessageQDef(BatteryStateQueue, 8, BatteryControlStruct);

	osMessageQId DCMotorStateQueueHandle;  //HANDLES TO INTERRACT TO QUEUES
	osMessageQId StepMotorStateQueueHandle;
	osMessageQId AccelStateQueueHandle;
	osMessageQId RangersStateQueueHandle;
	osMessageQId BatteryStateQueueHandle;

osPoolId  AccelDataPoolHandle;  // MEMORY POOL ID FOR QUEUES, IS'T USED YET

osThreadId SensorMonitorinHandle;
osThreadId Uart_Control_TaHandle;
osThreadId DC_Motor_ContHandle;
osThreadId StepMotor_ConHandle;


/* USER CODE END Variables */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN FunctionPrototypes */
   
void SensorMonitorFunction(void const * argument);
void UARTTransferFunction(void const * argument);
void DC_Motor_Function(void const * argument);
void StepMotorFunc(void const * argument);

void MX_FREERTOS_Init(void); /* (MISRA C 2004 rule 8.1) */
/* USER CODE END FunctionPrototypes */


/**
  * @brief  FreeRTOS initialization
  * @param  None
  * @retval None
  */
void MX_FREERTOS_Init(void) {
  /* USER CODE BEGIN Init */
  /* definition and creation of SensorMonitorin */
  osThreadDef(SensorMonitorin, SensorMonitorFunction, osPriorityNormal, 0, 512);
  SensorMonitorinHandle = osThreadCreate(osThread(SensorMonitorin), NULL);

  /* definition and creation of Uart_Control_Ta */
  osThreadDef(Uart_Control_Ta, UARTTransferFunction, osPriorityIdle, 0, 512);
  Uart_Control_TaHandle = osThreadCreate(osThread(Uart_Control_Ta), NULL);

  //osThreadDef(DC_Motor_Cont, DC_Motor_Function, osPriorityIdle, 0, 256);
  //DC_Motor_ContHandle = osThreadCreate(osThread(DC_Motor_Cont), NULL);

  ///* definition and creation of StepMotor_Con */
  //osThreadDef(StepMotor_Con, StepMotorFunc, osPriorityIdle, 0, 256);
  //StepMotor_ConHandle = osThreadCreate(osThread(StepMotor_Con), NULL);
  /* USER CODE END Init */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* Create the thread(s) */

  /* definition and creation of DC_Motor_Cont */

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* Create the queue(s) */
  /* definition and creation of StepCommandQueue */


  /* USER CODE BEGIN RTOS_QUEUES */
  //STATE FROM MC DATA QUEUES
  //AccelDataPoolHandle = osPoolCreate(osPool(AccelDataPool));                 // create memory pool
  AccelStateQueueHandle = osMessageCreate(osMessageQ(AccelStateQueue), NULL);
  StepMotorStateQueueHandle = osMessageCreate(osMessageQ(StepMotorStateQueue), NULL);
  DCMotorStateQueueHandle = osMessageCreate(osMessageQ(DCMotorStateQueue), NULL);
  RangersStateQueueHandle = osMessageCreate(osMessageQ(RangersStateQueue), NULL);
  BatteryStateQueueHandle = osMessageCreate(osMessageQ(BatteryStateQueue), NULL);

  //COMMAND FROM USER QUEUES
  StepMotorCommandQueueHandle = osMessageCreate(osMessageQ(StepMotorCommandQueue), NULL);
  DCMotorCommandQueueHandle = osMessageCreate(osMessageQ(DCMotorCommandQueue), NULL);
  /* USER CODE END RTOS_QUEUES */
}

/* USER CODE BEGIN Header_SensorMonitorFunction */
/**
  * @brief  Function implementing the SensorMonitorin thread.
  * @param  argument: Not used 
  * @retval None
  */
/* USER CODE END Header_SensorMonitorFunction */
void SensorMonitorFunction(void const * argument)
{
  /* USER CODE BEGIN SensorMonitorFunction */

   AccelData = new AccelDataStruct;
   GyroData =  new GyroDataStruct;
      AccelerometerDataStruct* AccelDataMessage = new AccelerometerDataStruct;

      ReadDeviceID();
      osDelay(300);
      MPU_init();
  /* Infinite loop */
  for(;;)
  {
  osDelay(100);  

    MPU_get_accel(AccelData);
    MPU_get_gyro(GyroData);
    memcpy((uint8_t*)AccelDataMessage + 6,(uint8_t*)AccelData + 6,6);
    memcpy((uint8_t*)AccelDataMessage + 12,(uint8_t*)GyroData + 6,6);


      AccelDataMessage->HEADER.HEADER1 = 0xF1;
      AccelDataMessage->HEADER.HEADER2 = 0xD2;
      AccelDataMessage->HEADER.SIZE_UNIT = 6+12;
        HAL_UART_Transmit_IT(&huart1,(uint8_t*)(MESSAGE),strlen(MESSAGE));
 //---------------------------------------------------------
 VoltageIndicator.ShowNextLevel();
 //---------------------------------------------------------
    osMessagePut(AccelStateQueueHandle, (uint32_t)AccelDataMessage, osWaitForever);  // Send Message
  }
  delete AccelData;
  delete GyroData;
  //delete AccelDataMessage;

  /* USER CODE END SensorMonitorFunction */
}

/* USER CODE BEGIN Header_UARTTransferFunction */
/**
* @brief Function implementing the Uart_Control_Ta thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_UARTTransferFunction */
void UARTTransferFunction(void const * argument)
{
  /* USER CODE BEGIN UARTTransferFunction */
  /* Infinite loop */
  uint8_t SendData[20];

   AccelerometerDataStruct* Data;
  /* Infinite loop */
  for(;;)
  {

        osEvent event = osMessageGet(AccelStateQueueHandle,osWaitForever);
		//sprintf(MESSAGE,"GET DATA status - %02X \r\n",event.status);
		//HAL_UART_Transmit_IT(&huart1,(uint8_t*)(MESSAGE),strlen(MESSAGE));
    //    osDelay(10);

      if(event.status == osEventMessage)
      {
          Data = (AccelerometerDataStruct*)event.value.p;

          if(Data->HEADER.SIZE_UNIT == 18)
          {
            memcpy(SendData,(uint8_t*)Data,18);

          sprintf(MESSAGE,"ACCEL_X = %d ACCEL_Y  = %d ACCEL_Z = %d \r\n",Data->AccelX,
                                                                        Data->AccelY,
                                                                        Data->AccelZ);

          HAL_UART_Transmit_IT(&huart1,(uint8_t*)(MESSAGE),strlen(MESSAGE));
          osDelay(10);

          sprintf(MESSAGE,"HEADER - %02X SIZE - %d\r\n",Data->HEADER.HEADER1,Data->HEADER.SIZE_UNIT);
          HAL_UART_Transmit_IT(&huart1,(uint8_t*)(MESSAGE),strlen(MESSAGE));
          osDelay(10);

          //HAL_UART_Transmit_IT(&huart1,SendData,18);
          }
          //osPoolFree(AccelDataPoolHandle, Data);                  // free memory allocated for message
      }

    //          event = osMessageGet(DCMotorStateQueueHandle,0);
    //  if(event.status == osEventMessage)
    //  {
    //    HEADER_STRUCT* Data = (HEADER_STRUCT*)event.value.p;
    //    HAL_UART_Transmit_IT(&huart1,(uint8_t*)(Data),Data->SIZE_UNIT);
    //    osDelay(20);
    //  }

    //          event = osMessageGet(StepMotorStateQueueHandle,0);
    //  if(event.status == osEventMessage)
    //  {
    //    HEADER_STRUCT* Data = (HEADER_STRUCT*)event.value.p;
    //    HAL_UART_Transmit_IT(&huart1,(uint8_t*)(Data),Data->SIZE_UNIT);
    //    osDelay(20);
    //  }

    //          event = osMessageGet(RangersStateQueueHandle,0);
    //  if(event.status == osEventMessage)
    //  {
    //    HEADER_STRUCT* Data = (HEADER_STRUCT*)event.value.p;
    //    HAL_UART_Transmit_IT(&huart1,(uint8_t*)(Data),Data->SIZE_UNIT);
    //    osDelay(20);
    //  }

    //          event = osMessageGet(BatteryStateQueueHandle,0);
    //  if(event.status == osEventMessage)
    //  {
    //    HEADER_STRUCT* Data = (HEADER_STRUCT*)event.value.p;
    //    HAL_UART_Transmit_IT(&huart1,(uint8_t*)(Data),Data->SIZE_UNIT);
    //    osDelay(20);
    //  }


  }
        //sprintf(MESSAGE,"ACCEL X = %d Y = %d Z = %d \r\n",Data->Accel_X,Data->Accel_Y,Data->Accel_Z);
        //HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));

  //READ COMMAND FROM UART TO CONTROL STEP MOTOR
   //if(huart1.RxXferCount == 0)
   //{
   //          if(DataRec[0] == 0xA1 && DataRec[1] == 0xF1)
   //          {
   //            MESSAGE_SIZE = DataRec[2];
   //            DataRec[0] = 0;
   //            DataRec[1] = 0;
   //            HAL_UART_Receive_IT(&huart1,DataRec,MESSAGE_SIZE);
   //            osDelay(10);
   //           //     sprintf(MESSAGE+3,"MC WAIT BYTES %d",MESSAGE_SIZE);
   //           //     MESSAGE[2] = strlen(MESSAGE+3);
   //           //     HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
   //           // osDelay(10);
   //          }

   //          if(MESSAGE_SIZE != 0)
   //          {

   //            if(DataRec[0] == 0x01)
   //            {
   //                sprintf(MESSAGE+3,"recieved - %s",DataRec);
   //                MESSAGE[2] = strlen(MESSAGE+3);
   //                HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
   //                osDelay(10);
   //            }

   //                if(DataRec[0] == 0xD1)
   //                {
   //                    MotorRecCommand = (MotorControl*)(DataRec+1);
   //                    StepMotorCommand.NumberMotor = MotorRecCommand->NumberMotor;
   //                    StepMotorCommand.Direction = MotorRecCommand->Direction;
   //                    StepMotorCommand.Speed = MotorRecCommand->Speed;
   //                    StepMotorCommand.Angle = MotorRecCommand->Angle;
   //                        osMessagePut(StepCommandQueueHandle,&StepMotorCommand,5);
   //                    sprintf(MESSAGE+3,"MOTOR COMMAND - %d %d %d %d",StepMotorCommand.NumberMotor,
   //                                                                    StepMotorCommand.Direction,
   //                                                                    StepMotorCommand.Angle,
   //                                                                    StepMotorCommand.Speed);
   //                    MESSAGE[2] = strlen(MESSAGE+3);
   //                    HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
   //                    osDelay(40);
   //                }

   //            if(DataRec[0] == 0xD2)
   //            {
   //                sprintf(MESSAGE+3,"COMMAND TO DC MOTOR GET");
   //                MESSAGE[2] = strlen(MESSAGE+3);
   //                HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
   //                osDelay(10);


   //            }

   //                MESSAGE_SIZE = 0;
   //            HAL_UART_Receive_IT(&huart1,DataRec,3);
   //          }
   //  }
  //=========================================================================================
  /* USER CODE END UARTTransferFunction */

}

/* USER CODE BEGIN Header_DC_Motor_Function */
/**
* @brief Function implementing the DC_Motor_Cont thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_DC_Motor_Function */
void DC_Motor_Function(void const * argument)
{
  /* USER CODE BEGIN DC_Motor_Function */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1);
  }
  /* USER CODE END DC_Motor_Function */
}

/* USER CODE BEGIN Header_StepMotorFunc */
/**
* @brief Function implementing the StepMotor_Con thread.
* @param argument: Not used
* @retval None
*/
/* USER CODE END Header_StepMotorFunc */
void StepMotorFunc(void const * argument)
{
  /* USER CODE BEGIN StepMotorFunc */
  /* Infinite loop */
 //uint8_t MESSAGE[20];

 STEP_COMMAND COMMAND_SEQUENCE[8];
  SetCommand(1,0,0,0,&COMMAND_SEQUENCE[0]);
  SetCommand(1,1,0,0,&COMMAND_SEQUENCE[1]);
  SetCommand(0,1,0,0,&COMMAND_SEQUENCE[2]);
  SetCommand(0,1,1,0,&COMMAND_SEQUENCE[3]);
  SetCommand(0,0,1,0,&COMMAND_SEQUENCE[4]);
  SetCommand(0,0,1,1,&COMMAND_SEQUENCE[5]);
  SetCommand(0,0,0,1,&COMMAND_SEQUENCE[6]);
  SetCommand(1,0,0,1,&COMMAND_SEQUENCE[7]);

  STEP_COMMAND COMMAND_SEQUENCE_FULL[4];
  SetCommand(1,0,0,1,&COMMAND_SEQUENCE_FULL[0]);
  SetCommand(1,1,0,0,&COMMAND_SEQUENCE_FULL[1]);
  SetCommand(0,1,1,0,&COMMAND_SEQUENCE_FULL[2]);
  SetCommand(0,0,1,1,&COMMAND_SEQUENCE_FULL[3]);

  STEP_COMMAND COMMAND_SEQUENCE_FULL_BACK[4];
  SetCommand(0,0,1,1,&COMMAND_SEQUENCE_FULL_BACK[0]);
  SetCommand(0,1,1,0,&COMMAND_SEQUENCE_FULL_BACK[1]);
  SetCommand(1,1,0,0,&COMMAND_SEQUENCE_FULL_BACK[2]);
  SetCommand(1,0,0,1,&COMMAND_SEQUENCE_FULL_BACK[3]);
  int n = 0;

  int count_sector = 0;
  int Direction = 1;

  /* Infinite loop */
  for(;;)
  {
    osDelay(4);
      count_sector++;
      
      if(count_sector == 400)
      {
        count_sector = 0;
        Direction = Direction*-1;
      }

      if(Direction == 1)
      {
      TakeStep(COMMAND_SEQUENCE_FULL + n);
      n++;
      if(n == 4)
      n = 0;
      }

      if(Direction == -1)
      {
      TakeStep(COMMAND_SEQUENCE_FULL_BACK + n);
      n++;
      if(n == 4)
      n = 0;
      }

 //     osEvent event = osMessageGet(StepMotorCommandQueueHandle,0);
 //     if(event.status == osEventMessage)
 //     {
 //       StepMotorControlStruct* Data = event.value.p;
        //Direction = Data->Direction;

          //sprintf(MESSAGE,"DIRECTION - %d  \r\n",Direction);
          //HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
          //osDelay(20);
      }
  /* USER CODE END StepMotorFunc */
}

/* Private application code --------------------------------------------------*/
/* USER CODE BEGIN Application */
     
/* USER CODE END Application */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
