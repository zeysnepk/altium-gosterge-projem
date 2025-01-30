

#include "dht11.h"


Dht11 DHT11_Oku(TIM_HandleTypeDef *htim, GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin){
	int8_t presence, rh_byte1, rh_byte2, temp_byte1, temp_byte2, checksum;
	Dht11 dht;
	HAL_TIM_Base_Start(htim);
	Pin_Output(GPIOx, GPIO_Pin);
	HAL_GPIO_WritePin(GPIOx, GPIO_Pin, GPIO_PIN_RESET);
	HAL_Delay(18);
	Pin_Input(GPIOx, GPIO_Pin);
	int8_t res = 0;
	Delay_Microseconds(htim, 40);
	if ( !(HAL_GPIO_ReadPin(GPIOx, GPIO_Pin)) ){
		Delay_Microseconds(htim, 80);
		if( HAL_GPIO_ReadPin(GPIOx, GPIO_Pin) ){
			res = 1;
		} else{
			res = -1;
		}
	}
	while( HAL_GPIO_ReadPin(GPIOx, GPIO_Pin) );
	if( res == 1 ){
	    rh_byte1 = DHT_veri_al(htim, GPIOx, GPIO_Pin);
	    rh_byte2 = DHT_veri_al(htim, GPIOx, GPIO_Pin);
	    temp_byte1 = DHT_veri_al(htim, GPIOx, GPIO_Pin);
	    temp_byte2 = DHT_veri_al(htim, GPIOx, GPIO_Pin);
	    checksum = DHT_veri_al(htim, GPIOx, GPIO_Pin);

	    if( checksum == (rh_byte1 + rh_byte2 + temp_byte1 + temp_byte2) ){
	    	dht.hum = rh_byte1;
	    	dht.temp = temp_byte1;
	    }
	}
	return dht;
}

void Pin_Output(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin){
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	HAL_GPIO_WritePin(GPIOx, GPIO_Pin, GPIO_PIN_RESET);
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void Pin_Input(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin){
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	GPIO_InitStruct.Pin = GPIO_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	HAL_GPIO_Init(GPIOx, &GPIO_InitStruct);
}

void Delay_Microseconds(TIM_HandleTypeDef *htim, uint16_t time){
	__HAL_TIM_SET_COUNTER(htim, 0);
	while( __HAL_TIM_GET_COUNTER(htim) < time );
}

int8_t DHT_veri_al(TIM_HandleTypeDef *htim, GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin){
	uint8_t i = 0;
	for( uint8_t j=0; j<8; j++ ){
		while( !(HAL_GPIO_ReadPin(GPIOx, GPIO_Pin)) );
		Delay_Microseconds(htim, 50);
		if( !(HAL_GPIO_ReadPin(GPIOx, GPIO_Pin)) ){
			i &= ~( 1 << ( 7 - j ) );
		} else{
			i |= ( 1 << ( 7 - j ) );
		}
		while( HAL_GPIO_ReadPin(GPIOx, GPIO_Pin) );
	}
	return i;
}
