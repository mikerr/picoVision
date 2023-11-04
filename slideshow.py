# slideshow
from picographics import PicoGraphics, PEN_RGB555
from pimoroni import Button
import pngdec
import time,os

from machine import Pin, SPI
import sdcard
# needs sdcard.py from https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/storage/sdcard/sdcard.py

WIDTH = 400
HEIGHT = 300
display = PicoGraphics(PEN_RGB555, WIDTH, HEIGHT)

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

png = pngdec.PNG(display)       
pngs = []

# set up the SD card
sd_spi = SPI(1, sck=Pin(10, Pin.OUT), mosi=Pin(11, Pin.OUT), miso=Pin(12, Pin.OUT))

try:
    sd = sdcard.SDCard(sd_spi, Pin(15))
    os.mount(sd, "/sd")
    
    files = os.listdir('/sd')
    for file in files:
        if file.endswith(".png") :
            pngs.append("/sd/" + file)
except:
    print ("No sd")

files = os.listdir('/')
for file in files:
    if file.endswith(".png") :
        pngs.append(file)

while True:
    for imagefile in pngs :
        print(imagefile)
        try:
            png.open_file(imagefile)
        except:
            continue
        scalew = WIDTH // png.get_width()
        scaleh = HEIGHT // png.get_height()
        scale = min(scalew,scaleh)
        
        for _ in range(2):            
            display.set_pen(BLACK)
            display.clear()
            png.decode(0,0,scale)
            
            display.set_pen(WHITE)
            display.text(imagefile,20,HEIGHT - 20)
            display.update()
        time.sleep(1)
