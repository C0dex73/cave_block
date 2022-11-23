#========== MAIN FILE ==========
#
# called by the user
# call the menu file and the useJSON file
#
import pygame
import math
import random
from run import menu

pygame.init() #initialize pygame
screen = pygame.display.set_mode((400, 400)) #set the screen to 400 by 400 pixels

running = -1 # running variable

while running != 0: #main loop
    for event in pygame.event.get(): #get all the pygame events
        if event.type == pygame.QUIT: #if the user close the window
            running = 0 #stop the main loop
        if running == -1: #if it's the first iteration
            menu.Menu.__init__(screen) #initialize the menu
            running = 1 #avoid a recall of this section
        pygame.display.flip() #update the screen

pygame.quit() #stop the program