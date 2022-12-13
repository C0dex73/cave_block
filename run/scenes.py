from run.tools import *
from run.player import Player

class Menu: #to handle the menu display
    def __init__(self, screen, pygame, Data): #called while initializing the class
        self.pygame = pygame
        self.Data = Data
        self.next = self #set the next scene to itself
        self.font = self.pygame.font.Font("textures/font.ttf", Rescaler(100, 0)) #set the font

        #parts of tick function to avoid errors with self call
        self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #set the text of the ExitButton
        self.OptionText = self.font.render("Option", True, (250, 250, 250)) #set the text of the OptionButton
        
    
    
    def tick(self, screen, events, keys): #called every active tick
        #background image
        self.bg = self.pygame.image.load("textures/test.png").convert() #load the bg menu image
        self.bg = self.pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen
        
        #EXIT button
        exitButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.exitButtonSurface = self.ExitText.get_rect(topleft=exitButtonTLCorner) #get the whole text surface
        if self.exitButtonSurface.collidepoint(self.pygame.mouse.get_pos()[0], self.pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #make it lighter
            if testEvent([self.pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = None #stop the game (state = 0 in mainloop)
        else: 
            self.ExitText = self.font.render("Exit", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.ExitText, exitButtonTLCorner) #render the text

        #OPTION button
        optionButtonTLCorner = (Rescaler(50, 0), Rescaler(500, 1)) #set the topleft corner of the button
        self.optionButtonSurface = self.OptionText.get_rect(topleft=optionButtonTLCorner) #get the whole text surface
        if self.optionButtonSurface.collidepoint(self.pygame.mouse.get_pos()[0], self.pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.OptionText = self.font.render("Option", True, (250, 250, 250)) #make it lighter
            if testEvent([self.pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Options(screen, self.pygame, self.Data) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.OptionText = self.font.render("Option", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.OptionText, optionButtonTLCorner) #render the text




class Options: #to handle the option menu display
    def __init__(self, screen, pygame, Data): #called when initializing this class
        self.pygame = pygame
        self.Data = Data
        self.next = self #set the next scene to itself
        self.font1 = self.pygame.font.Font("textures/font.ttf", Rescaler(100, 0)) #set the fonts
        self.font2 = self.pygame.font.Font("textures/font2.ttf", Rescaler(25, 0))

        #parts of tick function to avoid errors with self call
        self.MenuText = self.font1.render("Menu", True, (250, 250, 250)) #set the text of the ExitButton

    def tick(self, screen, events, keys): #called every active tick
        #background image
        self.bg = self.pygame.image.load("textures/used/bigdoor23.png").convert() #load the bg option image #TODO : replace this with the real path
        self.bg = self.pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen

        #MENU button
        menuButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.menuButtonSurface = self.MenuText.get_rect(topleft=menuButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(self.pygame.mouse.get_pos()[0], self.pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.MenuText = self.font1.render("Menu", True, (250, 250, 250)) #make it lighter
            if testEvent([self.pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Menu(screen, self.pygame, self.Data) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.MenuText = self.font1.render("Menu", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.MenuText, menuButtonTLCorner) #render the text
        
        #right button 
        #indicator
        if testKey(self.Data["inputs"]["right"], keys, self.pygame):
            self.pygame.draw.rect(screen, (0, 255, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(60, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            self.pygame.draw.rect(screen, (255, 0, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(60, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.rightText = self.font2.render("Right (" + self.Data["inputs"]["right"] + ")", True, (225, 225, 225))
        screen.blit(self.rightText, (Rescaler(630, 0), Rescaler(60, 1)))
            
            
        #left button
        # indicator
        if testKey(self.Data["inputs"]["left"], keys, self.pygame):
            self.pygame.draw.rect(screen, (0, 255, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(135, 1), 
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            self.pygame.draw.rect(screen, (255, 0, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(135, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.leftText = self.font2.render("Left (" + self.Data["inputs"]["left"] + ")", True, (225, 225, 225))
        screen.blit(self.leftText, (Rescaler(630, 0), Rescaler(135, 1)))
            
        #jump button
        # indicator
        if testKey(self.Data["inputs"]["jump"], keys, self.pygame):
            self.pygame.draw.rect(screen, (0, 255, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(210, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            self.pygame.draw.rect(screen, (255, 0, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(210, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.jumpText = self.font2.render("Jump (" + self.Data["inputs"]["jump"] + ")", True, (225, 225, 225))
        screen.blit(self.jumpText, (Rescaler(630, 0), Rescaler(210, 1)))            
            
        #crouch button
        # indicator
        if testKey(self.Data["inputs"]["crouch"], keys, self.pygame):
            self.pygame.draw.rect(screen, (0, 255, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(285, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            self.pygame.draw.rect(screen, (255, 0, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(285, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.crouchText = self.font2.render("Crouch (" + self.Data["inputs"]["crouch"] + ")", True, (225, 225, 225))
        screen.blit(self.crouchText, (Rescaler(630, 0), Rescaler(285, 1)))
        
        #shoot button
        # indicator
        if testKey(self.Data["inputs"]["shoot"], keys, self.pygame):
            self.pygame.draw.rect(screen, (0, 255, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(360, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25 ,1)),
                                                                        border_radius=2)
        else:
            self.pygame.draw.rect(screen, (255, 0, 0), self.pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(360, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)), 
                                                                        border_radius=2)
        #text
        self.shootText = self.font2.render("Shoot (" + self.Data["inputs"]["shoot"] + ")", True, (225, 225, 225))
        screen.blit(self.shootText, (Rescaler(630, 0), Rescaler(360, 1)))



class Game:
    def __init__(self, screen, pygame, Data): #called when initializing this class
        self.pygame = pygame
        self.Data = Data
        self.terrain = TerrainGen()
        self.player = Player(screen)
        
    def tick(self, screen, events, keys):
        DrawTerrain(screen, self.terrain, self.Data)