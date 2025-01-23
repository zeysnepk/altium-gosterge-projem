from machine import Pin
import time


class ST7920:
    def __init__(self, sclk, cs, sid, rst):
        # Ekran boyutları
        self.startRow = 0
        self.startCol = 0
        self.endRow = 0
        self.endCol = 0
        self.numRows = 64
        self.numCols = 128
        self.graphic_check = 0
        self.image = bytearray((128 * 64) // 8)
        
        # GPIO pinleri
        self.sclk = Pin(sclk, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.sid = Pin(sid, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        self.init_lcd()
        
    def send_spi(self, byte):
        """Her bit için ayrı ayrı gönderilmiştir
        SPI kullanılmamıştır bu yüzden hız açından 
        pek performans sağlayamamıştır
        Herhangi bir GPIO pinleri ile 
        SPI gibi davranılması istenmiştir-düşük hız :(
        """
        self.sid.value(byte & 0x80 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x40 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x20 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x10 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x08 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x04 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x02 > 0)
        self.sclk.off()
        self.sclk.on()

        self.sid.value(byte & 0x01 > 0)
        self.sclk.off()
        self.sclk.on()


	#komut gönderme fonkssiyonu
    def send_cmd(self, cmd):
        self.cs.value(1)  
        self.send_spi(0xf8 + (0<<1))
        self.send_spi(cmd & 0xf0)
        self.send_spi((cmd<<4)&0xf0)
        time.sleep_us(50)
        self.cs.value(0)  

	#veri gönderme fonksiyonu
    def send_data(self, data):
        self.cs.value(1)
        self.send_spi(0xf8+(1<<1))
        self.send_spi(data&0xf0)
        self.send_spi((data<<4)&0xf0)
        time.sleep_us(50)
        self.cs.value(0)
        
    #metinsel ifadeler için fonksiyon
    def send_string(self, row, col, string):
        if row == 0:
            col = (col & 0x0F) | 0x80  
        elif row == 1:
            col = (col & 0x0F) | 0x90  
        elif row == 2:
            col = (col & 0x0F) | 0x88  
        elif row == 3:
            col = (col & 0x0F) | 0x98
        else:
            col = (col & 0x0F) | 0x80  
        self.send_cmd(col)  
        for char in string:
            self.send_data(ord(char))  

    #grafik modu veya metin modu için özelleştirilmiş fonksiyon
    def graphic_mode(self, enable):
        if enable == 1:
            self.send_cmd(0x30)
            time.sleep_ms(1)
            self.send_cmd(0x34)
            time.sleep_ms(1)
            self.send_cmd(0x36)
            time.sleep_ms(1)
            self.graphic_check = 1
        elif enable == 0:
            self.send_cmd(0x30)
            time.sleep_ms(1)
            self.graphic_check = 0
            
    #grafiksel işlemler için güncelleme fonksiyonu             
    def update(self):
        self.draw_bitmap(self.image)
                    
    #çalıştırılan ilk fonksiyon - ekranı başlatır
    def init_lcd(self):
        
        time.sleep_ms(40) 
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(50)

        
        self.send_cmd(0x30)
        time.sleep_us(110)
        self.send_cmd(0x30)
        time.sleep_us(40)
        self.send_cmd(0x08)
        time.sleep_us(110)
        self.send_cmd(0x01)
        time.sleep_ms(12)
        self.send_cmd(0x06)  
        time.sleep_ms(1)
        self.send_cmd(0x0C) 
        time.sleep_ms(1)
        self.send_cmd(0x01)  
        time.sleep_ms(1)

	#tüm ekranı temizler
    def clear(self):
        if self.graphic_check == 1:
            for y in range(64):
                if y<32:
                    self.send_cmd(0x80|y)
                    self.send_cmd(0x80)
                else:
                    self.send_cmd(0x80|(y-32))
                    self.send_cmd(0x88)
                for x in range(8):
                    self.send_data(0)
                    self.send_data(0)
        else:
            self.send_cmd(0x01)
            time.sleep_ms(2)
        for i in range(len(self.image)):
            self.image[i] = 0
    
	#pixel ayarlama
    def set_pixel(self,x,y):
        if 0 <= x < self.numCols and 0 <= y < self.numRows:
            p_index = (y * (self.numCols // 8)) + (x // 8)
            self.image[p_index] |= 0x80 >> (x % 8)
            
            if self.startRow > y:
                self.startRow = y
            if self.endRow <= y:
                self.endRow = y + 1
            if self.startCol > x:
                self.startCol = x
            if self.endCol <= x:
                self.endCol = x + 1
            
    #gönderilen iki nokta arasına çizgi çizer
    def draw_line(self, x0, y0, x1, y1):
        dx = (x1 - x0) if x1 >= x0 else (x0 - x1)
        dy = (y1 - y0) if y1 >= y0 else (y0 - y1)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set_pixel(x0, y0)  
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
            
    #draw_line fonksiyonu kullanılarak 4 çizgi birleştiren çerçeve
    def draw_frame(self, x0, y0, x1, y1):
        self.draw_line(x0, y0, x1, y0)
        self.draw_line(x0, y1, x1, y1)
        self.draw_line(x0, y0, x0, y1)
        self.draw_line(x1, y0, x1, y1)

	#Bitmap çizer
    def draw_xbmp(self, x, y, width, height, bitmap):
        if width <= 0 or height <= 0:
            return

        bytes_per_row = (width + 7) // 8
        max_x = min(x + width, self.numCols)
        max_y = min(y + height, self.numRows)

        for yy in range(y, max_y):
            if yy >= self.numRows:
                break
            
            row_start = (yy - y) * bytes_per_row
            for byte_x in range(bytes_per_row):
                curr_byte = bitmap[row_start + byte_x]
                
                for bit in range(8):
                    xx = byte_x * 8 + bit
                    if xx >= width:
                        break
                    if curr_byte & (1 << bit):
                        pixel_x = x + xx
                        pixel_y = yy

                        if pixel_x < self.numCols and pixel_y < self.numRows:
                            self.set_pixel(pixel_x, pixel_y)
    def draw_bitmap(self, graphic):
        #hareketli çizimler için iki ayrı bölüme gönderilip hız arttırılmıştır
        #ekranın üst bölümü
        for y in range(32):
            self.send_cmd(0x80 | y)
            self.send_cmd(0x80)
            
            offset = 16 * y
            for x in range(0, 16, 2):
                self.send_data(graphic[offset + x])
                self.send_data(graphic[offset + x + 1])

		#ekranın alt bölümüm
        for y in range(32, 64):
            self.send_cmd(0x80 | (y - 32))
            self.send_cmd(0x88)
            
            offset = 16 * y
            for x in range(0, 16, 2):
                self.send_data(graphic[offset + x])
                self.send_data(graphic[offset + x + 1])

                                

                

