import pygame, os, sys

from pygame.locals import *

class Laser(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'laser.PNG')
        self.image = pygame.image.load(sys_name).convert()

        self.rect = self.image.get_rect()
        self.dy = 0
        self.rect.centerx = x
        self.rect.centery = y
        
    def update(self):
        self.rect.centery += self.dy
    
    def shoot(self, paddle):
        self.dy = -25
        paddle.laser_amount -= 1