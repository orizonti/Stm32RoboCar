#include "stdint.h"
typedef struct 
{
   uint16_t HEADER1 = 0xD1;
   uint16_t HEADER2 = 0xF1;
   uint16_t SIZE_UNIT = 20;
} HEADER_STRUCT;


typedef struct 
{
   HEADER_STRUCT HEADER;

   uint16_t Speed1;
   uint16_t Speed2;
   uint16_t Speed3;
   uint16_t Speed4;
   
} DC_MotorControlStruct;

typedef struct 
{
   HEADER_STRUCT HEADER;


   uint16_t AccelX = 0x20;
   uint16_t AccelY = 0x20;
   uint16_t AccelZ = 0x20;

   uint16_t AngularSpeedX = 0x20;
   uint16_t AngularSpeedY = 0x20;
   uint16_t AngularSpeedZ = 0x20;
} AccelerometerDataStruct;


typedef struct 
{
   HEADER_STRUCT HEADER;

   uint16_t AngleMotor1;
   uint16_t AngleMotor2;
   uint16_t AngleMotor3;

   uint16_t SpeedMotor1;
   uint16_t SpeedMotor2;
   uint16_t SpeedMotor3;
} StepMotorControlStruct;

typedef struct 
{
   HEADER_STRUCT HEADER;

  uint16_t RangeRigth;
  uint16_t RangeLeft;
} RangeControlStruct;

typedef struct 
{
   HEADER_STRUCT HEADER;

  uint16_t CurrentConsumption;
  uint16_t BatteryVoltage;
} BatteryControlStruct;

