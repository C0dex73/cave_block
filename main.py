
import pygame
import math
import random
pygame.init() #initialize pygame

running = -1 # running variable
clock = pygame.time.Clock()
while running != 0: #main loop
    for event in pygame.event.get(): #get all the pygame events

        if event.type == pygame.QUIT: #if the user close the window
            running = 0 #stop the main loop
        
        if running == -1:
            screen = pygame.display.set_mode((400, 400)) #set the screen to 400 by 400 pixels
            pygame.display.set_caption("CaveBlock") #set the title of the window
            #TODO : add init stuff here
            running = 1
        
        if running == 1:
            pygame.display.update() #update the screen
            #TODO : add tick stuff here
        clock.tick(60) #set the clock rate to 60 fps

pygame.quit() #stop the program

class Menu:
    def innit(screen):
        image = pygame.image.load("")