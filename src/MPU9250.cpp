#include "MPU9250.h"
#include <stdint-gcc.h>
#include <stdlib.h>
#include <string.h>

extern char MESSAGE[50];
uint8_t MPU_ADDRESS = 0x68 << 1;


uint8_t ReadDeviceID()
{


                uint8_t DeviceId = 0;
                I2C_ReadBufferMem(hi2c1,0x68,0x75,&DeviceId,1);
                sprintf(MESSAGE,"WHO AM I = %02X  \r\n",DeviceId);
                HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
                HAL_Delay(500);
                return DeviceId;
}

void MPU_init (void) 
{
   uint8_t Command;
   
   Command = MPU9250_CLKSEL_INTER;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_PWR_MGMT_1, 1, 0x00, 1, 100);   // Clear sleep mode bit (6), enable all sensors 
   HAL_Delay(100);
   Command = MPU9250_CLKSEL_PLL;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_PWR_MGMT_1, 1, &Command, 1, 100);   // Set clock source to be PLL with x-axis gyroscope reference, bits 2:0 = 001
   
   // Configure Gyro and Accelerometer
   // Disable FSYNC and set accelerometer and gyro bandwidth to 44 and 42 Hz, respectively; 
   // DLPF_CFG = bits 2:0 = 010; this sets the sample rate at 1 kHz for both
   // Maximum delay is 4.9 ms which is just over a 200 Hz maximum rate
   Command = MPU9250_DLPF_41_BAND;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_CONFIG, 1, &Command, 1, 100);
   
   // Set sample rate = gyroscope output rate/(1 + SMPLRT_DIV)
   Command = 0x04;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_SMPLRT_DIV, 1, &Command, 1, 100);   // Use a 200 Hz rate; the same rate set in CONFIG above
   
   Command = MPU9250_DLPF_41_BAND | MPU9250_GYRO_FS_RANGE_500;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_GYRO_CONFIG, 1, &Command, 1, 100);    // Write new GYRO_CONFIG value to register

   Command = MPU9250_ACCEL_FS_RANGE_500;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_ACCEL_CONFIG, 1, &Command, 1, 100);   // Write new ACCEL_CONFIG register value

   Command = MPU9250_A_DLPF_BAND_41;
   HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_ACCEL_CONFIG2, 1, &Command, 1, 100);   // Write new ACCEL_CONFIG2 register value
   
   // The accelerometer, gyro, and thermometer are set to 1 kHz sample rates, 
   // but all these rates are further reduced by a factor of 5 to 200 Hz because of the SMPLRT_DIV setting

    // Configure Interrupts and Bypass Enable
    // Set interrupt pin active high, push-pull, and clear on read of INT_STATUS, enable I2C_BYPASS_EN so additional chips 
    // can join the I2C bus and all can be controlled by the Arduino as master

  // R=0x22;
  // HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_INT_PIN_CFG, 1, &R, 1, 100);
  // R=0x01;
  // HAL_I2C_Mem_Write(&hi2c1, MPU_ADDRESS, MPU9250_INT_ENABLE, 1, &R, 1, 100);   // Enable data ready (bit 0) interrupt
     

            uint32_t error = HAL_I2C_GetError(&hi2c1);
            if (error != HAL_I2C_ERROR_NONE)
            {
                    sprintf(MESSAGE, "I2C READ MEM ERROR - %02d \r\n",error);
                    HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
            }
}
//
void MPU_get_accel (AccelDataStruct* AccelData) 
{
    HAL_I2C_Mem_Read(&hi2c1, MPU_ADDRESS, MPU9250_ACCEL_XOUT_H, 1, (uint8_t*)AccelData, 6, 100);
    AccelData->Accel_X = AccelData->Accel_X_H << 8 | AccelData->Accel_X_L;
    AccelData->Accel_Y = AccelData->Accel_Y_H << 8 | AccelData->Accel_Y_L;
    AccelData->Accel_Z = AccelData->Accel_Z_H << 8 | AccelData->Accel_Z_L;

    //sprintf(MESSAGE,"ACCEL_X = %d ACCEL_Y  = %d ACCEL_Z = %d \r\n",AccelData->Accel_X,AccelData->Accel_Y,AccelData->Accel_Z);
    //HAL_UART_Transmit_IT(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE));
}
//
void MPU_get_gyro (GyroDataStruct* GyroData) 
{
    HAL_I2C_Mem_Read(&hi2c1, MPU_ADDRESS, MPU9250_ACCEL_XOUT_H, 1, (uint8_t*)GyroData, 6, 100);
    GyroData->Gyro_X = GyroData->Gyro_X_H << 8 | GyroData->Gyro_X_L;
    GyroData->Gyro_Y = GyroData->Gyro_Y_H << 8 | GyroData->Gyro_Y_L;
    GyroData->Gyro_Z = GyroData->Gyro_Z_H << 8 | GyroData->Gyro_Z_L;

    //sprintf(MESSAGE,"GYRO_X = %d GYRO_Y  = %d GYRO_Z = %d \r\n",GyroData->Gyro_X,GyroData->Gyro_Y,GyroData->Gyro_Z);
    //HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
}


