import pygame, os, sys, Menu

from pygame.locals import *

from Ball import *
from Paddle import *
from Brick import *
from Upgrade import *
from Laser import *
from Pybreaker_Functions import *
from Text import *

pygame.mixer.init(22050, -16, 2, 1024)
pygame.init()

def Game(level, lives, score):
    
    try:
        x360 = pygame.joystick.Joystick(0)
        x360.init()
        joypad_status = True
    except pygame.error:
        pass
        joypad_status = False
        
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'ACTIONIS.TTF')        
    score_font = pygame.font.Font(sys_name, 35)
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'COOLFONT.ttf')
    upgrade_font = pygame.font.Font(sys_name, 60) 
    
    size = (800, 640)
    screen = pygame.display.set_mode(size)
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'Background.jpg')
    background = pygame.image.load(sys_name).convert()
    
    pygame.display.set_caption('PYBREAKER =D')
    
    upgrade_message = 0
    upgrade_check = 0
    death_check = 0
    laser_check = 0
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-sounds', 'Powerup.ogg')
    upgrade_sound = pygame.mixer.Sound(sys_name) 
    upgrade_sound.set_volume(0.5)
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-sounds', 'ThechnoTheme.mp3')
    pygame.mixer.music.load(sys_name)
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(10)
    
#########################Creation of Groups/Sprites#############################
    
    player1 = Paddle(lives, score)
    
    paddle = pygame.sprite.GroupSingle()
    paddle.add(player1)
    
    ball = Ball(player1.rect.centerx, (player1.rect.top - 24))
    ball.SPAWNSTATE = True
    
    ball_group = pygame.sprite.Group()
    ball_group.add(ball)
    
    upgrade_group = pygame.sprite.Group()
    
    laser_group = pygame.sprite.Group()
    
    text_group = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    keep_going = True
    
    time_passed = 0
    timer = 0
    sticky_timer = 0
    time_check = 1
    
    pygame.key.set_repeat(100)
    
#################################Level Importing########################
    
    brick_group = pygame.sprite.Group()
    
    brick_group = level_importer(level)
      
#################################Starting the Loop##############################
    
    score_label = Text(40, 603, 'Score: {0}      Lives: {1}' . format(player1.get_score(), player1.lives), (201, 192, 187), score_font)
    text_group.add(score_label)
    
    screen.blit(background, (0, 0))
    
    start = 1
    
    while keep_going:
        clock.tick(30)        
###############################Ball Spawn/Sticky States#########################
        
        if ball.SPAWNSTATE:
            ball.rect.centerx = player1.rect.centerx
            ball.rect.bottom = player1.rect.top
            if player1.STICKY:
                sticky_timer += clock.get_time() / (1000.0)
                if sticky_timer > 2.0:
                    ball.SPAWNSPEEDS()
                    ball.SPAWNSTATE = False
                    sticky_timer = 0
        
#######################COLLISION DETECTION & Handling###########################          
        
        #Temp Stored Collision Values
        if pygame.sprite.spritecollide(player1, ball_group, False):
            ball_list = pygame.sprite.spritecollide(player1, ball_group, False)
            for temp_ball in ball_list:
                if not temp_ball.SPAWNSTATE:
                    ball_paddle_collision(temp_ball, player1)
                if player1.STICKY:
                    temp_ball.dx, temp_ball.dy = 0,0
                    temp_ball.rect.bottom = player1.rect.top 
                    
                    temp_ball.SPAWNSTATE = True
        
        if pygame.sprite.groupcollide(ball_group, brick_group, False, False):
            ball_brick_dict = pygame.sprite.groupcollide(ball_group, brick_group, False, False)
            
            for ball, brick_list in ball_brick_dict.iteritems():
                ball_brick_collision(ball, brick_list[0])
                for brick in brick_list:
                    if brick.hit == 0:
                        brick_group.remove(brick)
                        temp_score = brick.get_score()
                        player1.add_score(temp_score)
                            
                        if brick.upgrade == 1:
                                
                            upgrade = Upgrade(brick.rect.centerx, brick.rect.centery)
                            upgrade_group.add(upgrade)
                            
                    elif brick.hit > 0:
                        brick.hit -= 1
            
        if pygame.sprite.spritecollide(player1, upgrade_group, False):
            temp_upgrade = pygame.sprite.spritecollide(player1, upgrade_group, True)
            screen.blit(background, (0,0))
            
            upgrade_sound.play()
            upgrade_check = 0
            upgrade_message = 1
            
            for upgrade_text in text_group:
                if upgrade_text != score_label:
                    text_group.remove(upgrade_text)
                    
            if temp_upgrade[0].number_upgrade != 1:
                player1.DOWNGRADE()
                
            if player1.paddle_size == -1:
                player1.DOWNGRADE()
                
            timer = 0 
            player1.laser_amount = 0
            player1.STICKY = False
                   
            if temp_upgrade[0].number_upgrade == 0:
                laser_check = 1
                
            if temp_upgrade[0].number_upgrade == 1 or temp_upgrade[0].number_upgrade == 2 or temp_upgrade[0].number_upgrade == 5:
                upgrade_check = 1
                
            if temp_upgrade[0].number_upgrade == 3:
                ball_group = MULTIBALL(ball_group)
                    
            temp_upgrade[0].sound.play()    
            decide_upgrade(player1, temp_upgrade[0], ball)
        
        if pygame.sprite.groupcollide(laser_group, brick_group, False, False):
            laser_brick_dict = pygame.sprite.groupcollide(laser_group, brick_group, False, False)
            for laser, brick_list in laser_brick_dict.iteritems():
                for brick in brick_list:
        
                    if brick.hit == 0:
                        
                        pygame.sprite.groupcollide(laser_group, brick_group, True, True)
                        temp_score = brick.get_score()
                        player1.add_score(temp_score)
                        
                        if brick.upgrade == 1:
                        
                            upgrade = Upgrade(brick.rect.centerx, brick.rect.centery)
                            upgrade_group.add(upgrade)
                        
                    elif brick.hit > 0:
                        
                        pygame.sprite.groupcollide(laser_group, brick_group, True, False)
                        brick.hit -= 1
                          
