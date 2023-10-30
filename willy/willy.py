# willy  - manic miner

from picographics import PicoGraphics, PEN_RGB555
from pimoroni import Button
import pngdec

WIDTH = 400
HEIGHT = 300
display = PicoGraphics(PEN_RGB555, WIDTH, HEIGHT)
 
scale = 1
button_a = display.is_button_a_pressed
button_x = display.is_button_x_pressed
button_y = Button(9, invert=True).read

x = 30
y = 100
xdir = 0
ydir = 1
jumping = 0

# platform = [startx, y, endx]
platforms =  [[0,104,250],[0,57,35],[0,41,30],[0,25,250],[40,90,155],[155,82,240],[227,66,250],[58,58,225],[130,49,155]]
conveyor = [58,58,225]
collapsing = [[113,25,138],[152,25,178],[185,82,225]]

def playerhitplatform (platform):
    px = platform[0] * scale
    py = platform[1] * scale
    pz = platform[2] * scale
    
    if x > px and x < pz :
        if abs(py - y) < 2 : return True
    return False
            
# load in sprites and images
png = pngdec.PNG(display)
png.open_file("/level1.png")
for _ in range(2):
    willy = display.load_animation(0, "/willy.png", (16, 16))
    png.decode(0,0,scale)
    display.update()

collapsed = [0] * 300
while True:
    display.display_sprite(0,0, x,y)
    # clear collapsed platforms
    for p in collapsing:
        for px in range(p[0],p[2]):
             display.rectangle(px,p[1],5,collapsed[px])          
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
                    jumping = 0
                    ydir = 0
                    
    if playerhitplatform(conveyor) : xdir = -1
    for p in collapsing:
        if playerhitplatform(p):
            if collapsed[x] < 20 : collapsed[x] += 5
            else : ydir = 1
        
    if not onplatform : ydir = 1
   
    if jumping :
        jumping -= 1
        if jumping >= 20 : ydir = -1
        else : ydir = 1
    
    x += xdir
    y += ydir
    
    if x < 0 : x = 0
    if x > 240 : x = 240  
