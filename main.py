import pygame
import json
from run import *

def main():
    pygame.init() #initialize pygame
    screen = pygame.display.set_mode(Data["screen"]["size"]) #init the screen
    state = 1 # state variable
    clock = pygame.time.Clock() #init the clock

    scene = Menu(screen, Data) #set the first scene to the menu scene
    pygame.display.set_caption(Data["screen"]["caption"]) #set the title of the window

    while state != 0: #main loop
        events = pygame.event.get() #get all the pygame events and store them in a variable
        keys = pygame.key.get_pressed() #get all the keyboard inputs and store them in a variable
        for event in events:
            if event.type == pygame.QUIT: #if the user close the window
                state = 0 #stop the main loop

        scene.tick(screen, events, keys) #do everything to do in the tick of the scene
        if scene.next == None: #if we don't have any scene next
            state = 0 #stop the main loop
        else :
            scene = scene.next #change to the next scene defined by the actual scene
        pygame.display.update() #update the screen
        clock.tick(60) #set the clock rate to 60 fps
    pygame.quit() #stop the program

#main program
with open("data/app.json", "r") as f: #open the file with app parameters
    Data = json.load(f) #save the data to a var
main()