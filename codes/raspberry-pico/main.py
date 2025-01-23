from st7920 import ST7920
from machine import Pin, I2C, reset
import time

import goz
from mpu6050 import MPU6050
import dht


class Main:
    def __init__(self):
        # reset butonu bir bacağı GND bağlı olduğundan PULL_UP
        self.reset = Pin(22, Pin.IN, Pin.PULL_UP)
        self.buton_1 = Pin(12, Pin.IN)
        self.buton_2 = Pin(7, Pin.IN)
        self.buton_3 = Pin(5, Pin.IN)
        # st7920 için SPI kullanılmamıştır
        self.lcd = ST7920(sclk=Pin(11), cs=Pin(9), sid=Pin(10), rst=Pin(6))
        # dht11 için kütüphane kullanılmıştır
        self.d = dht.DHT11(machine.Pin(2))
        i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=200000) 
        self.mpu = MPU6050(i2c)
        
        # güç verildiğinde ilk gösterilen fonksiyon
        self.intro()
        self.baslangic = time.ticks_ms()
        self.onceki_buton = 0
        self.buton = 0
        
    def intro(self):
        # gozler bitmap'leri için ayrı bir dosyada bitmap array şeklinde tanımlanmıştır
        gozler = [goz.goz_1, goz.goz_5]
        self.lcd.send_string(3,0,f"Zeynep Kaplan")
        self.lcd.graphic_mode(1)
        for i in gozler:
            self.lcd.clear()
            self.lcd.draw_xbmp(0,0,128,64,i)
            self.lcd.update()
            
    def buton_kontrol(self):
        if not self.reset.value():
            machine.reset()
        if self.buton_1.value():
            time.sleep_ms(20)
            if self.onceki_buton != 1:
                self.buton = 1
        elif self.buton_2.value():
            time.sleep_ms(20)
            if self.onceki_buton != 2:
                self.buton = 2
        elif self.buton_3.value():
            time.sleep_ms(20)
            if self.onceki_buton != 3:
                self.buton = 3
            
        self.onceki_buton = self.buton
            
    def loop(self):
        self.anlik_zaman = time.ticks_ms()
        self.buton_kontrol()
        # yarım saniyelik periyot
        if(self.anlik_zaman - self.baslangic >= 500):
            self.baslangic = self.anlik_zaman
            # import edilen modülden mpu verilerini çekme
            ax, ay, az, gx, gy, gz, temp = self.mpu.mpu_verileri_al()
            self.d.measure()
            temp_2 = self.d.temperature()
            hum = self.d.humidity()
            # ölçülen iki sıcaklık verisinin ortalaması alınmıştır
            temp_value = (temp+temp_2)/2
            time.sleep_ms(10)
            if self.buton == 1:
                # ilk buton ivme verilerini gösterir
                self.mpu_goster("ivme olcumleri", "a", "m/s2" ,ax, ay, az)
            elif self.buton == 2:
                # ikinci buton gyro verilerini gosterir
                self.mpu_goster("gyro olcumleri", "g", "rad/s" ,gx, gy, gz)
            elif self.buton == 3:
                # üçüncü buton ise sıcaklık ve nem bilgisini gösterir
                self.dht_goster(temp_value, hum)
        time.sleep(0.1)
                
    def mpu_goster(self, baslik, sym, birim, veri_x, veri_y, veri_z):
        self.lcd.clear()  
        # string ifadeler için grafik modu disable
        self.lcd.graphic_mode(0)  
        self.lcd.send_string(0, 0, f"{baslik}")  
        self.lcd.send_string(1, 0, f"{sym}x = {veri_x:.3f}{birim}") 
        self.lcd.send_string(2, 0, f"{sym}y = {veri_y:.3f}{birim}")  
        self.lcd.send_string(3, 0, f"{sym}z = {veri_z:.3f}{birim}")
        
    def dht_goster(self, temp, hum):
        self.lcd.clear()
        self.lcd.graphic_mode(0)
        self.lcd.send_string(0, 0, f"Temp = {temp:.4f}C")
        self.lcd.send_string(1, 0, f"---------------------------------")
        self.lcd.send_string(2, 0, f"Hum = {hum} %") 
     
main = Main()
while True:
    main.loop()
    
