from machine import I2C, Pin
import time

class MPU6050:
    MPU6050_ADDR    =   0x68
    PWR_MGMT_1      =   0x6B
    SMPRT_DIV       =   0x19
    GYRO_CONFIG     =   0x1B
    ACCEL_CONFIG    =   0x1C
    ACCEL_XOUT_H    =   0x3B
    GYRO_XOUT_H     =   0x43
    TEMP_OUT_H      =   0x41
    
    ALPHA           =   0.1
    YERCEKIMI       =   9.81
    PI              =   3.14

    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = self.MPU6050_ADDR
        self.mpu_ayarlar()

    def mpu_ayarlar(self):
        # Güç yönetim ayarı
        self.i2c.writeto_mem(self.addr, self.PWR_MGMT_1, b'\x00')
        # Veri hızı ayarı
        self.i2c.writeto_mem(self.addr, self.SMPRT_DIV, b'\x07')
        # Gyroskop ölçüm ayarı
        self.i2c.writeto_mem(self.addr, self.GYRO_CONFIG, b'\x00')
        # İvmeölçer ölçüm ayarı
        self.i2c.writeto_mem(self.addr, self.ACCEL_CONFIG, b'\x00')
        time.sleep_ms(200) 
        

    def raw_veri(self, reg):
        # Yüksek byte okuma
        high = self.i2c.readfrom_mem(self.addr, reg, 1)[0]
        # Düşük byte okuma
        low = self.i2c.readfrom_mem(self.addr, reg + 1, 1)[0]
        #birleştirme ve SET etme
        value = (high << 8) | low
        # Negatif değerleri işleme sokma
        if value >= 0x8000:
            value = -((65535 - value) + 1)
        return value

    def mpu_verileri_al(self):
        # İvme verileri(m/s²)
        ax = ( ( self.raw_veri(self.ACCEL_XOUT_H) ) 
              / 16384.0 ) * 9.80665 * self.ALPHA - 0.4
        ay = ( ( self.raw_veri(self.ACCEL_XOUT_H + 2) ) 
              / 16384.0 ) * 9.80665 * self.ALPHA
        az = ( ( ( self.raw_veri(self.ACCEL_XOUT_H + 4) ) 
                / 16384.0 ) * 9.80665 - self.YERCEKIMI ) * self.ALPHA
        
        # Jiroskop verileri (rad/s)
        gx = ( ( self.raw_veri(self.GYRO_XOUT_H) ) 
              / 131.0 ) * (self.PI /  180.0)
        gy = ( ( self.raw_veri(self.GYRO_XOUT_H + 2) ) 
              / 131.0 ) * (self.PI /  180.0)
        gz = ( ( self.raw_veri(self.GYRO_XOUT_H + 4) ) 
              / 131.0 ) * (self.PI /  180.0)

        #Sıcaklık verisi(°C)
        temp = ( self.raw_veri(self.TEMP_OUT_H) ) 
        / 340 + 36.53
        
        return ax, ay, az, gx, gy, gz, temp
        


