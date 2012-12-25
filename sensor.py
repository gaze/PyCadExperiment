#!/usr/bin/env python2.7

from preview_context import *
from pcb_output_context import *
from dxf_output_context import *

import diode
import led

led_down = 0.09

paddle_width = 0.19

deflection = 2*pi/360.0 * 18

active_area_utilization = 1

mounting_hole_dia = 0.089
mounting_hole_spacing = 0.9


def normalize(n):
    return n/(sqrt(dot(n,n.T)))

def argof(n):
    x = n.item(0)
    y = n.item(1)
    return arctan2(y,x)

def construct(c):

    x = paddle_width/2*cos(deflection)
    y = paddle_width/2*sin(deflection)

    c.write(Line(c, matrix([x,y]),matrix([-x,-y])))
    c.write(Line(c, matrix([-x,y]),matrix([x,-y])))

    emitter = matrix([0,led_down])
    high_p = normalize(matrix([-x,-y])-emitter)
    low_p  = normalize(matrix([-x,y])-emitter)

    sep_angle = abs(argof(high_p)-argof(low_p))
    distance = (0.5*diode.active_area_width*active_area_utilization)/tan(sep_angle/2)

    mid_p = normalize(high_p+low_p)*distance
    high_p = high_p*distance
    low_p = low_p*distance

    print sqrt(dot(high_p-low_p,(high_p-low_p).T))

    llight = {}
    rlight = {}
    ld = {}
    rd = {}

    for a in [0,pi]:
        c.rotate(a)
        c.translate(0,led_down)

        c.set_layer("optical")

        if a == 0:
            c.write(Line(c, 0, low_p))
            c.write(Line(c, 0, high_p))
            c.write(Line(c, 0, mid_p))

        ld[a] = {}
        rd[a] = {}

        for side in ["left", "right"]:
            if side == "right":
                c.reflecth()

            c.rotate(argof(mid_p)-pi/2)
            c.translate(0,distance)
            
            (ld[a][side],rd[a][side]) = diode.construct(c)

            c.pop()
            c.pop()

            if side == "right":
                c.pop()

        (llight[a],rlight[a]) = led.construct(c,20.0/360.0*2*pi)

        c.pop()
        c.pop()

    c.set_layer("guard_outline");

    # LED cage to Diode Cage
    c.write(Line(None,ld[0]["right"].p,llight[pi].p))
    c.write(Line(None,ld[0]["left"].p,rlight[pi].p))

    c.write(Line(None,ld[pi]["right"].p,llight[0].p))
    c.write(Line(None,ld[pi]["left"].p,rlight[0].p))

    # Diode cage to diode cage
    c.write(Line(None,rd[pi]["left"].p,rd[0]["right"].p))
    c.write(Line(None,rd[0]["left"].p,rd[pi]["right"].p))


    c.set_layer("copper_pads");
    c.write(Point(c,matrix([-mounting_hole_spacing/2,0]),type="hole",drill=mounting_hole_dia,thickness=0))
    c.write(Point(c,matrix([mounting_hole_spacing/2,0]),type="hole",drill=mounting_hole_dia,thickness=0))

    c.set_layer("guard_outline");
    c.write(Point(c,matrix([-mounting_hole_spacing/2,0]),type="hole",drill=mounting_hole_dia,thickness=0))
    c.write(Point(c,matrix([mounting_hole_spacing/2,0]),type="hole",drill=mounting_hole_dia,thickness=0))

if __name__ == "__main__":
    c = PCBOutputContext("copper_pads")
    construct(c)
    
    c = DXFOutputContext("guard_outline")
    construct(c)
    c.save("guard.dxf")

#    c = PreviewContext(4,4,168.0)
    c = PreviewContext(2,2,400)

    c.set_layer("copper_pads")
    c.set_layer_prop("color",MAGENTA)

    c.set_layer("part_outline")
    c.set_layer_prop("color",WHITE)

    c.set_layer("guard_outline")
    c.set_layer_prop("color",CYAN)

    c.set_layer("optical")
    c.set_layer_prop("color",YELLOW)

    construct(c)

    c.show()
