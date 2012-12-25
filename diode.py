#!/usr/bin/env python2.7

from preview_context import *

width = 0.190
height = 0.150

wire_spacing = 0.1

active_area_width = 0.118

wires_off_top = 0.06

slew_space = 0.02

cage_width = width+2*slew_space
cage_height = height+slew_space

hole_dia=0.028
pad_dia=0.06

def construct(c):

    # The wafer is RIGHT above the wires.
    c.translate(0, - wires_off_top)

    c.set_layer("part_outline")

    c.rect((-width/2,0),(width/2,height))

    c.set_layer("copper_pads")

    c.write(Point(c,matrix([ wire_spacing/2,wires_off_top]),type="hole",drill=hole_dia,thickness=pad_dia))
    c.write(Point(c,matrix([-wire_spacing/2,wires_off_top]),type="hole",drill=hole_dia,thickness=pad_dia))

    c.set_layer("guard_outline")

    left_point = matrix([-cage_width/2, 0])
    right_point = matrix([cage_width/2, 0])

    for (p1,p2) in [
        (matrix([-cage_width/2,cage_height]),matrix([cage_width/2,cage_height])),
        (left_point,matrix([-cage_width/2,cage_height])),
        (right_point,matrix([cage_width/2,cage_height]))]:
        c.write(Line(c,p1,p2))

    ret = (Point(c,left_point),Point(c,right_point))

    c.set_layer("optical")
    c.write(Line(c, matrix([-active_area_width/2,wires_off_top]), matrix([active_area_width/2, wires_off_top])))

    c.pop()

    return ret


if __name__ == "__main__":
    c = PreviewContext(1,1,168.0)

    c.set_layer("copper_pads")
    c.set_layer_prop("color",RED)

    c.set_layer("part_outline")
    c.set_layer_prop("color",WHITE)

    c.set_layer("guard_outline")
    c.set_layer_prop("color",CYAN)

    c.set_layer("optical")
    c.set_layer_prop("color",MAGENTA)

    construct(c)

    c.show()
