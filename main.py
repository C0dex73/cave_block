
import pygame
import math
import random

def main():
    pygame.init() #initialize pygame
    state = -1 # state variable
    clock = pygame.time.Clock()
    while state != 0: #main loop
        for event in pygame.event.get(): #get all the pygame events

            if event.type == pygame.QUIT: #if the user close the window
                state = 0 #stop the main loop
            
            if state == -1: #first time state
                screen = pygame.display.set_mode((400, 400)) #set the screen to 400 by 400 pixels
                pygame.display.set_caption("CaveBlock") #set the title of the window
                Menu()
                #TODO : add init stuff here
                state = 1
            
            if state == 1:
                pygame.display.update() #update the screen
                #TODO : add tick stuff here
            clock.tick(60) #set the clock rate to 60 fps

    pygame.quit() #stop the program

class Menu: #to handle the menu display
    def __init__(self, screen):
        



if __name__ == "__main__":
    main()