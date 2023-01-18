"""
entity hanlder module
"""
import pygame
from run.tools import *
from typing import Sequence
import time
import math

class Player(pygame.sprite.Sprite):
    """
    Player class that handles the health, position, movement and all the things related to the player
    """
    def __init__(self, screen:pygame.surface.Surface, position:tuple[int], Data:dict, health:int) -> None:
        """initialize the player
        
        Args:
            screen (pygame.surface.Surface) : where to display the player
            position (tuple[int]) : the start position of the player
            Data (dict) : the data from app.json
        Return:
            Nothing 
        """
        self.Data = Data.copy()
        self.speed = Data["entities"]["player"]["speed"]
        self.imageState = 1
        #? what is the line below doing ?
        #*take the time in nanoseconds,
        #*and //10**8 to get the time in milliseconds by returning the quotient of the division by 10^8.
        #*then take the digit by returning the rest of the division by 10
        self.imageTimer = time.time_ns()//10**8 % 10
        self.position = position
        self.direction = pygame.math.Vector2(0, 0)
        self.checkSprites = pygame.sprite.Group()
        
        #~draw the image
        playerImage = pygame.image.load("assets/used/Astro_" + str(self.imageState) + ".png").convert_alpha()
        playerImage = pygame.transform.scale(playerImage, (1*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = playerImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #^generate the check sprites to check collision with the terrain
        #~BOTTOM CHECKER
        bottomCheckSprite = pygame.sprite.Sprite()
        bottomCheckSprite.rect = pygame.Rect(self.rect.midbottom[0] - (self.rect.width - 4)/2, self.rect.midbottom[1], self.rect.width - 4, 2)
        pygame.draw.rect(screen, (255, 0, 0), bottomCheckSprite.rect)
        
        #~TOP CHECKER
        topCheckSprite = pygame.sprite.Sprite()
        topCheckSprite.rect = pygame.Rect(self.rect.midtop[0] - (self.rect.width - 4)/2, self.rect.midtop[1], self.rect.width - 4 , 2)
        pygame.draw.rect(screen, (255, 0, 0), topCheckSprite.rect)
        
        #~RIGHT CHECKER
        rightCheckSprite = pygame.sprite.Sprite()
        rightCheckSprite.rect = pygame.Rect(self.rect.midright[0], self.rect.midright[1] - (self.rect.height - 4)/2, 2, self.rect.height - 4)
        pygame.draw.rect(screen, (255, 0, 0), rightCheckSprite.rect)
        
        #~LEFT CHECKER
        leftCheckSprite = pygame.sprite.Sprite()
        leftCheckSprite.rect = pygame.Rect(self.rect.midleft[0], self.rect.midleft[1] - (self.rect.height - 4)/2, 2, self.rect.height - 4)
        pygame.draw.rect(screen, (255, 0, 0), leftCheckSprite.rect)
        
        #add each collision checker sprites to a group
        self.checkSprites.add(bottomCheckSprite)
        self.checkSprites.add(topCheckSprite)
        self.checkSprites.add(rightCheckSprite)
        self.checkSprites.add(leftCheckSprite)
    
        #~state bools        
        self.isGrounded = False
        self.isCrouching = False
        self.oldIsCrouching = False
        
        #~take the properties of the player object from the data
        self.features = Data["entities"]["player"].copy()
        self.features["health"] = health

    def tick(self, screen:pygame.surface.Surface, events:list[pygame.event.Event], keys:Sequence[bool], terrainCollider:pygame.sprite.Group) -> None:
        """do the player tick (actualisation)
        
        Args:
            screen (pygame.surface.Surface): where to display the player
            events (list[pygame.event.Event]) : the pygame events (user inputs)
            keys (Sequence[bool]) : the pressed keys
            terrainCollider (pygame.sprite.Group) : all the solid block colliders of the terrain
            
        Return:
            Nothing
        """
        #actualize the Data
        self.Data = GetData("data/app.json")
        
        #~DEV MODE (godmode)
        if self.Data["devMode"] : self.features["health"] = 100 ; self.features["power"] = 60

        #anti negative health
        if self.features["health"] < 0 : self.features["health"] = 0
        
        #~STATE BOOLS ACTUALISING
        #? why is bool here ?
        #*bool(Sprite()) will return True if the Sprite exists, we check if there is a terrain sprite that collides with the bottom checker
        self.isGrounded = bool(pygame.sprite.spritecollideany(self.checkSprites.sprites()[0], terrainCollider))
        self.isCrouching = keys[self.Data["inputs"]["crouch"]]
        
        if self.isCrouching == False and self.oldIsCrouching == True and pygame.sprite.spritecollideany(self.checkSprites.sprites()[1], terrainCollider): self.isCrouching = True
        
        #~gravity
        crouchFactor = 1
        if keys[self.Data["inputs"]["crouch"]] : crouchFactor = 4
        if not self.isGrounded : self.direction.y += self.Data["gravity"] * crouchFactor
        
        #~toggle between crouch and normal position for the colliders
        if self.isCrouching :
            self.checkSprites.sprites()[1].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[2].rect.height = self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[2].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40/2 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[3].rect.height = self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[3].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40/2 #type: ignore (rect not static) #!anti-ERROR
        else:
            self.checkSprites.sprites()[1].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - 2*self.Data["screen"]["size"][0]/40 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[2].rect.height = 2*self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[2].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[3].rect.height = 2*self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static) #!anti-ERROR
            self.checkSprites.sprites()[3].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static) #!anti-ERROR
        
        #~load the image
        imagePath = "assets/used/Astro_" #constant file path
        imageSize = [1*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20] #40 and 20 if the number of lines and columns
        if self.isCrouching : 
            imagePath += "C" #add C to the path
            if self.imageState >= 4: self.imageState = 1 #^same as line 165 but for crouching (only 3 images)
            imageSize[1] /= 2 #two times smaller in height
        playerImage = pygame.image.load(imagePath + str(math.floor(self.imageState)) + ".png").convert_alpha()
        playerImage = pygame.transform.scale(playerImage, imageSize) 
        self.rect = playerImage.get_rect(topleft = self.position)
        
        #~INPUTS
        if keys[self.Data["inputs"]["right"]] :
            self.direction.x = 1 * self.speed
        elif keys[self.Data["inputs"]["left"]] :
            self.direction.x = -1 * self.speed
        else:
            self.direction.x = 0
        
        if keys[self.Data["inputs"]["jump"]] and self.isGrounded: #to jump the player have to be on the ground
            self.direction.y = -4
        elif self.isCrouching:
            self.direction.x /= 2
            
        #rotate the image before direction correction
        if self.direction.x < 0: playerImage = pygame.transform.flip(playerImage, True, False)
        
        #~COLLISION CHEKCHERS
        #for each check sprite if the player do a movement to go in the wall, then cancel this movement
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[1], terrainCollider) and self.direction.y < 0: self.direction.y = 0
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[0], terrainCollider) and self.direction.y > 0: self.direction.y = 0 
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[2], terrainCollider) and self.direction.x > 0: self.direction.x = 0
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[3], terrainCollider) and self.direction.x < 0: self.direction.x = 0
                
                
        #~UPDATINGS IMAGE AND POSITION
        #then move everything and update the image
        for collider in self.checkSprites:  
            collider.rect.top += self.direction.y # type: ignore (rect not static) #!anti-ERROR 
            collider.rect.left += self.direction.x # type: ignore (rect not static) #!anti-ERROR
            if self.Data["devMode"]: #draw it if in dev mode
               pygame.draw.rect(screen, (255, 0, 0), collider.rect) # type: ignore (rect not static) #!anti-ERROR
        #take the top and left collision checkers to get the topleft corner of the image, so the position of the player
        self.position = (self.checkSprites.sprites()[3].rect.centerx, self.checkSprites.sprites()[1].rect.centery) # type: ignore (rect not static) #!anti-ERROR

        #~ANIMATION
        #change the image of the player relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/8 per 1/10 = 10 images every 8 seconds
        if self.direction.x != 0 and time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 27, and if it's different
            self.imageState += 0.125
            if self.imageState == 5 : self.imageState = 1 #if we overflowed (no file named astro_5)
        
        screen.blit(playerImage, self.position)
        self.oldIsCrouching = self.isCrouching #shift the value of isCrouching
        
