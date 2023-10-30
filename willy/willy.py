# willy  - manic miner

from picographics import PicoGraphics, PEN_RGB555
from pimoroni import Button
import time
import pngdec

WIDTH = 400
HEIGHT = 300
display = PicoGraphics(PEN_RGB555, WIDTH, HEIGHT)
    
button_a = display.is_button_a_pressed
button_x = display.is_button_x_pressed
button_y = Button(9, invert=True).read

x = 15
y = 100
xdir = 0
ydir = 1
landed = jumping = 0

platforms =  [[0,104,250],[0,57,35],[0,41,30],[0,25,250],[40,90,155],[155,82,240],[227,66,250],[58,58,225],[130,49,155]]
conveyor = [58,58,225]

def playerhitplatform (platform):
    px = platform[0]
    py = platform[1]
    pz = platform[2]
    
    if x > px and x < pz :
        if abs(py - y) < 2 : return True
    return False
            
# load in sprites and images
png = pngdec.PNG(display)
png.open_file("/level1.png")
for _ in range(2):
    willy = display.load_animation(0, "/willy.png", (16, 16))
    png.decode(0,0)
    display.update()

while True:
    start_time = time.ticks_ms()
    display.display_sprite(0,0, x,y)
    display.update()
    
    xdir = 0 # no inertia
    if button_a() : xdir = -1
    if button_x() : xdir = 1
    if button_y() :
        if ydir == 0 and not jumping : jumping = 40
    
    onplatform = 0
    for p in platforms :
            if playerhitplatform(p) :
                onplatform = 1
                # only fall onto platforms
                if ydir == 1 :
                    landed = 1
                    jumping = 0
                    ydir = 0
    #print(x,y)
    if playerhitplatform(conveyor) : xdir = -1
    if not onplatform : ydir = 1
   
    if jumping :
        jumping -= 1
        if jumping >= 20 : ydir = -1
        else : ydir = 1
    
    x += xdir
    y += ydir
    
    # lock frame rate to 50fps ( 20ms)
    while True:
        ftime = time.ticks_ms() - start_time
        if ftime >= 20 : break
    #print (f"{ ftime } ms { 1000 // ftime } fps") 
