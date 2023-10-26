# stickman walking

import math

from picographics import PicoGraphics, PEN_RGB555
display = PicoGraphics(PEN_RGB555, 400, 300)

GREEN = display.create_pen(0, 200, 0)

WIDTH, HEIGHT = display.get_bounds()

xpos = int(WIDTH / 2)
ypos = int(HEIGHT / 3) 

def drawline(start,end):
    x1 = start[0] + xpos
    y1 = start[1] + ypos
    x2 = end[0] + xpos
    y2 = end[1] + ypos
    display.line(x1,y1,x2,y2)

def add (v1,v2):
    vec = [v1[0] + v2[0], v1[1] + v2[1]]
    return (vec)

def sinangle(angle):
    return int(math.sin(math.radians(angle)) * 30)

def cosangle(angle):
    return int(math.cos(math.radians(angle)) * 30)

def drawground():
    dustx = WIDTH - (i % WIDTH) 
    for dust in range(0,WIDTH,50):
	    display.pixel (int(dustx /2 ) + dust,HEIGHT - 60)
    
i = 0
while True:
    display.set_pen(0)
    display.clear()

    display.set_pen(GREEN)
   
    # Head
    head = 15
    display.circle(xpos,ypos,head)
    display.set_pen(0)
    display.circle(xpos,ypos,head-1)
    
    display.set_pen(GREEN)
    
    # body
    neck = [0,head]
    hip = [0,80]
    drawline(neck,hip)
    
    # arms
    for side in [0,180]:
        a = sinangle(i + side)  
        shoulder = [0, head + 10]
        elbow = [sinangle(a),cosangle(a)]
        elbow = add(shoulder,elbow)
        drawline(shoulder,elbow)
        
        wrist = [sinangle(a+90),cosangle(a+90)]
        wrist = add(elbow,wrist)
        drawline(elbow,wrist)
    
    # legs
    for side in [0,180]:
        a = sinangle(i + side)
        knee = [sinangle(a),cosangle(a)]
        knee = add(hip,knee)
        drawline(hip,knee)
        
        a = sinangle(i + side -45)
        ankle = [sinangle(a-40),cosangle(a-40)]
        ankle = add(knee,ankle)
        drawline(knee,ankle)
        
    # loop
    i = i + 3
    
    drawground()
    display.update()

