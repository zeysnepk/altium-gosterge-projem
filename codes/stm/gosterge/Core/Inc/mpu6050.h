
#ifndef MPU6050_H
#define MPU6050_H

#include "stm32f4xx_hal.h"

#define MPU_ADDR		(0x68 << 1)
#define WHO_AM_I			0x75
#define PWR_MGMT_1			0x6B
#define SMPRT_DIV			0x19
#define CONFIG				0x1A
#define GYRO_CONF			0x1B
#define ACCEL_CONF 			0x1C
#define ACCEL_XOUT_H		0x3B

typedef struct {
    float ax;
    float ay;
    float az;
    float gx;
    float gy;
    float gz;
    float t;
} MpuData;

void Mpu_Conf(I2C_HandleTypeDef *hi2c);
void Mem_W_R(I2C_HandleTypeDef *hi2c, uint8_t addr, uint8_t *data, uint8_t *kontrol);
MpuData Mpu_Oku(I2C_HandleTypeDef *hi2c);
uint8_t WhoamI_Control(I2C_HandleTypeDef *hi2c);

#endif
