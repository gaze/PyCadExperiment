#!/usr/bin/env python2.7

import sdxf

from context import *

class DXFOutputContext(Context):
    def __init__(self,target_layer):
        Context.__init__(self)
        self.target_layer = target_layer
        self.d = sdxf.Drawing()
        
    def write_line(self,obj):
        if(self.target_layer != self.active):
            return

        p1 = (obj.p1.item(0),obj.p1.item(1))
        p2 = (obj.p2.item(0),obj.p2.item(1))

        self.d.append(sdxf.Line(points=[p1,p2], layer="work"))

    def write_arc(self,obj):

        print "Arcs unsupported"

    def write_point(self,obj):
        if(self.target_layer != self.active):
            return

        p = (obj.p.item(0),obj.p.item(1))

        self.d.append(sdxf.Line(points=[p], layer="work"))


    def save(self, name):
        self.d.saveas(name)
        
