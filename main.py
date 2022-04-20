import machine
import gc
import lcd
from machine import I2C, Pin
import adafruit_mlx90640
import st7789

machine.freq(240000000)
gc.collect()

# init lcd
spi_sck = Pin(2, Pin.OUT)
spi_tx = Pin(3, Pin.OUT)
lcd_reset = Pin(0, Pin.OUT)
lcd_dc = Pin(1, Pin.OUT)
lcd_width = 240
lcd_height = 240
spi_lcd = machine.SPI(0, baudrate=80000000, phase=1, polarity=1,
                      sck=spi_sck, mosi=spi_tx)
display = lcd.lcd_config(spi_lcd, width=lcd_width, height=lcd_height,
                         reset=lcd_reset, dc=lcd_dc, rotation=0)

i2c = I2C(0, scl=Pin(17, Pin.OUT), sda=Pin(16, Pin.OUT), freq=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
gc.collect()
while True:
    mlx.getFrame(frame)
    rect_wid = 6
    for h in range(24):
            for w in range(32):
                t = frame[h * 32 + w]
                color = int((t-20)/20*255)
                display.fill_rect(w*rect_wid,h*rect_wid,
                                  rect_wid,rect_wid,
                                  st7789.color565(color,color,color))
