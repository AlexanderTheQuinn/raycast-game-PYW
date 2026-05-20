# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:59:50 2026

@author: quinn
"""

import pygame as pg
from settings import *
import math


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky3.png', (WIDTH, HALF_HEIGHT))
        self.floor_image = self.get_texture('resources/textures/floor.jpg', (WIDTH, HALF_HEIGHT) )
        #self.floor_texture = self.get_texture('resources/textures/ground.png')
        self.sky_offset = 0
        self.floor_offset = 0
        
    def draw(self):
        self.draw_background()
        #self.draw_floor()
        self.render_game_objects()

        
    def draw_background(self): #calculate offset depending relative mouse movement
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel_x) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        #floor
        #pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
        self.floor_offset = (self.floor_offset + 4.5 * self.game.player.rel_y) % HALF_HEIGHT
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT + self.floor_offset))
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT + self.floor_offset - HALF_HEIGHT))
        
    def render_game_objects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
        
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha() #loads texture and returns scaled image
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/2rockwall.png'),
            #2: self.get_texture('resources/textures/ground.png') #does not work
            }

#test
"""                  
    def draw_floor(self):
        #Draw textured floor using surface buffer for better performance
        ox, oy = self.game.player.pos
    
        # Create a surface for just this frame's floor
        floor_surface = pg.Surface((WIDTH, HALF_HEIGHT))
        
        for y in range(HALF_HEIGHT, HEIGHT):
            screen_y = y - HALF_HEIGHT
            
            # Distance to floor row
            ratio = SCREEN_DIST / (2 * screen_y + 0.0001)
            
            # Stop calculating floor if it goes beyond a reasonable distance
            if ratio > MAX_DEPTH:
                continue
            
            # Create a scanline (horizontal line) for this row
            scanline = pg.Surface((WIDTH, 1))
            
            for ray in range(NUM_RAYS):
                # Calculate ray angle for this column
                ray_angle = self.game.player.angle - HALF_FOV + (ray * DELTA_ANGLE)
                
                # Get world coordinates on floor
                x_map = ox + ratio * math.cos(ray_angle)
                y_map = oy + ratio * math.sin(ray_angle)
                
                # Calculate texture coordinates
                tex_x = int((x_map * TEXTURE_SIZE) % TEXTURE_SIZE)
                tex_y = int((y_map * TEXTURE_SIZE) % TEXTURE_SIZE)
                
                # Clamp to valid texture range
                tex_x = tex_x % TEXTURE_SIZE
                tex_y = tex_y % TEXTURE_SIZE
                
                # Get pixel color from floor texture
                color = self.floor_texture.get_at((tex_x, tex_y))
                
                # Draw this ray's column on the scanline
                pg.draw.line(scanline, color, (ray * SCALE, 0), (ray * SCALE + SCALE, 0), SCALE)
            
            # Blit the scanline to the floor surface
            floor_surface.blit(scanline, (0, screen_y))
        
        # Blit the entire floor surface to the main screen
        self.screen.blit(floor_surface, (0, HALF_HEIGHT))
        """
