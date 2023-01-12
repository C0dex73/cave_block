"""
scenes.py is the module where all the scenes like menu, Controls or the game in itself are stored
it contains classes that represent the scenes and each class has its own tick function
"""
from run.tools import *
from run.entities import *
from run.interactions import *
from typing import Sequence
import pygame

class Menu: 
    """
    handle menu displaying and processing
    """
    def __init__(self, screen:pygame.surface.Surface, Data:dict, timer:float=0.00): #called while initializing the class
        """
        initialize the class
        
        screen : the screen ti display the menu
        Data : the app data (data/app.json file)
        timer : the time  where to start for music
        """
        self.Data = Data.copy()
        self.next = self #set the next scene to itself
        self.font = pygame.font.Font("assets/font.ttf", Rescaler(125)) #set the font

        #parts of tick function to avoid errors with self call
        self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #set the text of the ExitButton
        self.controlText = self.font.render("control", True, (250, 250, 250)) #set the text of the controlButton
        self.newGameText = self.font.render("New Game", True, (250, 250, 250)) #set the text of the NewGameButton
        
        if timer != -1:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/sounds/menu.ogg")
            pygame.mixer.music.play(-1, timer, 500)
    
    
    def tick(self, screen:pygame.surface.Surface, events:list[pygame.event.Event], keys:Sequence[bool]): #called every active tick
        """do the Menu tick (60 per second)

        Args:
            screen (_type_): _description_
            events (_type_): _description_
            keys (_type_): _description_
        """
        self.Data = GetData("data/app.json") #actualize the data
        #~background image
        self.bg = pygame.image.load("assets/used/menu.png").convert() #load the bg menu image 
        self.bg = pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen
        
        #~EXIT button
        exitButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.exitButtonSurface = self.ExitText.get_rect(topleft=exitButtonTLCorner) #get the whole text surface
        if self.exitButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.ExitText = self.font.render("Exit", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = None #stop the game (state = 0 in mainloop)
        else: 
            self.ExitText = self.font.render("Exit", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.ExitText, exitButtonTLCorner) #render the text

        #~control button
        controlButtonTLCorner = (Rescaler(50, 0), Rescaler(500, 1)) #set the topleft corner of the button
        self.controlButtonSurface = self.controlText.get_rect(topleft=controlButtonTLCorner) #get the whole text surface
        if self.controlButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.controlText = self.font.render("control", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Controls(screen, self.Data, self) #pass to control scene (state = 2 in mainloop)
        else: 
            self.controlText = self.font.render("control", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.controlText, controlButtonTLCorner) #render the text

        #~NEW GAME button
        newGameButtonTLCorner = (Rescaler(50, 0), Rescaler(400, 1)) #set the topleft corner of the button
        self.newGameButtonSurface = self.newGameText.get_rect(topleft=newGameButtonTLCorner) #get the whole text surface
        if self.newGameButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.newGameText = self.font.render("New Game", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Game(screen, self.Data) #start a new game
        else: 
            self.newGameText = self.font.render("New Game", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.newGameText, newGameButtonTLCorner) #render the text




class Game:
    def __init__(self, screen:pygame.surface.Surface, Data:dict, timer:float=0.00, player:Player|None=None, mines:list[Mine]|None=None, flyers:list[Flyer]|None=None, igMenu:bool=False, playerHealth:int=100, score:int=0) -> None: #called when initializing this class
        """init the game class
        
        Args :
            screen (pugame.surface.Surface): the screen where the game will be displayed
            Data (dict): the data from the app.json file
            timer (float) : when to start the music in seconds
            player (Player|None): the player
            mines (list[Mine]|None): the mines
            flyers (list[Flyer]|None): the flyers
            igMenu (bool): does it have to start with the in game menu open ?
            playerHealth (int): the player health at the start of the game
            score (int): the score at the start of the game
            
        Return :
            Nothing
        """
        self.font = pygame.font.Font("assets/font.ttf", Rescaler(100)) #set the font
        self.HUDfont = pygame.font.Font("assets/HUDfont.ttf", Rescaler(75, 0)) #set the HUD font
        self.controlText = self.font.render("control", True, (250, 250, 250)) #set the text of the controlButton
        self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #set the text of the ExitButton
        self.Data = Data.copy() #set the data
        
        #*entities
        self.terrain, self.positions = TerrainGen(self.Data) #generate the coded terrain and the positions of the entities
        if player == None:
            self.player = Player(screen, self.positions["player"], self.Data, playerHealth)
        else :
            self.player = player
        if mines == None:
            self.mines = []
            for minePos in self.positions["mines"]:
                self.mines.append(Mine(screen, minePos, self.Data))
        else :
            self.mines = mines
        if flyers == None:
            self.flyers = []
            for flyerPos in self.positions["flyers"]:
                self.flyers.append(Flyer(screen, flyerPos, self.Data))
        else :
            self.flyers = flyers
        self.explosions = []
        self.bullets = []
        
        self.next = self #set next scene
        self.toDrawTerrain, self.collider, self.doorCollider = DrawTerrain(screen, self.positions, self.terrain, self.Data) #set terrain image and collider
        self.inGameMenu = igMenu #set toggleable var for in-game menu
        self.GO = False
        self.playerCollisionCooldown = 0
        self.timer = timer
        self.score = score
        
        if timer != -1:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/sounds/ambient.ogg")
            pygame.mixer.music.play(-1, self.timer, 500)
        
    def tick(self, screen:pygame.surface.Surface, events:list[pygame.event.Event], keys) -> None:
        """
        tick fucntion will be called every tick of the game
        
        screen : the screen where we have to render everything
        events : the list of pygame events, same as pygame.event.get()
        keys : list of pressed keys
        
        return Nothing
        """
        #actualize the Data
        self.Data = GetData("data/app.json")
        
        #if the user press the igMenu key then toggle the menu interface
        if self.player.features["health"] <= 0: self.GO = True #make the game over
        if keys[eval("pygame.K_" + self.Data["inputs"]["igMenu"])] and self.inGameMenu and testEvent([pygame.KEYDOWN], events):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/sounds/ambient.ogg")
            pygame.mixer.music.play(-1, self.timer, 500)
        elif keys[eval("pygame.K_" + self.Data["inputs"]["igMenu"])] and testEvent([pygame.KEYDOWN], events):
            self.timer = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/sounds/menu.ogg")
            pygame.mixer.music.play(-1)
        if keys[eval("pygame.K_" + self.Data["inputs"]["igMenu"])] and testEvent([pygame.KEYDOWN], events): self.inGameMenu = not self.inGameMenu
        
        #if its game over then do game over outro loop
        if self.GO:
            self.Game_Over(screen, events)
        
        elif self.inGameMenu: #if the user is on the igMenu
            self.__IGMenu(screen, events) #render it
        
        else: #else do the game normal game tick
            screen.blit(self.toDrawTerrain, (0, 0)) #blit the terrain first in bg
            
            #do mines tick and update their state
            newListOfMines = []
            for mine in self.mines:
                newMine = mine.tick(screen)
                self.score += 15
                if not newMine == None : newListOfMines.append(newMine) ; self.score -= 15
            
             #do flyers tick and update their state
            newListOfFlyers = []
            for flyer in self.flyers:
                newFlyer, self.bullets = flyer.tick(screen, self.player, self.bullets, self.collider)
                self.score += 25
                if not newFlyer == None : newListOfFlyers.append(newFlyer) ; self.score -=25
            
            
             #do explosions tick and update their state
            newListOfExplosions = []
            for explosion in self.explosions:
                newExplosion = explosion.tick(screen)
                if not newExplosion == None : newListOfExplosions.append(newExplosion)
            
             #do bullets tick and update their state
            newListOfBBullets = []
            for bullet in self.bullets:
                newBullet = bullet.tick(screen, self.collider)
                if not newBullet == None : newListOfBBullets.append(newBullet)
            
            #*update entities
            self.player.tick(screen, events, keys, self.collider)
            self.bullets = newListOfBBullets
            self.explosions = newListOfExplosions
            self.mines = newListOfMines
            self.flyers = newListOfFlyers
            self.mines, self.explosions, self.player, self.bullets, self.flyers, self.playerCollisionCooldown, self.score = damage_collisions(screen, self.mines, self.player, self.flyers, self.explosions, self.bullets, self.Data, self.playerCollisionCooldown, self.score)
            
            #do use tick (take the doors) if the needed button is pressed
            if keys[eval("pygame.K_" + self.Data["inputs"]["use"])] :
                self.next = useKeyPressed(screen, self)
            
            #same with shoot tick
            if keys[eval("pygame.K_" + self.Data["inputs"]["shoot"])] and testEvent([pygame.KEYDOWN], events):
                shootKeyPressed(screen, self, keys)
            
            #HUD drawing
            HUDtopLeftCorner1 = (Rescaler(10, 0), Rescaler(10, 1))
            HUDtopLeftText1 = self.HUDfont.render(str(self.score), True, (0,0,255))
            
            HUDtopLeftCorner2 = (Rescaler(50, 0), Rescaler(600, 1))
            HUDtopLeftText2 = self.HUDfont.render(str(self.player.features["health"]) + " -" + str(self.player.features["power"]), True, (251,126,20))
            HUDtopLeftText2.set_alpha(40)
            
            screen.blit(HUDtopLeftText1, HUDtopLeftCorner1)
            screen.blit(HUDtopLeftText2, HUDtopLeftCorner2)
            
            
    def __IGMenu(self, screen:pygame.surface.Surface, events:list[pygame.event.Event]) -> None: #render the in-game menu 
        """render the in game Menu

        Args:
            screen (pygame.surface.Surface): where to render this
            events (list[pygame.event.Event]): the pygame events (user inputs)
        Returns:
            Nothing
        """
        screen.blit(self.toDrawTerrain, (0, 0)) #render the background in first to set in background
        igMenuSurface = pygame.Surface(self.Data["screen"]["size"], pygame.SRCALPHA).convert_alpha()
        menuFilter = pygame.Surface(self.Data["screen"]["size"])
        menuFilter.set_alpha(128)
        menuFilter.fill((75, 75, 75))
        igMenuSurface.blit(menuFilter.convert_alpha(), (0, 0))
        
        #~control button
        controlButtonTLCorner = (Rescaler(50, 0), Rescaler(500, 1)) #set the topleft corner of the button
        self.controlButtonSurface = self.controlText.get_rect(topleft=controlButtonTLCorner) #get the whole text surface
        if self.controlButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.controlText = self.font.render("control", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Controls(screen, self.Data, self) #pass to control scene (state = 2 in mainloop)
        else: 
            self.controlText = self.font.render("control", True, (200, 200, 200)) #set the text to his normal color
        igMenuSurface.blit(self.controlText, controlButtonTLCorner) #render the text
        
        #~MENU button
        menuButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.menuButtonSurface = self.MenuText.get_rect(topleft=menuButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.MenuText = self.font.render("Menu", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.next = Menu(screen, self.Data) #pass to control scene (state = 2 in mainloop)
        else: 
            self.MenuText = self.font.render("Menu", True, (200, 200, 200)) #set the text to his normal color
        igMenuSurface.blit(self.MenuText, menuButtonTLCorner) #render the text
        
        screen.blit(igMenuSurface, (0, 0))

    def Game_Over(self, screen:pygame.surface.Surface, events:list[pygame.event.Event]) -> None:
        """display the game over screen

        Args:
            screen (pygame.surface.Surface): where to render it
            events (list[pygame.event.Event]): the pygame events (user inputs)
        Returns:
            Nothing
        """
        screen.blit(self.toDrawTerrain, (0, 0)) #render the background in first to set in background
        GameOverSurface = pygame.Surface(self.Data["screen"]["size"], pygame.SRCALPHA).convert_alpha()
        
        GameOverFilter = pygame.Surface(self.Data["screen"]["size"])
        GameOverFilter.set_alpha(128)
        GameOverFilter.fill((75, 75, 75))
        GameOverSurface.blit(GameOverFilter.convert_alpha(), (0, 0))
        
        GameOverText = self.font.render("GAME OVER", True, (250, 5, 5))
        GameOverSurface.blit(GameOverText.convert_alpha(), (Rescaler(35, 1), Rescaler(250, 0)))
        
        screen.blit(GameOverSurface, (0, 0))
        pygame.display.update()
        
        time.sleep(1.5)
        
        screen.blit(self.toDrawTerrain, (0, 0)) #render the background in first to set in background
        GameOverSurface = pygame.Surface(self.Data["screen"]["size"], pygame.SRCALPHA).convert_alpha()
        
        GameOverFilter = pygame.Surface(self.Data["screen"]["size"])
        GameOverFilter.set_alpha(128)
        GameOverFilter.fill((75, 75, 75))
        GameOverSurface.blit(GameOverFilter.convert_alpha(), (0, 0))
        
        GameOverText = self.font.render("GAME OVER", True, (250, 5, 5))
        GameOverSurface.blit(GameOverText.convert_alpha(), (Rescaler(35, 1), Rescaler(250, 0)))
        
        GameOverIndicTextFont = pygame.font.Font("assets/font2.ttf", Rescaler(20))
        GameOverIndicText = GameOverIndicTextFont.render("press any key to continue", True, (255, 255, 255))
        GameOverSurface.blit(GameOverIndicText, (Rescaler(600, 1), Rescaler(10, 0)))
        
        screen.blit(GameOverSurface, (0, 0))
        pygame.display.update()
        pygame.event.get()
        
        GO = True
        while GO:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: GO = False
                
        self.next = Menu(screen, self.Data)

class Controls: #to handle the control menu display
    
    def __init__(self, screen:pygame.surface.Surface, Data:dict, returnScene:Menu|Game, timer:float=0.00) -> None: #called when initializing this class
        """
        initialize the class
        
        Args:
            screen  (pygame.surface.Surface) : where to display the menu
            Data (dict) : the app data (data/app.json file)
            timer (int): the time where to start for the music
            returnScene (Menu|Game): the scene to process after leaving this
        Returns:
            Nothing
        """
        self.returnScene = returnScene #save the scene to call at the end of the control scene
        self.Data = Data.copy() #save Data
        self.next = self #set the next scene to itself
        self.font1 = pygame.font.Font("assets/font.ttf", Rescaler(125)) #set the fonts
        self.font2 = pygame.font.Font("assets/font2.ttf", Rescaler(25))

        #parts of tick function to avoid errors with self call
        self.returnText = self.font1.render("Return", True, (250, 250, 250)) #set the text of the ExitButton

    def tick(self, screen:pygame.surface.Surface, events:list[pygame.event.Event], keys:Sequence[bool]) -> None: #called every active tick
        """do the control ticks

        Args:
            screen (pygame.surface.Surface): where to display the Controls scene
            events (list[pygame.event.Event]): the pygame events (user inputs)
            keys (Sequence[bool]): all the pressed keys

        Returns:
            Nothing
        """
        self.Data = GetData("data/app.json") #actualize the data
        #~background image
        self.bg = pygame.image.load("assets/used/bigdoor23.png").convert() #load the bg control image
        self.bg = pygame.transform.scale(self.bg, self.Data["screen"]["size"]) #rescale the image to the size of the screen
        screen.blit(self.bg, (0, 0)) #print the image on the screen

        #~RETURN button
        returnButtonTLCorner = (Rescaler(50, 0), Rescaler(600, 1)) #set the topleft corner of the button
        self.menuButtonSurface = self.returnText.get_rect(topleft=returnButtonTLCorner) #get the whole text surface
        if self.menuButtonSurface.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): #if the mouse hoover the text
            self.returnText = self.font1.render("Return", True, (250, 250, 250)) #make it lighter
            if testEvent([pygame.MOUSEBUTTONDOWN], events): #if the user click
                self.returnScene.next = self.returnScene #modify the .next atribute of the return scene beccause that was the control scene
                self.next = self.returnScene #pass to the last scene
        else: 
            self.returnText = self.font1.render("Return", True, (200, 200, 200)) #set the text to his normal color
        screen.blit(self.returnText, returnButtonTLCorner) #render the text
        
        #~right button 
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
            
            
        #~left button
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
            
        #~jump button
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
            
        #~crouch button
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
        
        #~shoot button
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
        
        #~use button
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
        
        #~ingameMenu button
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
