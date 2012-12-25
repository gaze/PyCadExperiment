#!/usr/bin/env python2.7

from numpy import *

class Point:
    def __init__(self,c,p,**args):
        if c == None:
            self.p = p
        else:
            self.p = c.transform_point(p)

        self.args = args

    def __radd__(self,other):
        P = self.p+other.p
        return Point(None,P)

    def __rsub__(self,other):
        P = self.p-other.p
        return Point(None,P)

    def get_type(self):
        return "point"

    def __str__(self):
        return "<point: %s>" % self.p

class Line:
    def __init__(self,c,p1,p2,**args):
        if c == None:
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = c.transform_point(p1)
            self.p2 = c.transform_point(p2)

        self.args = args

    def get_type(self):
        return "line"

class Arc:
    def __init__(self,c,p1,p2,r,direction):
        self.p1 = c.transform_point(p1)
        self.p2 = c.transform_point(p2)
        self.r = r

        if c.get_mirrored():
            if direction=="ccw":
                direction="cw"
            else:
                direction="ccw"
        
        self.direction = direction

    def getType(self):
        return "arc"

class Context(object):
    def __init__(self):
        self.mstack = []
        self.layers = {}
        self.active = "<none>"
    
    def translate(self,x,y):
        self.mstack.append(
            matrix([
                [1, 0, x],
                [0, 1, y],
                [0, 0, 1]
                ])
            )

    def rotate(self,theta):
        self.mstack.append(
            matrix([
                [cos(theta), -sin(theta), 0],
                [sin(theta), cos(theta),  0],
                [0, 0, 1]
                ])
            )

    def reflecth(self):
        self.mstack.append(
            matrix([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
                ])
            )

    def reflectv(self):
        self.mstack.append(
            matrix([
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
                ])
            )

    def pop(self):
        self.mstack = self.mstack[:-1]

    def get_flat_mtx(self):
        mtx = matrix([[1,0,0],[0,1,0],[0,0,1]])

        for m in self.mstack:
            mtx = mtx*m

        return mtx

    def get_mirrored(self):
        d = det(self.get_flat_mtx())
        
        return (d < 0)

    def transform_point(self,inp):
        mtx = self.get_flat_mtx()

        pt = resize(inp,(3,1))
        pt[2][0]=1

        pt = mtx*pt
        pt = pt/pt[2][0]

        return resize(pt, (1,2))


    def write_point(self,obj):
        pass

    def write_line(self,obj):
        pass

    def write_arc(self,obj):
        pass

    def write(self,obj):
        if obj.get_type() == "point":
            self.write_point(obj)
        if obj.get_type() == "line":
            self.write_line(obj)
        if obj.get_type() == "arc":
            self.write_arc(obj)

    def rect(self,p1,p2):
        x1,y1 = p1
        x2,y2 = p2

        for (p1,p2) in [
            (matrix([x1,y1]),matrix([x1,y2])),
            (matrix([x1,y2]),matrix([x2,y2])),
            (matrix([x2,y2]),matrix([x2,y1])),
            (matrix([x2,y1]),matrix([x1,y1]))]:
            self.write_line(Line(self,p1,p2))
        

    def set_layer(self,layer):
        self.active = layer

    def set_layer_prop(self,prop,value):
        try:
            self.layers[self.active][prop] = value
        except KeyError:
            self.layers[self.active] = {}
            self.layers[self.active][prop] = value

    def get_layer_prop(self,prop):
        return self.layers[self.active][prop]
