import pygame, random, os, sys

from pygame.locals import *

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, hit, score, imgnum):
        pygame.sprite.Sprite.__init__(self)
        
        self.image_number = imgnum
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}' .format(list_img[self.image_number]))
        self.image = pygame.image.load(sys_name).convert()
        
        self.rect = self.image.get_rect()
        self.upgrade = 0
        self.image.set_colorkey((0, 0, 0))
        
        temp_up = random.randint(0,7) # 12.5% Chance of a brick having an upgrade
        
        if temp_up == 3:
            self.upgrade = 1
                    
        self.rect.centerx = x
        self.rect.centery = y
        
        self.hit = hit
        self.score = score
        
    def get_score(self):
        return self.score
    
        
list_img = ['big_tile_1.PNG', 'big_tile_2.PNG', 'big_tile_3.PNG', 'big_tile_4.PNG', 'big_tile_5.PNG', 'SPECIALTILE1.PNG', 'SPECIALTILE2.PNG', 'GOLDTILE.PNG']