class Mine(pygame.sprite.Sprite):
    """class to handle Mine object and all this features"""
    
    def __init__(self, screen:pygame.surface.Surface, position:tuple[int], Data:dict) -> None:
        """initialize the Explosion
                
        Args:
            screen (pygame.surface.Surface): where to display the explosion effect
            position (tuple[int]) : position of the explosion effect
            Data (dict): the app.json content
            
        Return:
            Nothing
        """
        self.Data = Data.copy()
        self.imageState = 1
        #^same as line 27
        self.imageTimer = time.time_ns()//10**8 % 10
        self.position = position
        
        self.features = self.Data["entities"]["mine"].copy() #get all the mine features
    
    def tick(self, screen:pygame.surface.Surface):
        """called each game tick
        
        Args :
            screen (pygame.surface.Surface) : where to display the explosion
            
        Return:
            self or nothing
        """
        #~actualize the Data
        self.Data = GetData("data/app.json")
        
        if self.features["health"] < 0 : return None
        #~load the image
        imagePath = "assets/used/MINE_" + str(math.floor(self.imageState)) + ".png"
        mineImage = pygame.image.load(imagePath).convert_alpha()
        mineImage = pygame.transform.scale(mineImage, (1*self.Data["screen"]["size"][0]/40, 1*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = mineImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/16 per 1/10 = 10 images every 16 seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 27, and if it's different
            self.imageState += 1/16
            if self.imageState == 3: self.imageState = 1 #if we overflowed (no file named MINE_3)
            
        #draw the mine if it's alive, else draw the explosion
        screen.blit(mineImage, self.position)
        return self

class Explosion(pygame.sprite.Sprite):
    """class to handle mine explosion effect"""
    
    def __init__(self, screen:pygame.surface.Surface, position:tuple[int], Data:dict) -> None:
        """initialize the Explosion
                
        Args:
            screen (pygame.surface.Surface): where to display the explosion effect
            position (tuple[int]) : position of the explosion effect
            Data (dict): the app.json content
            
        Return :
            Nothing
        """
        self.Data = Data.copy()
        self.position = position
        self.imageState = 1
        #^same as line 27
        self.imageTimer = time.time_ns()//10**8 % 10
        
        self.features = Data["entities"]["explosion"].copy()
        
    def tick(self, screen:pygame.surface.Surface):
        """called each game tick
        
        Args :
            screen (pygame.surface.Surface) : where to display the explosion
            
        Return:
            self or nothing
        """
        #~actualize the Data
        self.Data = GetData("data/app.json")
        
        #~load the image
        imagePath = "assets/used/explosion_" + str(math.floor(self.imageState)) + ".png"
        explosionImage = pygame.image.load(imagePath).convert_alpha()
        explosionImage = pygame.transform.scale(explosionImage, (2*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = explosionImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/3 per 1/10 = 10 images every 3 seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 27, and if it's different
            self.imageState += 1/3
            if self.imageState >= 6 : return None
        
        screen.blit(explosionImage, self.position)
        return self
    
class Bullet(pygame.sprite.Sprite):
    """class to handle a simple bullet"""
    def __init__(self, position, direction:int, Data:dict, Enemy:bool=False) -> None:
        """initialize a Bullet
        
        Args:
            position (tuple[int]) : the position of the bullet
            Data (dict): the app.json content
            Enemy (bool): True if the bullet was shoot by an enemy (non-player entity)
            
        Return:
            Nothing
        """
        self.position = position
        self.enemy = Enemy
        self.image = pygame.image.load("assets/used/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (Rescaler(40, 0), Rescaler(20, 1)))
        self.rect = self.image.get_rect(topleft=self.position)
        self.features = Data["entities"]["bullet"].copy()
        self.direction = pygame.math.Vector2(direction, 0)
        
    def tick(self, screen:pygame.surface.Surface, terrainCollider:pygame.sprite.Group):
        """do the bullet tick

        Args:
            screen (pygame.surface.Surface): where to display the bullet
            terrainCollider (pygame.sprite.Group): each solid block sprite of the terrain

        Returns:
            self | Nothing
        """
        #actualize the Data
        self.Data = GetData("data/app.json")
        if pygame.sprite.spritecollideany(self, terrainCollider): return None
        else: 
            screen.blit(self.image, self.position) #type: ignore (image not static) #!anti-ERROR
            self.rect.topleft = self.position #type: ignore (rect not static) #!anti-ERROR
            
            self.position = (self.direction.x * self.features["speed"] + self.position[0], self.position[1])
            
            return self
        
class Flyer(pygame.sprite.Sprite):
    """class to handle flyer object and all this features"""
    
    def __init__(self, screen:pygame.surface.Surface, position:tuple[int], Data):
        """intialize flyer class
        
        Args:
            screen (pygame.surface.Surface) : where to display the flyer
            position (tuple[int]) : the position of the flyer
            Data (dict) : the app.json content
            
        Return :
            self | Nothing
        """
        self.Data = Data.copy()
        self.imageState = 1
        #^same as line 27
        self.imageTimer = time.time_ns()//10**8 % 10
        self.position = position
        self.direction = pygame.math.Vector2(0, 0)
        self.shootCoolDown = 0
        
        self.features = self.Data["entities"]["flyer"].copy() #get all the mine features
    
    def tick(self, screen:pygame.surface.Surface, player:Player, bullets:list[Bullet], terrainCollider:pygame.sprite.Group):
        """do flyer tick

        Args:
            screen (pygame.surface.Surface): where to display the flyer
            player (Player): the player (user)
            bullets (list[Bullet]): all the bullets of the scene
            terrainCollider (pygame.sprite.Group): each solid block collider of the terrain

        Returns:
            self, list[Bullet] | Nothing, list[Bullet]
        """
        #actualize the Data
        self.Data = GetData("data/app.json")
        if self.features["health"] <= 0 : return None, bullets
        #load the image
        imagePath = "assets/used/FLYER_" + str(math.floor(self.imageState)) + ".png"
        flyerImage = pygame.image.load(imagePath).convert_alpha()
        flyerImage = pygame.transform.scale(flyerImage, (1*self.Data["screen"]["size"][0]/40, 1*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = flyerImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and column
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/2 per 1/10 = 5 images every seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 27, and if it's different
            self.imageState += 1/2
            if self.imageState == 5: self.imageState = 1 #if we overflowed (no file named MINE_3)
            
        if player.position[0] < self.position[0] : flyerImage = pygame.transform.flip(flyerImage, True, False)
        
        if self.shootCoolDown + 2 < time.time():
            if player.position[0] < self.position[0] :
                newBullet = Bullet(self.rect.center, -1, self.Data, Enemy=True)
            else:
                newBullet = Bullet(self.rect.center, 1, self.Data, Enemy=True)
            bullets.append(newBullet)
            self.shootCoolDown = time.time()
                
        self.position += self.features["speed"]*self.direction
        
        #draw the mine if it's alive, else draw the explosion
        screen.blit(flyerImage, self.position)
        return self, bullets