# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:15:10 2026

@author: quinn
"""

import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES) #rendering set resolution
        self.clock = pg.time.Clock() #for framerate
        self.delta_time = 1
        self.new_game()
        
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
    
    def update(self):
        self.player.update()
        self.raycasting.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}') #display FPS
        
    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        #self.map.draw() #early tests
        #self.player.draw() #early tests
        
    def check_events(self): #event handler
        for event in pg.event.get(): #quitting the game
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
        
    def run(self): #main loop of game
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run() 
           