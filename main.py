"""
this is the main module that will be called when the user launch the game
it call run folder
it init pygame and the main loop
"""
import json
import pygame
from run.scenes import Menu

def main() -> None:
    """
    this is the main function that will be called when the module is executed
    
    return nothing
    """
    
    #inistalizing variables
    pygame.init()
    screen = pygame.display.set_mode(Data["screen"]["size"])
    state = 1
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(Data["volume"])
    
    pygame.display.set_caption(Data["screen"]["caption"]) #set the title of the window
    scene = Menu(screen, Data) #set the first scene to the menu scene

    #~ MAIN LOOP
    while state != 0:
        
        #get the inputs
        events = pygame.event.get() 
        keys = pygame.key.get_pressed()
        
        #check if the user quits the game
        for event in events:
            if event.type == pygame.QUIT:
                state = 0 #stop the main loop

        scene.tick(screen, events, keys) #do app tick
        
        if scene.next == None: #if we don't have any scene next
            state = 0 #stop the main loop
        else :
            scene = scene.next #change to the next scene defined by the actual scene
        
        
        pygame.display.update() #update the screen
        clock.tick(60) #set the clock rate to 60 fps
        
    pygame.quit() #stop the program

#main program
with open("data/app.json", "r") as f: #open the file with app parameters
    Data = json.load(f) #save the data to a var (:dict)
main()