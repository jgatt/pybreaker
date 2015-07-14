#!/usr/bin/env python
#Created by Gatt, Jason

import Game, Menu

menuLoop = True
gameLoop = False
level = 1
lives = 3
score = 0

while menuLoop:
    game_start = Menu.Menu()
    if game_start:
        gameLoop = True
        menuLoop = False
    else:
        break
     
while gameLoop:
    game_countinue = Game.Game(level,lives, score)
    lives = game_countinue[1]
    score = game_countinue[-1]
    if game_countinue[0]:
        level += 1
    else:
        break
    
