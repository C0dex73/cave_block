
import pygame
import math
import random
import json
from handler import *

def main():
    pygame.init() #initialize pygame
    screen = pygame.display.set_mode(Data["screen"]["size"]) #init the screen
    state = 1 # state variable
    clock = pygame.time.Clock() #init the clock

    scene = Menu(screen) #set the first scene to the menu scene
    pygame.display.set_caption(Data["screen"]["caption"]) #set the title of the window

    while state != 0: #main loop
        for event in pygame.event.get(): #get all the pygame events

            if event.type == pygame.QUIT: #if the user close the window
                state = 0 #stop the main loop
            
        #TODO : add tick stuff here

        scene.tick(screen)
        if scene.next == None: #TODO : add stop from next
            state
        scene = scene.next #change to the next scene defined by the actual scene
        pygame.display.update()
        clock.tick(60) #set the clock rate to 60 fps
    pygame.quit() #stop the program

#classes
class Menu: #to handle the menu display
    def __init__(self, screen):
        self.next = self #set the next scene to itself
        self.font = pygame.font.Font("textures/font.ttf", 100) #set the font

        #parts of tick function for if detection
        self.text = self.font.render("EXIT", True, (250, 250, 250))
    def tick(self, screen): #called every game tick

        #background image
        self.bg = pygame.image.load("textures/test.png").convert() #load the bg menu image
        self.bg = pygame.transform.scale(self.bg, Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen

        #EXIT button
        exitButtonTLCorner = (50, 600)
        self.exitButtonSurface = self.text.get_rect(topleft=exitButtonTLCorner)
        if self.exitButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            self.text = self.font.render("EXIT", True, (250, 250, 250))
            if testEvent(pygame.MOUSEBUTTONDOWN): #TODO : add quit()
                
        else:
            self.text = self.font.render("EXIT", True, (200, 200, 200))
        screen.blit(self.text, exitButtonTLCorner)
        
        self.next = self #set the next scene to itself


def testEvent(event):
    for e in pygame.event.get():
        if e.type == event:
            return True
    return False

#main program
with open("data/app.json", "r") as f: #open the file with app parameters
    Data = json.load(f) #save the data to a var
main()