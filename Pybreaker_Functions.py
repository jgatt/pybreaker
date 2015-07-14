import math, sys, os

from Laser import *
from Ball import *
from Brick import *

def ball_paddle_collision(ball, paddle):
    temp_velocity = math.sqrt((ball.dx ** 2) + (ball.dy ** 2))

    ball.dx = (ball.rect.centerx - paddle.rect.centerx) / 6.0
    if ball.dx >= 7.0 or ball.dx <= -7.0:
        ball.dy *= -1
    else:        
        ball.dy = math.sqrt((temp_velocity ** 2) - (ball.dx ** 2))
        ball.dy *= -1

def ball_brick_collision(ball, brick):
    if ball.rect.collidepoint(brick.rect.left,brick.rect.centery):
        ball.dx *= -1
        
    elif ball.rect.collidepoint(brick.rect.right,brick.rect.centery):
        ball.dx *= -1
        
    else:    
        ball.dy *= -1
    
def ball_ball_collision(ball1, ball2):
    
    temp_dx = ball1.dx
    temp_dy = ball1.dy
    
    temp_dx2 = ball2.dx
    temp_dy2 = ball2.dy
    
    ball1.dx, ball1.dy = temp_dx2, temp_dy2
    ball2.dx, ball2.dy = temp_dx, temp_dy
    
def spawnandshoot(paddle, laser_group):
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-sounds', 'laser_shoot.ogg')
    shoot = pygame.mixer.Sound(sys_name)
    
    laser = Laser(paddle.rect.centerx, paddle.rect.centery)
    laser.shoot(paddle)
    shoot.play()
    laser_group.add(laser)
    
    return laser_group

def decide_upgrade(paddle, upgrade, ball):
    
    if upgrade.number_upgrade == 0:
        paddle.LASER()
        
    elif upgrade.number_upgrade == 1:
        paddle.SUPERPADDLE()
        
    elif upgrade.number_upgrade == 2:
        paddle.SHRINKPADDLE()
        
    elif upgrade.number_upgrade == 4:
        paddle.LIFEUP()
        
    elif upgrade.number_upgrade == 5:
        paddle.STICKYSTATE()
        
def MULTIBALL(ball_group):

    for ball in ball_group:
        temp_ball = Ball(ball.rect.centerx, ball.rect.centery)
        temp_ball.dx, temp_ball.dy = ball.dx, ball.dy
        temp_ball.dx *= -1
        temp_ball.SPAWNSTATE = False
        ball_group.add(temp_ball)
        
    return ball_group

def level_importer(level_number):
    SPACE = 48
    ENTER = 24
    
    NORMALHIT = 0
    NORMALSCORE = 100
    
    SPECIALHIT = 1
    SPECIALSCORE = 300
    
    GOLDHIT = 2
    GOLDSCORE = 1000
    
    temp_x = 40
    temp_y = 24
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-levels', 'LEVEL{0}.txt' . format(level_number))
    level_file = open(sys_name, 'r')
    
    brick_group = pygame.sprite.Group()
    
    brick_list = level_file.read().split('\n')
    
    for line in brick_list:
        for char in line:
            if char == 'G':
                brick = Brick(temp_x, temp_y, GOLDHIT, GOLDSCORE, 7)
                brick_group.add(brick)
                temp_x += SPACE
            elif char != ' ' and int(char) <= 4:
                brick = Brick(temp_x, temp_y, NORMALHIT, NORMALSCORE, int(char))
                brick_group.add(brick)
                temp_x += SPACE
            elif char != ' ' and int(char) > 4:
                brick = Brick(temp_x, temp_y, SPECIALHIT, SPECIALSCORE, int(char))
                brick_group.add(brick)
                temp_x += SPACE
            else:
                temp_x += SPACE
        temp_x = 40
        temp_y += ENTER
                
               
    level_file.close()           
    return brick_group    