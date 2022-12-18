from run.tools import *
from run.player import Player
import pygame

class Menu: #to handle the menu display
    def __init__(self, screen, Data): #called while initializing the class
        self.Data = Data
        self.next = self #set the next scene to itself
        self.font = pygame.font.Font("textures/font.ttf", Rescaler(100, 0)) #set the font

        #parts of tick function to avoid errors with self call
        self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #set the text of the ExitButton
        self.OptionText = self.font.render("Option", True, (250, 250, 250)) #set the text of the OptionButton
        self.newGameText = self.font.render("New Game", True, (250, 250, 250)) #set the text of the NewGameButton
        
    
    
    def tick(self, screen, events, keys): #called every active tick
        #background image
        self.bg = pygame.image.load("textures/test.png").convert() #load the bg menu image #TODO : use the real path
        self.bg = pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen
        
        #EXIT button
        exitButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.exitButtonSurface = self.ExitText.get_rect(topleft=exitButtonTLCorner) #get the whole text surface
        if self.exitButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = None #stop the game (state = 0 in mainloop)
        else: 
            self.ExitText = self.font.render("Exit", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.ExitText, exitButtonTLCorner) #render the text

        #OPTION button
        optionButtonTLCorner = (Rescaler(50, 0), Rescaler(500, 1)) #set the topleft corner of the button
        self.optionButtonSurface = self.OptionText.get_rect(topleft=optionButtonTLCorner) #get the whole text surface
        if self.optionButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.OptionText = self.font.render("Option", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Options(screen, self.Data, self) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.OptionText = self.font.render("Option", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.OptionText, optionButtonTLCorner) #render the text

        #NEW GAME button
        newGameButtonTLCorner = (Rescaler(50, 0), Rescaler(300, 1)) #set the topleft corner of the button
        self.newGameButtonSurface = self.newGameText.get_rect(topleft=newGameButtonTLCorner) #get the whole text surface
        if self.newGameButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.newGameText = self.font.render("New Game", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Game(screen, self.Data) #start a new game
        else: 
            self.newGameText = self.font.render("New Game", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.newGameText, newGameButtonTLCorner) #render the text



class Options: #to handle the option menu display
    def __init__(self, screen, Data, returnScene): #called when initializing this class
        self.returnScene = returnScene #save the scene to call at the end of the option scene
        self.Data = Data #save Data
        self.next = self #set the next scene to itself
        self.font1 = pygame.font.Font("textures/font.ttf", Rescaler(100, 0)) #set the fonts
        self.font2 = pygame.font.Font("textures/font2.ttf", Rescaler(25, 0))

        #parts of tick function to avoid errors with self call
        self.returnText = self.font1.render("Return", True, (250, 250, 250)) #set the text of the ExitButton

    def tick(self, screen, events, keys): #called every active tick
        #background image
        self.bg = pygame.image.load("textures/used/bigdoor23.png").convert() #load the bg option image #TODO : replace this with the real path
        self.bg = pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen

        #RETURN button
        returnButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.menuButtonSurface = self.returnText.get_rect(topleft=returnButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.returnText = self.font1.render("Return", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.returnScene.next = self.returnScene #modify the .next atribute of the return scene beccause that was the Option scene
                self.next = self.returnScene #pass to the last scene
        else: 
            self.returnText = self.font1.render("Return", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.returnText, returnButtonTLCorner) #render the text
        
        #right button 
        #indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["right"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(60, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(60, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.rightText = self.font2.render("Right (" + self.Data["inputs"]["right"] + ")", True, (225, 225, 225))
        screen.blit(self.rightText, (Rescaler(630, 0), Rescaler(60, 1)))
            
            
        #left button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["left"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(135, 1), 
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(135, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.leftText = self.font2.render("Left (" + self.Data["inputs"]["left"] + ")", True, (225, 225, 225))
        screen.blit(self.leftText, (Rescaler(630, 0), Rescaler(135, 1)))
            
        #jump button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["jump"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(210, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(210, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.jumpText = self.font2.render("Jump (" + self.Data["inputs"]["jump"] + ")", True, (225, 225, 225))
        screen.blit(self.jumpText, (Rescaler(630, 0), Rescaler(210, 1)))            
            
        #crouch button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["crouch"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(285, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(285, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)),
                                                                        border_radius=2)
        #text
        self.crouchText = self.font2.render("Crouch (" + self.Data["inputs"]["crouch"] + ")", True, (225, 225, 225))
        screen.blit(self.crouchText, (Rescaler(630, 0), Rescaler(285, 1)))
        
        #shoot button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["shoot"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(360, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25 ,1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(360, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)), 
                                                                        border_radius=2)
        #text
        self.shootText = self.font2.render("Shoot (" + self.Data["inputs"]["shoot"] + ")", True, (225, 225, 225))
        screen.blit(self.shootText, (Rescaler(630, 0), Rescaler(360, 1)))
        
        #use button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["use"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(435, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25 ,1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(435, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)), 
                                                                        border_radius=2)
        #text
        self.useText = self.font2.render("Use (" + self.Data["inputs"]["use"] + ")", True, (225, 225, 225))
        screen.blit(self.useText, (Rescaler(630, 0), Rescaler(435, 1)))
        
        #ingameMenu button
        # indicator
        if keys[eval("pygame.K_" + self.Data["inputs"]["igMenu"])]:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(510, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25 ,1)),
                                                                        border_radius=2)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(Rescaler(600, 0),
                                                                        Rescaler(510, 1),
                                                                        Rescaler(25, 0),
                                                                        Rescaler(25, 1)), 
                                                                        border_radius=2)
        #text
        self.igText = self.font2.render("INGAME Menu (" + self.Data["inputs"]["igMenu"] + ")", True, (225, 225, 225))
        screen.blit(self.igText, (Rescaler(630, 0), Rescaler(510, 1)))



