from machine import Pin
import time

class DHT11:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_UP)

    def read(self):
        self.data = []
        self.sinyal_gonder()
        self._check_response()
        for i in range(40):
            self.data.append(self._read_bit())
        return self._parse_data()

    def sinyal_gonder(self):
        self.pin.init(Pin.OUT)
        self.pin.value(0)  
        time.sleep_ms(18) 
        self.pin.init(Pin.IN) 
        time.sleep_us(40) 
        if not self.pin.read():
            time.sleep_us(80)
            if self.pin.read() : res = 1 
            else : res = -1
            
        while self.pin.read():
            if res == 1:
                rh_byte1 = self.veri_oku();
                rh_byte2 = self.veri_oku();
                temp_byte1 = self.veri_oku();
                temp_byte2 = self.veri_oku();
                checksum = self.veri_oku();
                
        if checksum == rh_byte1 + rh_byte2 + temp_byte1 + temp_byte2:
            hum = rh_byte1
            temp = temp_byte1

    def veri_oku(self):
        for j in range(8):
            while not self.pin.read(): pass
            time.sleep_us(50)
            if not self.pin.read():
                i &= ~( 1<<(7-j) )
            else:
                i |= ( 1<<(7-j) )
            while self.pin.read(): pass
        return i


dht = DHT11(pin=2)  

while True:
    try:
        temperature, humidity = dht.read()
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")
    except RuntimeError as e:
        print(f"Error: {e}")
    time.sleep(2)  # DHT11 requires at least a 1-second delay between reads
