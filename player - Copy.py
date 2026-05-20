# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:36:30 2026

@author: quinn
"""

from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.pitch = 0
        
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos
        
        self.check_wall_collision(dx, dy)
        
        #player movement with keys
        #if keys[pg.K_LEFT]:
            #self.angle -= PLAYER_ROTATION_SPEED * self.game.delta_time
        #if keys[pg.K_RIGHT]:
            #self.angle += PLAYER_ROTATION_SPEED * self.game.delta_time
        self.angle %= math.tau # tau = 2*pi
        
    def check_wall(self, x, y):
        return(x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy): #only allow movement if there is no wall
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
             self.y += dy
        
    def draw(self):
        #direction player's movement
        #pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     #(self.x * 100 + WIDTH * math.cos(self.angle),
                      #self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)
        
    def mouse_control(self): #retrieve mouse coordinates, check if within bounds, if not set cursor to middle
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < MOUSE_BORDER_BOTTOM or my > MOUSE_BORDER_TOP:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
    # Horizontal mouse movement (left-right rotation)
        self.rel_x = pg.mouse.get_rel()[0]
        self.rel_x = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel_x))
        self.angle += self.rel_x * MOUSE_SENSITIVITY * self.game.delta_time
        
        # Vertical mouse movement (up-down look, only downward)
        self.rel_y = pg.mouse.get_rel()[1]
        self.rel_y = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel_y))
        
        # Only allow downward movement (positive rel_y)
        if self.rel_y > 0:  # Only process downward movement
            self.pitch += self.rel_y * MOUSE_SENSITIVITY * self.game.delta_time
            # Clamp pitch to prevent looking too far down
            self.pitch = min(self.pitch, HALF_FOV)
        
    def update(self): 
        self.movement() #calling movement method from update method
        self.mouse_control()
        
    @property #for convenience: returns players coordinates
    def pos(self):
        return self.x, self.y
    
    @property #know which map tile we are on
    def map_pos(self):
        return int(self.x), int(self.y)