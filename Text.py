import pygame, os, sys

from pygame.locals import *

class Text(pygame.sprite.Sprite):
    
    def __init__(self, x, y, message, RGBtupple, font):
        pygame.sprite.Sprite.__init__(self)
        
        self.message = message
        self.font = font
        self.anti = True
        self.RGBtupple = RGBtupple
        self.image = self.font.render(self.message, self.anti, self.RGBtupple).convert_alpha()
        
        self.rect = self.image.get_rect()
        
        self.rect.left = x
        self.rect.top = y
    
    def update(self):
        temp_x = self.rect.left
        temp_y = self.rect.top
        
        self.image = self.font.render(self.message, self.anti, self.RGBtupple).convert_alpha()
    
        self.rect = self.image.get_rect()
        
        self.rect.left = temp_x
        self.rect.top = temp_y