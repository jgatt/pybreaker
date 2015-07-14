import pygame, os, sys, random

from pygame.locals import *

class Upgrade(pygame.sprite.Sprite):
    
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)

        self.number_upgrade = random.randint(0, 5)
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}' .format(list_img[self.number_upgrade]))
        self.image = pygame.image.load(sys_name).convert()

        sys_name = os.path.join(sys.path[0], 'Pybreaker-sounds', '{0}' .format(list_sound[self.number_upgrade]))
        self.sound = pygame.mixer.Sound(sys_name)
        
        self.rect = self.image.get_rect()
        
        self.rect.centerx = center_x
        self.rect.centery = center_y
        
        self.image.set_colorkey((0, 255, 0))
        
        self.dy = 5
        
        self.count = 0
        
        
    def update(self):
        self.rect.centery += self.dy
        self.count += 1
        
        if self.count > 10:
            self.count = 0
        elif self.count < 5:
            self.rect.centerx += 3
        elif self.count > 5:
            self.rect.centerx -= 3
        
           
list_img = ['LASERPOWER.png', 'GROWPADDLE.png', 'SHRINKPADDLE.png', 'MULTIBALL.png', '1UP.png', 'STICKY.png']
list_sound = ['LASERMESSAGE.ogg', 'SUPERPADDLE.ogg', 'SHRINKPADDLE.ogg', 'MULTIBALL.ogg', '1UP.ogg', 'STICKYBALL.ogg']