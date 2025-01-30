
#include "mpu6050.h"


uint8_t WhoamI_Control(I2C_HandleTypeDef *hi2c){
	uint8_t who_am_i;
	uint8_t reg = WHO_AM_I;
	HAL_I2C_Master_Transmit(hi2c, MPU_ADDR, &reg, 1, 100);
	HAL_I2C_Master_Receive(hi2c, MPU_ADDR, &who_am_i, 1, 100);
	return who_am_i;
}

void Mpu_Conf(I2C_HandleTypeDef *hi2c){
	uint8_t kontrol = 0;
	// sleep modundan çıkma
	uint8_t data = 0x00;
	Mem_W_R(hi2c, PWR_MGMT_1, &data, &kontrol);

	/*
	DLPF reg aktif olduğundan Gyroscope Output Rate = 1kHz
	Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
	SMPLRT_DIV = 0 ile sample rate = 1kHz ayarlandı */
	data = 0x00;
	Mem_W_R(hi2c, SMPRT_DIV, &data, &kontrol);

	 //daha hassas ölçüm için DLPF orta değerde ayarlandı
	data = 0x03;
	Mem_W_R(hi2c, CONFIG, &data, &kontrol);

	// Gyroscope ± 250 °/s ayarlandı
	data = 0x00;
	Mem_W_R(hi2c,GYRO_CONF, &data, &kontrol);
	// Accelerometer ± 2g ayarlandı
	Mem_W_R(hi2c,ACCEL_CONF, &data, &kontrol);

}

void Mem_W_R(I2C_HandleTypeDef *hi2c, uint8_t addr, uint8_t *data, uint8_t *kontrol){
	HAL_I2C_Mem_Write(hi2c, MPU_ADDR, addr, 1, data, 1, 100);
	HAL_I2C_Mem_Read(hi2c, MPU_ADDR, addr, 1, kontrol, 1, 100);
}

MpuData Mpu_Oku(I2C_HandleTypeDef *hi2c){
	uint8_t mpu_data[14];
	HAL_I2C_Mem_Read(hi2c, MPU_ADDR, ACCEL_XOUT_H, 1, mpu_data, 14, 500);
	int16_t acc_x = ( int16_t )( ( mpu_data[0] << 8 ) | mpu_data[1] );
	int16_t acc_y = ( int16_t )( ( mpu_data[2] << 8 ) | mpu_data[3] );
	int16_t acc_z = ( int16_t )( ( mpu_data[4] << 8 ) | mpu_data[5] );
	int16_t temp = ( int16_t )( ( mpu_data[6] << 8 ) | mpu_data[7] );
	int16_t gyro_x = ( int16_t )( ( mpu_data[8] << 8 ) | mpu_data[9] );
	int16_t gyro_y = ( int16_t )( ( mpu_data[10] << 8 ) | mpu_data[11] );
	int16_t gyro_z = ( int16_t )( ( mpu_data[12] << 8 ) | mpu_data[13] );

	MpuData data;

	data.ax = (float)acc_x / 16384.0;
	data.ay = (float)acc_y / 16384.0;
	data.az = (float)acc_z / 16384.0;

	data.gx = (float)gyro_x / 131.0;
	data.gy = (float)gyro_y / 131.0;
	data.gz = (float)gyro_z / 131.0;

	data.t = temp / 340 + 36.53;

	return data;
}



