#========== MAIN FILE ==========
#
# called by the user
# call the menu file and the useJSON file
#
import pygame
import math
import random
from run.menu import Menu
from data.useJSON import useJSON

pygame.init() #initialize pygame

#using useJSON.Get("data/app.json") to get the app dictionary
screen = pygame.display.set_mode(useJSON.Get("data/app.json")["size"]) #set the screen to 400 by 400 pixels
pygame.display.set_caption(useJSON.Get("data/app.json")["title"])

running = -1 # running variable

while running != 0: #main loop
    for event in pygame.event.get(): #get all the pygame events

        if event.type == pygame.QUIT: #if the user close the window
            running = 0 #stop the main loop

        if running == -1: #if it's the first iteration
            Menu(screen) #initialize the menu (run Menu.__init__(Menu, screen))
            running = 1 #avoid a recall of this section
        
        pygame.display.flip() #update the screen

pygame.quit() #stop the program