class Game:
    def __init__(self, screen, Data, player=None): #called when initializing this class
        self.font = pygame.font.Font("textures/font.ttf", Rescaler(100, 0)) #set the font
        self.OptionText = self.font.render("Option", True, (250, 250, 250)) #set the text of the OptionButton
        self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #set the text of the ExitButton
        self.Data = Data
        self.terrain = TerrainGen()
        if player == None:
            self.player = Player(screen)
        else :
            self.player = player
        self.next = self
        self.terrain = DrawTerrain(screen, self.terrain, self.Data)
        self.inGameMenu = False
        
    def tick(self, screen, events, keys):
        if keys[eval("pygame.K_" + self.Data["inputs"]["igMenu"])] and testEvent([pygame.KEYDOWN], events): self.inGameMenu = not self.inGameMenu #if the user press the igMenu key then toggle the menu interface
        if self.inGameMenu: #if the user is on the igMenu
            self.__IGMenu(screen, events) #render it
        else: #else do the game normal tick
            screen.blit(self.terrain, (0, 0))
            
    def __IGMenu(self, screen, events): #render the in-game menu 
        screen.blit(self.terrain, (0, 0)) #render the background in first to set in background
        igMenuSurface = pygame.Surface(self.Data["screen"]["size"], pygame.SRCALPHA).convert_alpha()
        menuFilter = pygame.Surface(self.Data["screen"]["size"])
        menuFilter.set_alpha(128)
        menuFilter.fill((75, 75, 75))
        igMenuSurface.blit(menuFilter.convert_alpha(), (0, 0))
        
        #OPTION button
        optionButtonTLCorner = (Rescaler(50, 0), Rescaler(500, 1)) #set the topleft corner of the button
        self.optionButtonSurface = self.OptionText.get_rect(topleft=optionButtonTLCorner) #get the whole text surface
        if self.optionButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.OptionText = self.font.render("Option", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Options(screen, self.Data, self) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.OptionText = self.font.render("Option", True, (200, 200, 200)) #set the text to his normal color
        igMenuSurface.blit(self.OptionText, optionButtonTLCorner) #render the text
        
        #MENU button
        menuButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.menuButtonSurface = self.MenuText.get_rect(topleft=menuButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Menu(screen, self.Data) #pass to Option scene (state = 2 in mainloop)
        else: 
            self.MenuText = self.font.render("Menu", True, (200, 200, 200)) #set the text to his normal color
        igMenuSurface.blit(self.MenuText, menuButtonTLCorner) #render the text
        
        screen.blit(igMenuSurface, (0, 0))