# willy  - manic miner

from picographics import PicoGraphics, PEN_RGB555
from pimoroni import Button
import pngdec
from random import randrange as rnd

WIDTH = 400
HEIGHT = 300
display = PicoGraphics(PEN_RGB555, WIDTH, HEIGHT)
 
scale = 1
button_a = display.is_button_a_pressed
button_x = display.is_button_x_pressed
button_y = Button(9, invert=True).read

x = 10
y = 90
xdir = ydir = jumping = 0

# platform = [startx, y, endx]
platforms =  [[0,104,250],[0,57,40],[0,41,30],[0,25,250],[40,90,155],[155,82,250],[227,66,250],[58,58,225],[130,49,155]]
conveyor = [58,58,225]
collapsing = [[113,25,138],[152,25,178],[185,82,225]]
monstermove = [58,58,130]

gems = [[240,50],[240,3],[80,3],[130,12],[200,30]]
spikes = [[96,90],[170,60],[188,30],[218,30]]

def playerhit (obj) :
    return (abs(x - obj[0]) < 8 and abs(y - obj[1]) < 8 )               
    
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
    willy = display.load_animation(0, "/characters.png", (16, 16), source=(0, 0, 128, 16))
    monster = display.load_animation(1, "/characters.png", (16, 16), source=(128, 0, 16, 16))
    png.decode(0,0,scale)
    display.update()

mx = monstermove[0]
my = monstermove[1]
mdir = 1

collapsed = [0] * 300
collectedgems =[]

while True:
    display.display_sprite(0,0, x,y,1,scale)
    display.display_sprite(1,1, mx,my,1,scale)
    
    for gem in gems:     
        if gem in collectedgems : color = display.create_pen(0,0,0)
        else :
            if playerhit(gem) : collectedgems.append(gem)
            color = display.create_pen(rnd(255),rnd(255),rnd(255))
        display.set_pen(color)    
        display.circle(gem[0],gem[1],3)
    
    mx += mdir
    if mx < monstermove[0] or mx > monstermove[2] : mdir *= -1 
    if playerhit([mx,my]) : x = 20 ; y = 90
        
    for spike in spikes:
        color = display.create_pen(rnd(255),rnd(255),rnd(255))
        display.set_pen(color)
        #display.circle(spike[0],spike[1],4)
        if playerhit(spike) :
            x = 20; y = 90
    
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
                    
    for p in collapsing:
        for px in range(p[0],p[2]):
             display.set_pen(0)
             display.rectangle(px,p[1],5,collapsed[px])
        if playerhitplatform(p):
            if collapsed[x] < 20 : collapsed[x] += 5
            else : ydir = 1
             
    if playerhitplatform(conveyor) : xdir = -1
    
    if not onplatform : ydir = 1
   
    if jumping :
        jumping -= 1
        if jumping >= 20 : ydir = -1
        else : ydir = 1
    
    x += xdir
    y += ydir
    
    if x < 8 : x = 8
    if x > 240 : x = 240
    
    display.update()
