import pygame, pickle
from pygame.locals import *

from Paddle import *
from Ball import *
from Text import *

pygame.init()
pygame.mixer.init(44100, -16, 2, 512)

def Menu():
    
    try:
        x360 = pygame.joystick.Joystick(0)
        x360.init()
    except pygame.error:
        print 'Cannot load Joypad'
        
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    
    comp = Paddle(0, 0)
    comp_ball = Ball(comp.rect.centerx, comp.rect.centery - 25)
    
    comp_ball.SPAWNSPEEDS()
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'Menu Background.JPG')
    background = pygame.image.load(sys_name).convert()
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'COOLFONT.ttf')
    large_score_font = pygame.font.Font(sys_name, 90)
    small_score_font = pygame.font.Font(sys_name, 40)
    
    clock = pygame.time.Clock()
    menuLoop = True
    help_check = 0
    
    ball_group = pygame.sprite.Group()
    ball_group.add(comp_ball)
    
    paddle = pygame.sprite.Group()
    paddle.add(comp)
    
    text_group = pygame.sprite.Group()
        
    screen.blit(background, (0,0))
    
    while menuLoop:
        clock.tick(30)
        
        comp.rect.centerx = comp_ball.rect.centerx
        
        if comp.rect.colliderect(comp_ball):
            comp_ball.dy *= -1
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                keep_going = False
                return False
                
            if ev.type == pygame.JOYBUTTONDOWN:
                if ev.button == 0:
                    if help_check == 0:
                        menuLoop = False
                        return True
                    else:
                        background = PyBreaker_MainMenu(screen, help_check, text_group)
                        help_check = 0
                        
                if ev.button == 1:
                    background = PyBreaker_Help(screen, text_group)
                    help_check = 1
                        
                if ev.button == 2:
                    background = PyBreaker_Scores(screen, large_score_font, small_score_font, text_group)
                    return_message = Text(25, 540, 'Press Enter or Space to return to the Menu', (199, 211, 235), small_score_font)
                    text_group.add(return_message)
                    help_check = 1
                        
            if ev.type == pygame.KEYDOWN:
                
                if ev.key == pygame.K_ESCAPE:
                    keep_going = False
                    return False
                
                if ev.key == 13 or ev.key == pygame.K_SPACE:
                    if help_check == 0:
                        menuLoop = False
                        return True
                    else:
                        background = PyBreaker_MainMenu(screen, help_check, text_group)
                        help_check = 0
                
                if ev.key == K_h:
                    background = PyBreaker_Help(screen, text_group)
                    help_check = 1
                    
                if ev.key == K_LSHIFT or ev.key == K_RSHIFT:
                    background = PyBreaker_Scores(screen, large_score_font, small_score_font, text_group)
                    return_message = Text(25, 540, 'Press Enter or Space to return to the Menu', (199, 211, 235), small_score_font)
                    text_group.add(return_message)
                    help_check = 1
                        
        text_group.clear(screen, background)
        text_group.update()
        text_group.draw(screen)
        
        paddle.clear(screen, background)
        paddle.update()
        paddle.draw(screen)
        
        ball_group.clear(screen, background)
        ball_group.update()
        ball_group.draw(screen)
        
        pygame.display.update()
        
