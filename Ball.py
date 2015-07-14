import pygame, random, os, sys

from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, rect_centerx, rect_centery):
        pygame.sprite.Sprite.__init__(self)
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'big_ball.PNG')
        self.image = pygame.image.load(sys_name).convert()

        rand_sound = random.randint(0,2)
        sys_name = os.path.join(sys.path[0], 'Pybreaker-sounds', '{0}' .format(sound_list[rand_sound]))
        self.bounce = pygame.mixer.Sound(sys_name)
        
        self.rect = self.image.get_rect()
        
        self.image.set_colorkey((255, 0, 0))
        
        self.rect.centerx = rect_centerx
        self.rect.centery = rect_centery
        #SPAWN STATE FOR INITIAL BALL/WHEN THE BALL 'DIES'; 'TRUE' == 'DEAD' False == 'ALIVE'
        self.SPAWNSTATE = False
        self.dx = 0
        self.dy = 0
        
    def update(self):

        self.rect.centerx += self.dx
        self.rect.centery += self.dy
    
        if self.rect.top < 0:
            self.bounce.play()
            self.rect.top = 0
            self.dy *= -1
        elif self.rect.right > (800.0):
            self.bounce.play()
            self.rect.right = 800
            self.dx *= -1
        elif self.rect.left < 0:
            self.bounce.play()
            self.rect.left = 0
            self.dx *= -1
               
    def collision(self):
        self.dy *= -1
        
    def SPAWNSPEEDS(self):
        self.dx = 6
        self.dy = -6
                          
sound_list = ['bounce1.ogg', 'bounce2.ogg', 'bounce3.ogg']