##################################DEALING WITH UPGRADES#########################
        
        if upgrade_message == 1:
            time_passed += clock.get_time() / (1000.0)
            if len(temp_upgrade) > 0:
                
                if temp_upgrade[0].number_upgrade == 0:
                    upgrade_label = Text(10, 300, 'ZOMG LOLZ YOU GOT THE LAZAWRS!', (199, 211, 235), upgrade_font)
                    
                    laser_label = Text(400, 603,'Laser: {0}' .format(player1.laser_amount), (201, 192, 187), score_font)
                    text_group.add(laser_label)
                    
                elif temp_upgrade[0].number_upgrade == 1:
                    upgrade_label = Text(250, 300, 'SUPER PADDLE!', (199, 211, 235), upgrade_font)
                    
                    time_label = Text(400, 603,'Upgrade Time Left: 15', (201, 192, 187), score_font)
                    text_group.add(time_label)
                
                elif temp_upgrade[0].number_upgrade == 2:
                    upgrade_label = Text(250, 300, 'SHRINK PADDLE!', (199, 211, 235), upgrade_font)
                    
                    time_label = Text(400, 603,'Upgrade Time Left: 15', (201, 192, 187), score_font)
                    text_group.add(time_label)
                    
                elif temp_upgrade[0].number_upgrade == 3:
                    upgrade_label = Text(75, 300, 'MULTIBALL!        MULTIBALL!', (199, 211, 235), upgrade_font)
                
                elif temp_upgrade[0].number_upgrade == 4:
                    upgrade_label = Text(395, 300, '1up!', (199, 211, 235), upgrade_font)
                
                elif temp_upgrade[0].number_upgrade == 5:
                    upgrade_label = Text(280, 300, 'STICKY BALL!', (199, 211, 235), upgrade_font)
                    
                    time_label = Text(400, 603,'Sticky Time Left: 25', (201, 192, 187), score_font)
                    text_group.add(time_label)
                    
                text_group.add(upgrade_label)
                for upgrade in temp_upgrade:
                    temp_upgrade.remove(upgrade)
            if time_passed > 2.0:
                
                text_group.remove(upgrade_label)
                upgrade_message = 0
                time_passed = 0
                
        if upgrade_check == 1:
            timer += clock.get_time() / (1000.0)
                
            if int(timer) > 14 and not player1.STICKY:
                player1.DOWNGRADE()
                text_group.remove(time_label)
                upgrade_check = 0
                timer = 0
                
            elif int(timer) > 20:
                player1.STICKY = False
                timer = 0
                text_group.remove(time_label)
                upgrade_check = 0
                     
        if laser_check == 1:
            if player1.laser_amount == 0:
                laser_check = 0
                text_group.remove(laser_label)
                
#################################EVENTS#########################################
        
        key_list = pygame.key.get_pressed()
        
        if joypad_status:
            xaxis = x360.get_axis(0)
        
            if xaxis > 0.5 and (int(xaxis) + 1) == 1:
                player1.move_paddle(7)
            elif int(xaxis) == -1:
                player1.move_paddle(-7)
    
        if key_list[K_RIGHT] == 1:
            player1.move_paddle(7)
        elif key_list[K_LEFT] == 1:
            player1.move_paddle(-7)
        
        for ev in pygame.event.get():
            
            if ev.type == pygame.JOYBUTTONDOWN:
                if ev.button == 0:
                    if player1.get_laser_amount() > 0:
                        spawnandshoot(player1, laser_group)
                    if ball.SPAWNSTATE or player1.STICKY:
                        ball.SPAWNSPEEDS()
                        ball.SPAWNSTATE = False
            
            if ev.type == pygame.KEYDOWN:
                 
                if ev.key == pygame.K_ESCAPE:
                    keep_going = False
                    return False, player1.lives, player1.score
                
                if ev.key == pygame.K_SPACE:
                    if player1.get_laser_amount() > 0:
                        spawnandshoot(player1, laser_group)
                    if ball.SPAWNSTATE or player1.STICKY:
                        ball.SPAWNSPEEDS()
                        ball.SPAWNSTATE = False
                    
            if ev.type == pygame.QUIT:
                keep_going = False
                return False, player1.lives, player1.score
                       
