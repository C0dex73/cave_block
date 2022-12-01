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
        events = pygame.event.get() #get all the pygame events and store them in a variable
        for event in events:
            if event.type == pygame.QUIT: #if the user close the window
                state = 0 #stop the main loop

        scene.tick(screen, events) #do everything to do in the tick of the scene
        if scene.next == None: #if we don't have any scene next
            state = 0 #stop the main loop
        else :
            scene = scene.next #change to the next scene defined by the actual scene
        pygame.display.update() #update the screen
        clock.tick(120) #set the clock rate to 60 fps
    pygame.quit() #stop the program

#classes
class Menu: #to handle the menu display
    def __init__(self, screen): #called while initializing the class
        self.next = self #set the next scene to itself
        self.font = pygame.font.Font("textures/font.ttf", 100) #set the font

        #parts of tick function to avoid errors with self call
        self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #set the text of the ExitButton
        self.OptionText = self.font.render("Option", True, (250, 250, 250)) #set the text of the OptionButton
        
    
    
    def tick(self, screen, events): #called every active tick
        #background image
        self.bg = pygame.image.load("textures/test.png").convert() #load the bg menu image
        self.bg = pygame.transform.scale(self.bg, Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen
        #EXIT button
        exitButtonTLCorner = (50, 600) #set the topleft corner of the button
        self.exitButtonSurface = self.ExitText.get_rect(topleft=exitButtonTLCorner) #get the whole text surface
        if self.exitButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = None #stop the game (state = 0 in mainloop)
        else: 
            self.ExitText = self.font.render("Exit", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.ExitText, exitButtonTLCorner) #render the text

        #OPTION button
        optionButtonTLCorner = (50, 500) #set the topleft corner of the button
        self.optionButtonSurface = self.OptionText.get_rect(topleft=optionButtonTLCorner) #get the whole text surface
        if self.optionButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.OptionText = self.font.render("Option", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Options(screen) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.OptionText = self.font.render("Option", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.OptionText, optionButtonTLCorner) #render the text

class Options: #to handle the option menu display
    def __init__(self, screen): #called when initializing this class
        self.next = self #set the next scene to itself
        self.font = pygame.font.Font("textures/font.ttf", 100) #set the font

        #parts of tick function to avoid errors with self call
        self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #set the text of the ExitButton

    def tick(self, screen, events): #called every active tick
        #background image
        self.bg = pygame.image.load("textures/used/bigdoor23.png").convert() #load the bg option image #TODO : replace this with the real path
        self.bg = pygame.transform.scale(self.bg, Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen

        #OPTION button
        menuButtonTLCorner = (50, 600) #set the topleft corner of the button
        self.menuButtonSurface = self.MenuText.get_rect(topleft=menuButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Menu(screen) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.MenuText = self.font.render("Menu", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.MenuText, menuButtonTLCorner) #render the text



def testEvent(Tevents, Revents):
    for event in Tevents: #for each event to check
        for e in Revents: #for each event appenning
            if e.type == event: #if there are the event to check return true else return false
                return True
    return False

#main program
with open("data/app.json", "r") as f: #open the file with app parameters
    Data = json.load(f) #save the data to a var
main()