void I2C_ReadBufferMem(I2C_HandleTypeDef hi, uint16_t DEV_ADDR,uint16_t REGISTER, uint8_t* Buffer,uint16_t sizebuf)
{
        while(HAL_I2C_Mem_Read(&hi, DEV_ADDR, REGISTER, 1, Buffer, sizebuf, 100)!= HAL_OK)
        {
            uint32_t error = HAL_I2C_GetError(&hi);
            if (error != HAL_I2C_ERROR_NONE)
            {
                    sprintf(MESSAGE, "I2C READ MEM ERROR - %02d \r\n",error);
                    HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
                    break;
            }
        }
}
void I2C_WriteBufferMem(I2C_HandleTypeDef hi, uint16_t DEV_ADDR,uint16_t REGISTER, uint8_t* Buffer,uint16_t sizebuf)
{
        while(HAL_I2C_Mem_Write(&hi, DEV_ADDR, REGISTER, 1, Buffer, sizebuf, 100)!= HAL_OK)
        {
            uint32_t error = HAL_I2C_GetError(&hi);
            if (error != HAL_I2C_ERROR_NONE)
            {
                    sprintf(MESSAGE, "I2C WRITE MEM ERROR - %02d ADDR - %02d \r\n",error,DEV_ADDR);
                    HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
                    break;
            }

        }
}

//void I2C_WriteBuffer(I2C_HandleTypeDef hi, uint8_t DEV_ADDR, uint8_t sizebuf)
//{
//        while(HAL_I2C_Master_Transmit(&hi, (uint16_t)DEV_ADDR,(uint8_t*) &ReadBuffer, (uint16_t)sizebuf, (uint32_t)1000)!= HAL_OK)
//        {
//            uint32_t error = HAL_I2C_GetError(&hi);
//            if (error != HAL_I2C_ERROR_NONE)
//            {
//                    sprintf(MESSAGE, "I2C WRITE ERROR - %02X \r\n",error);
//                    HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
//                    break;
//            }
//        }
//}
//void I2C_ReadBuffer(I2C_HandleTypeDef hi, uint8_t DEV_ADDR, uint8_t sizebuf)
//{
//        while(HAL_I2C_Master_Receive(&hi, (uint16_t)DEV_ADDR, (uint8_t*) &ReadBuffer, (uint16_t)sizebuf, (uint32_t)1000)!= HAL_OK)
//        {
//            uint32_t error = HAL_I2C_GetError(&hi);
//            if (error != HAL_I2C_ERROR_NONE)
//            {
//                    sprintf(MESSAGE, "I2C READ ERROR - %02X \r\n",error);
//                    HAL_UART_Transmit(&huart1,(uint8_t*)MESSAGE,strlen(MESSAGE),50);
//                    break;
//            }
//        }
//}

//void MPU_get_accel (AccelDataStruct* AccelData) 
//{
//        //I2C_ReadBufferMem(hi2c1,0x68,0x3b,AccelData,6);
//        //AccelData->Accel_X = (int16_t)(((int16_t)rawData[0] << 8) | rawData[1]) ;  // Turn the MSB and LSB into a signed 16-bit value
//        //AccelData->Accel_Y = (int16_t)(((int16_t)rawData[2] << 8) | rawData[3]) ;  
//        //AccelData->Accel_Z = (int16_t)(((int16_t)rawData[4] << 8) | rawData[5]) ; 
//}
////
//void MPU_get_gyro (GyroDataStruct* GyroData) 
//{
////  uint8_t rawData[6];  // x/y/z gyro register data stored here
////  HAL_I2C_Mem_Read(&hi2c1, MPU9250_ADDRESS_R, GYRO_XOUT_H, 1, rawData, 6, 100);    // Read the six raw data registers sequentially into data array
////  destination[0] = (int16_t)(((int16_t)rawData[0] << 8) | rawData[1]) ;  // Turn the MSB and LSB into a signed 16-bit value
////  destination[1] = (int16_t)(((int16_t)rawData[2] << 8) | rawData[3]) ;  
////  destination[2] = (int16_t)(((int16_t)rawData[4] << 8) | rawData[5]) ; 
//}
