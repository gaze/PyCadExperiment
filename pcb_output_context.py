#!/usr/bin/env python2.7

from context import *

class PCBOutputContext(Context):
    def __init__(self,target_layer):
        Context.__init__(self)
        self.target_layer = target_layer
        self.counter = 0

        self.clearance = 0.001
        self.mask = 0.001
        
    def write_line(self,obj):
        if(self.target_layer != self.active):
            return

        if(obj.args["type"] == "smd"):

            rX1 = int(obj.p1.item(0)*100000.0)
            rY1 = int(obj.p1.item(1)*100000.0)

            rX2 = int(obj.p2.item(0)*100000.0)
            rY2 = int(obj.p2.item(1)*100000.0)

            thickness = int(obj.args["thickness"]*100000.0)

            clearance = int(self.clearance*100000.0)
            mask = int(self.mask*100000.0)

            name = "N%s" % self.counter
            number = "%s" % self.counter
            flags = ""

            print """Pad [%i %i %i %i %i %i %i "%s" "%s" "%s"]""" % (rX1, rY1, rX2, rY2, thickness, clearance, mask, name, number, flags)

            self.counter += 1

        else:
            print "ERROR! Bad pad type"

    def write_arc(self,obj):
        if(self.target_layer != self.active):
            return

        print "Please don't dump arcs in the copper layer."

    def write_point(self,obj):
        if(self.target_layer != self.active):
            return

        if(obj.args["type"] == "hole"):

            rX = int(obj.p.item(0)*100000.0)
            rY = int(obj.p.item(1)*100000.0)

            thickness = int(obj.args["thickness"]*100000.0)
            drill = int(obj.args["drill"]*100000.0)

            clearance = int(self.clearance*100000.0)
            mask = int(self.mask*100000.0)

            name = "N%s" % self.counter
            number = "%s" % self.counter
            flags = ""

            print """Pin [%i %i %i %i %i %i "%s" "%s" "%s"]""" % (rX, rY, thickness, clearance, mask, drill, name, number, flags)

            self.counter += 1
        else:
            print "ERROR! Bad pad type"

    def write_epilogue():

        print """
)


Layer(1 "top")
(
)
Layer(2 "ground")
(
)
Layer(3 "signal2")
(
)
Layer(4 "signal3")
(
)
Layer(5 "power")
(
)
Layer(6 "bottom")
(
)
Layer(7 "outline")
(
)
Layer(8 "spare")
(
)
Layer(9 "silk")
(
)
Layer(10 "silk")
(
)
"""
