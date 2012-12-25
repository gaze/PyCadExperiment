#!/usr/bin/env python2.7

from context import *

import pygame

BLACK = ( 0 , 0 , 0 )
RED   = ( 255 , 0 , 0 )
GREEN = ( 0 , 255 , 0 )
BLUE  = ( 0 , 0 , 255 )
CYAN = ( 0, 255, 255 )
MAGENTA = ( 255 , 0, 255 )
YELLOW = ( 255, 255, 0 )
WHITE = ( 255, 255, 255 )

DARK_GREY = ( 50, 50, 50 )
VERY_DARK_GREY = ( 25, 25, 25 )


class PreviewContext(Context):
    def __init__(self,w,h,ppi):
        Context.__init__(self)
        
        pygame.init()

        size=[int(w*ppi),int(h*ppi)]

        # This will send us to on screen coordinates
        self.mstack.append(
            matrix([
                    [float(ppi),0,float(ppi)*float(w)/2.0],
                    [0,float(ppi),float(ppi)*float(h)/2.0],
                    [0,0,1]
                    ]))

        self.screen=pygame.display.set_mode(size)
        self.screen.fill(BLACK)

        pygame.display.set_caption("Preview")

        pygame.draw.line(self.screen,DARK_GREY,(w*ppi/2,0),(w*ppi/2,h*ppi))
        pygame.draw.line(self.screen,DARK_GREY,(0,h*ppi/2),(w*ppi,h*ppi/2))

    
    def show(self):
        clock = pygame.time.Clock()

        done=False

        while done==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True

            pygame.display.flip()

            clock.tick(20)

        print "Goodbye!"

        pygame.quit()

    def get_color(self):
        try:
            return self.get_layer_prop("color")
        except KeyError:
            return WHITE

    def write_line(self,obj):
        p1 = (obj.p1.item(0),obj.p1.item(1))
        p2 = (obj.p2.item(0),obj.p2.item(1))

        pygame.draw.line(self.screen,self.get_color(),p1,p2)

    def write_arc(self,obj):
        print "writing an arc!!111"

    def write_point(self,obj):
        POINTCROSSPX=3

        x = obj.p.item(0)
        y = obj.p.item(1)

        pygame.draw.line(self.screen,self.get_color(),(x-POINTCROSSPX,y),(x+POINTCROSSPX,y))
        pygame.draw.line(self.screen,self.get_color(),(x,y-POINTCROSSPX),(x,y+POINTCROSSPX))
