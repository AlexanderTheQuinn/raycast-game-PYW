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
        try:
            self.floor_image = self.get_texture('resources/textures/floor.jpg', (WIDTH, HALF_HEIGHT))
        except:
            # Fallback if floor image doesn't exist
            self.floor_image = pg.Surface((WIDTH, HALF_HEIGHT))
            self.floor_image.fill((100, 150, 100))
        self.sky_offset = 0
        self.floor_offset = 0
        
    def draw(self):
        self.draw_background()
        self.render_game_objects()

        
    def draw_background(self):
        # Sky horizontal offset (left-right mouse movement)
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel_x) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        
        # Floor vertical offset (up-down mouse movement)
        self.floor_offset = (self.floor_offset + 4.5 * self.game.player.rel_y) % HALF_HEIGHT
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT + self.floor_offset))
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT + self.floor_offset - HALF_HEIGHT))
        
    def render_game_objects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)
        
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/2rockwall.png'),
            }