def HighScores(score):
    score_file = Check_Scores()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    greater_than = False
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'COOLFONT.ttf')
    largeFont = pygame.font.Font(sys_name, 75)
    smallFont = pygame.font.Font(sys_name, 40)
    
    ENTER = 40
    temp_y = 300
    
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))
    
    text_group = pygame.sprite.Group()
    
    screen.blit(background, (0,0))
    usr_name = str()
    
    load = pickle.load(score_file)
    keys = load.keys()
    keys.sort()
    
    for key in keys:
        if score > key:
            greater_than = True
            
    if greater_than:
        greeting = Text(35, 100, 'YOU GOT A HIGH SCORE =D', (199, 211, 235), largeFont)
        text_group.add(greeting)
        
        text_name = Text(35, 400, 'ENTER YOUR NAME: {0}' .format(usr_name), (199, 211, 235), smallFont)
        text_group.add(text_name)
        check = False
        
        scoreLoop = True
        check = False
        
        while scoreLoop:
        
            for ev in pygame.event.get():
                
                if ev.type == pygame.QUIT:
                    scoreLoop = False
                    
                if ev.type == pygame.KEYDOWN:
                    
                    if ev.key == pygame.K_ESCAPE:
                        scoreLoop = False
                    if not check:
                        if ev.key == 13:
                            check = True
                        elif ev.key == 32:
                            usr_name += " "
                           
                        elif ev.key == 8:
                                if len(usr_name) > 0:
                                    usr_name = usr_name[:-1]
                                    text_name.message = text_name.message[:-1]
                        else:
                            temp = ev.key
                            letter = pygame.key.name(temp)
                            usr_name += letter
                            text_name.message = 'ENTER YOUR NAME: {0}' .format(usr_name)
                    
                          
            if check:
                load[score] = usr_name
                if len(load) > 5:
                    load.pop(keys[0])
                check = False
                
                score_file = open('Highscores.pkl', 'wb')
                pickle.dump(load, score_file)
                
                score_file.close()
                
                score_file = open('Highscores.pkl', 'rb')
                load = pickle.load(score_file)
                                
                score_file.close()
                text_group.empty()
                    
                background = PyBreaker_Scores(screen, largeFont, smallFont, text_group)
                
                quit_message = Text(25, 540, 'Press Escape to quit', (199, 211, 235), smallFont)
                
                text_group.add(quit_message)
                
            text_group.clear(screen, background)
            text_group.update()
            text_group.draw(screen)
            
            pygame.display.update()
        
    else:
        greeting = Text(200, 100, "YOU DIDN'T GET A HIGH SCORE!", (199, 211, 235), smallFont)
        text_group.add(greeting)
        
        greeting2 = Text(200, 140, "TRY AGAIN NEXT TIME...", (199, 211, 235), smallFont)
        text_group.add(greeting2)
        
        quit_message = Text(25, 520, 'Press Space to see the HighScores', (199, 211, 235), smallFont)
        quit_message2 = Text(25, 560, 'Escape to quit', (199, 211, 235), smallFont)
        text_group.add(quit_message)
        text_group.add(quit_message2)
        
        scoreLoop = True
        check = False
        while scoreLoop:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    scoreLoop = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        scoreLoop = False
                    elif ev.key == K_SPACE:
                        check = True
            if check:
                text_group.empty()
                background = PyBreaker_Scores(screen, largeFont, smallFont, text_group)
                    
                quit_message = Text(25, 540, 'Press Escape to quit', (199, 211, 235), smallFont)
                    
                text_group.add(quit_message)
                check = False
                
            text_group.clear(screen, background)
            text_group.update()
            text_group.draw(screen)
            
            pygame.display.update()   

    
        
def PyBreaker_MainMenu(screen, help_check, text_group):
    for text in text_group:
        text_group.remove(text)
            
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'Menu Background.JPG')
    background = pygame.image.load(sys_name).convert()    
            
    screen.blit(background, (0,0))

    return background

def PyBreaker_Help(screen, text_group):
    for text in text_group:
        text_group.remove(text)
    
    sys_name = os.path.join(sys.path[0], 'Pybreaker-images', 'Help Background.JPG')
    background = pygame.image.load(sys_name).convert()
                    
    screen.blit(background, (0,0))
    
    return background

def PyBreaker_Scores(screen, large_score_font, small_score_font, text_group):
    score_file = Check_Scores()
    ENTER = 40
    
    load = pickle.load(score_file)
    
    keys = load.keys()
    keys.sort()
        
    temp_y = 300
    
    background = pygame.Surface((800, 640))
    background.fill((0, 0, 0))
    
    screen.blit(background, (0,0))
                        
    greeting = Text(200, 100, 'HIGH SCORES', (199, 211, 235), large_score_font)
    text_group.add(greeting)
    
    for k in range(4, -1, -1):
        temp_score = Text(50, temp_y, '{0}: {1}' .format(keys[k], load[keys[k]]), (199, 211, 235), small_score_font)
        text_group.add(temp_score)
        temp_y += ENTER
    
    score_file.close()
    return background

def Check_Scores():
    try:
        score_file = open('Highscores.pkl', 'rb')
    except IOError:
        score_file = open('Highscores.pkl', 'wb')

        D = {50000: 'BILLY BOB THE KING', 20000: 'Player2', 15000: 'Player3', 10000: 'Player4',
             5000: 'Player5'}

        pickle.dump(D, score_file)   
        
        score_file.close()
        
        score_file = open('Highscores.pkl', 'rb')
    
    return score_file  