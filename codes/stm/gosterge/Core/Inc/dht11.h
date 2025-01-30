
#ifndef DHT11_H
#define DHT11_H


#include "stm32f4xx_hal.h"




typedef struct {
    int hum;
    int temp;
} Dht11;


Dht11 DHT11_Oku(TIM_HandleTypeDef *htim, GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
void Pin_Output(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
void Pin_Input(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);
void Delay_Microseconds(TIM_HandleTypeDef *htim, uint16_t time);
int8_t DHT_veri_al(TIM_HandleTypeDef *htim, GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin);


#endif
