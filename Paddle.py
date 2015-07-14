import pygame, random, os, sys

from pygame.locals import *

class Paddle(pygame.sprite.Sprite):
    "Models a Paddle object that is the players main control outlet"
    def __init__(self, lives, score):
        pygame.sprite.Sprite.__init__(self)
        
        self.paddle_size = 0
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}'.format(image_list[self.paddle_size]))
        self.image = pygame.image.load(sys_name).convert()
        
        self.rect = self.image.get_rect()
        
        self.image.set_colorkey((0, 255, 0))
        self.rect.centery = 580
        self.rect.centerx = 400
        self.dx = 0
        
        self.score = score
        self.lives = lives
        self.laser_amount = 0
        
        #STICKYSTATE WHERE TRUE = STICKY STATE, FALSE = NORMAL STATE
        self.STICKY = False
               
    def update(self):
        self.rect.centerx += self.dx
        
        if self.rect.right > 800:
            self.dx = 0
        elif self.rect.left < 0:
            self.dx = 0
            
        self.dx = 0 
        
    def move_paddle(self, dx):
        self.dx = dx
        
    def get_score(self):
        return self.score
    
    def get_laser_amount(self):
        return self.laser_amount
    
    def add_score(self, new_score):
        self.score += new_score
    
    def SUPERPADDLE(self): 
        "'Grow's' the paddle"
        temp_x = self.rect.centerx
        temp_y = self.rect.centery
        
        if self.paddle_size == 0:
            self.paddle_size = 1
        elif self.paddle_size == 1:
            self.paddle_size = 2
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}'.format(image_list[self.paddle_size]))    
        self.image = pygame.image.load(sys_name).convert()
        
        self.rect = self.image.get_rect()
    
        self.image.set_colorkey((0, 255, 0))
        
        self.rect.centery = temp_y
        self.rect.centerx = temp_x
        
    def LASER(self):
        "Start's the laser creation process, now when a user enter's SPACE a laser is spawned"
        self.laser_amount += 25
        
    def SHRINKPADDLE(self):
        "Shrinks the paddle"
        temp_x = self.rect.centerx
        temp_y = self.rect.centery
        
        self.paddle_size = -1
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}'.format(image_list[self.paddle_size]))    
        self.image = pygame.image.load(sys_name).convert()
        
        self.rect = self.image.get_rect()
    
        self.image.set_colorkey((0, 255, 0))
        
        self.rect.centery = temp_y
        self.rect.centerx = temp_x
        
    def DOWNGRADE(self):
        "'Downgrades' the padded, by returning it to it's original form"
        temp_x = self.rect.centerx
        temp_y = self.rect.centery
        
        self.paddle_size = 0
        
        sys_name = os.path.join(sys.path[0], 'Pybreaker-images', '{0}'.format(image_list[self.paddle_size]))    
        self.image = pygame.image.load(sys_name).convert()
        
        self.rect = self.image.get_rect()
    
        self.image.set_colorkey((0, 255, 0))
        
        self.rect.centery = temp_y
        self.rect.centerx = temp_x
        
    def LIFEUP(self):
        "Add's a life to the player"
        self.lives += 1
        
    def STICKYSTATE(self):
        "Set's the paddle's sticky status to 'True' which forces the ball to 'stick' to the paddle"
        self.STICKY = True
        
image_list = ['big_paddle_2.PNG', 'UPGRADEPADDLE1.PNG', 'UPGRADEPADDLE2.PNG', 'DOWNGRADEPADDLE.PNG']