##############################EXTRANEOUS SPRITES################################      
    
    #I was having Laser's 'pop' up from the bottom of the screen, obviously when the integer value;
    #for their 'rect.centery' was guetting too small and so became positive (silly Python), so I had to;
    #come up with this code to correct the issue...kinda detracts from efficiency, but still necessary
    
        if len(laser_group) > 0:
            for laser in laser_group:
                if laser.rect.centery < 0:
                    laser_group.remove(laser)
                
        if len(ball_group) > 0:
            for ball in ball_group:
                if ball.rect.centery > 600:
                    if len(ball_group) == 1:
                        
    #'DEATH' CALCULATIONS
                        timer = 0
                        player1.lives -= 1                    
                        player1.DOWNGRADE()
                        player1.STICKY = False
                        screen.blit(background, (0, 0))
                        'Clearing Extraneous Upgrades'
                        player1.laser_amount = 0
                        upgrade_check = 0
                        death_check = 1
                        for upgrade_text in text_group:
                            if upgrade_text != score_label:
                                text_group.remove(upgrade_text)
                        if player1.lives > 0:
                            time_label = Text(400, 603,'Time Until Next Life: 3', (201, 192, 187), score_font)
                            text_group.add(time_label)
                        
                    ball_group.remove(ball)
                    
        if len(ball_group) > 0:
            for upgrade in upgrade_group:
                if upgrade.rect.centery > 640:
                    upgrade_group.remove(upgrade)
                    
#####################################DEATH & COMPLETION#########################
        
        if len(ball_group) == 0:
            if death_check == 0:
                ball = Ball(player1.rect.centerx, (player1.rect.centery))
                ball.SPAWNSTATE = True
                ball_group.add(ball)
        
        if len(brick_group) == 0:
            timer += clock.get_time() / (1000.0)
            if timer < 3.0:
                new_level_label = upgrade_font.render('LEVEL {0} COMPLETED! =D' .format(level), True, (201, 192, 187))
                screen.blit(new_level_label, (150, 300))
                
            elif timer > 3.0 and level == 10:
                keep_going = False
                Menu.HighScores(player1.score)
                return False, player1.lives, player1.score
            
            elif timer > 3.0 and level != 10:
                keep_going = False
                return True, player1.lives, player1.score
            
        if death_check == 1 and player1.lives == 0:
            timer += clock.get_time() / (1000.0)
            if timer < 3.0:
                gameover_label = upgrade_font.render('GAME OVER! Try again next time!', True, (201, 192, 187))
                screen.blit(gameover_label, (15, 300))
            else:
                keep_going = False
                Menu.HighScores(player1.score)
                return False, player1.lives, player1.score
        
        if death_check == 1 and player1.lives > 0:
            timer += clock.get_time() / (1000.0)
            upgrade_group.empty()
            if timer > 3.0:
                ball_group.remove(ball)
                timer = 0
                death_check = 0
                text_group.remove(time_label)

####################################LABEL UPDATING##############################
       
        score_label.message = 'Score: {0}      Lives: {1}' .format(player1.get_score(), player1.lives)
        
        if player1.laser_amount > 0:
            laser_label.message = 'Laser: {0}' .format(player1.laser_amount)
            
        if player1.paddle_size != 0:
            if timer < 15 and timer > 0.0:
                time = (15 - int(timer))
                time_label.message = 'Upgrade Time Left: {0}' .format(time)
        if player1.STICKY:
            if timer < 30 and timer > 0.0:
                time = (20 - int(timer))
                time_label.message = 'Sticky Time Left: {0}' .format(time)
        if death_check == 1 and player1.lives > 0:
            if timer < 3 and timer > 0.0:
                time = (3 - int(timer))
                time_label.message = 'Time Until Next Life: {0}' .format(time)
                
######################################UPDATES###################################
        
        text_group.clear(screen, background)
        text_group.update()
        text_group.draw(screen)
        
        paddle.clear(screen, background)
        paddle.update()
        paddle.draw(screen)
        
        ball_group.clear(screen, background)
        ball_group.update()
        ball_group.draw(screen)
        
        brick_group.clear(screen, background)
        brick_group.update()
        brick_group.draw(screen)
        
        upgrade_group.clear(screen, background)
        upgrade_group.update()
        upgrade_group.draw(screen)
        
        laser_group.clear(screen, background)
        laser_group.update()
        laser_group.draw(screen)
        
        pygame.display.flip()
######################################END! =D###################################
