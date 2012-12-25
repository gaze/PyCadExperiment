#!/usr/bin/env python2.7

from preview_context import *

c = PreviewContext(5.0,5.0,96.0)
c.set_layer("top_board_layer")
c.set_layer_prop("color",BLUE)

c.translate(1,1)
for ang in [0,pi/2,pi,3*pi/2]:
    c.rotate(ang)
    c.write(Point(c, matrix([0.1,0.1])))
    c.pop()

c.show()
