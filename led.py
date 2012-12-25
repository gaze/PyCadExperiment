#!/usr/bin/env python2.7

from preview_context import *

width = 0.155
height = 0.146

diode_depth = 0.03

pad_width = 0.046
pad_height = 0.113

h_slew_space = 0.02

# We let the vertical take up the roundness of the endmill.
v_slew_space = 0.0625

cage_width = width+2*h_slew_space
cage_height = height+v_slew_space

pad_thickness = pad_width
pad_length = pad_height-pad_thickness

def write_pad(c,centerpoint):
    os = matrix([0, pad_length/2])
    p1 = centerpoint - os
    p2 = centerpoint + os

    c.write(Line(c,p1,p2,type="smd",thickness=pad_thickness))

def construct(c,guard_angle):
    c.translate(0,-diode_depth)

    c.set_layer("part_outline")

    c.rect((-width/2,0),(width/2,height))

    c.set_layer("copper_pads")

    write_pad(c, matrix([-width/2+pad_width/2,height-pad_height/2]))
    write_pad(c, matrix([ width/2-pad_width/2,height-pad_height/2]))

    c.set_layer("optical")

    c.write(Point(c,matrix([0,diode_depth])))

    c.set_layer("guard_outline")

    guard_up = diode_depth-(sin(guard_angle)*cage_width/2)

    left_point = matrix([-cage_width/2, guard_up])
    right_point = matrix([cage_width/2, guard_up])

    for (p1,p2) in [
        (matrix([-cage_width/2,cage_height]),matrix([cage_width/2,cage_height])),
        (left_point,matrix([-cage_width/2,cage_height])),
        (right_point,matrix([cage_width/2,cage_height]))]:
        c.write(Line(c,p1,p2))

    ret = (Point(c,left_point),Point(c,right_point))

    c.pop()

    #Draw the LED's light cone

    """
    c.set_layer("optical")
    len = 0.2
    extinction_angle = 80.0/360.0*2*pi
    x = len*sin(extinction_angle)
    y = -len*cos(extinction_angle)
    
    c.write(Line(c,matrix([0,0]),matrix([x,y])))
    c.write(Line(c,matrix([0,0]),matrix([-x,y])))"""

    return ret


if __name__ == "__main__":
    c = PreviewContext(1,1,168.0)

    c.set_layer("copper_pads")
    c.set_layer_prop("color",YELLOW)

    c.set_layer("part_outline")
    c.set_layer_prop("color",WHITE)

    c.set_layer("guard_outline")
    c.set_layer_prop("color",CYAN)

    c.set_layer("optical")
    c.set_layer_prop("color",MAGENTA)


    construct(c,0)

    c.show()
