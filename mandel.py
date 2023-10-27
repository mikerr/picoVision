# mandelbrot fractal

import time
import math
from pimoroni import Button

from picographics import PicoGraphics, PEN_RGB555
display = PicoGraphics(PEN_RGB555, 400, 300)

WIDTH, HEIGHT = display.get_bounds()

def mandel(i,res) :
    max_iter = 255  // res
    y = (i - HEIGHT/2) * scale + cy;
    for j in range (0,WIDTH, res):
        x = (j - WIDTH/2) * scale + cx;
        xs = (x - 0.25)
        zx = math.sqrt(xs * xs + y * y)
        if (x < zx - 2 * zx * zx + 0.25) : continue
        if ((x + 1)*(x + 1) + y * y < 1/16) : continue

        zx = zy = zx2 = zy2 = 0
        iter = 0
        for n in range (max_iter -1):
            iter = n
            zy = 2 * zx * zy + y
            zx = zx2 - zy2 + x
            zx2 = zx * zx
            zy2 = zy * zy
            if (zx2 + zy2 > 4) : break
            
            if (iter < max_iter):
                c = iter * res
                colorpixel(j,i,c)
             
def colorpixel(x,y,c):
    if invertcolors : c = 256- clr [c]
    r = c
    g = b = 0
    color = display.create_pen(r, g, b )
    display.set_pen(color)
    if (res > 1) : display.rectangle(x,y,res,res)
    else : display.pixel(x,y)

scale = 1./128
cx = -.6
cy = 0
invertcolors = 1

clr=[int(255*((i/255)**12)) for i in range(255,-1,-1)]

while True:
    res = 8
    i = 0
    while res >= 1 :
        # repeat once for each buffer to kill flicker
        for r in range(2):
            #scrub previous scanline
            display.set_pen(0)
            display.rectangle(0,i,WIDTH,res)
        
            mandel(i,res)
            display.update()
            
        if i == 0: t_start = time.ticks_ms()
        i += res
        if i > HEIGHT :
            i = 0  
            t_end = time.ticks_ms()
            print(f"resolution {res} in {t_end - t_start} ms")
            res = res // 2
        
        if display.is_button_a_pressed() :
            invertcolors = not invertcolors
            break
        if display.is_button_x_pressed() :
            scale = scale * 0.9
            break
        button_y = Button(9, invert=True).read
        if button_y() :
            scale = scale * 1.1
            break
