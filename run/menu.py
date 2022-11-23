#==========MENU CLASS FOR THE MENU DISPLAYING==========
#
# - called by main.py when the game start
# - call differents levels like tutorial.py or game.py when executed
#
import pygame
import random
import math

class Menu:
    def __init__(screen): #called at the beginning to initialize the menu displaying
        bgPicture = pygame.image.load("medias/pictures/menu.png").convert() #import the background picture
        bgPicture = pygame.transform.scale(bgPicture, (400, 400)) #rescale the background picture to the window size
        
        screen.blit(bgPicture, (0, 0)) #load the background picture at coordinates 0;0
