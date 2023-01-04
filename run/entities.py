"""
entity hanlder module
"""
import pygame
from run.tools import Rescaler
import time
import math

class Player():
    """
    Player class that handles the health, position, movement and all the things related to the player
    """
    def __init__(self, screen, position, Data, health):
        """intialize the player class"""
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
        
        #draw the image
        playerImage = pygame.image.load("assets/used/Astro_" + str(self.imageState) + ".png").convert_alpha()
        playerImage = pygame.transform.scale(playerImage, (1*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = playerImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #generate the check sprites to check collision with the terrain
        bottomCheckSprite = pygame.sprite.Sprite()
        bottomCheckSprite.rect = pygame.Rect(self.rect.midbottom[0] - (self.rect.width - 4)/2, self.rect.midbottom[1], self.rect.width - 4, 2)
        pygame.draw.rect(screen, (255, 0, 0), bottomCheckSprite.rect)
        
        topCheckSprite = pygame.sprite.Sprite()
        topCheckSprite.rect = pygame.Rect(self.rect.midtop[0] - (self.rect.width - 4)/2, self.rect.midtop[1], self.rect.width - 4 , 2)
        pygame.draw.rect(screen, (255, 0, 0), topCheckSprite.rect)
        
        rightCheckSprite = pygame.sprite.Sprite()
        rightCheckSprite.rect = pygame.Rect(self.rect.midright[0], self.rect.midright[1] - (self.rect.height - 4)/2, 2, self.rect.height - 4)
        pygame.draw.rect(screen, (255, 0, 0), rightCheckSprite.rect)
        
        leftCheckSprite = pygame.sprite.Sprite()
        leftCheckSprite.rect = pygame.Rect(self.rect.midleft[0], self.rect.midleft[1] - (self.rect.height - 4)/2, 2, self.rect.height - 4)
        pygame.draw.rect(screen, (255, 0, 0), leftCheckSprite.rect)
        
        #add the collision checker sprites to a group
        self.checkSprites.add(bottomCheckSprite)
        self.checkSprites.add(topCheckSprite)
        self.checkSprites.add(rightCheckSprite)
        self.checkSprites.add(leftCheckSprite)
        
        self.isGrounded = False
        self.isCrouching = False
        self.oldIsCrouching = False
        
        self.features = Data["entities"]["player"].copy()
        self.features["health"] = health

    def tick(self, screen, events, keys, terrainCollider):
        """called each game tick to modify player state"""

        if self.features["health"] < 0 : self.features["health"] = 0
        #bool(Sprite()) will return True if the Sprite exists, we check if the 
        self.isGrounded = bool(pygame.sprite.spritecollideany(self.checkSprites.sprites()[0], terrainCollider))
        self.isCrouching = keys[eval("pygame.K_" + self.Data["inputs"]["crouch"])]
        
        if self.isCrouching == False and self.oldIsCrouching == True and pygame.sprite.spritecollideany(self.checkSprites.sprites()[1], terrainCollider): self.isCrouching = True
        
        #gravity
        if not self.isGrounded : self.direction.y += 0.1
        
        #toggle between crouch and normal position for the colliders
        if self.isCrouching :
            self.checkSprites.sprites()[1].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static)
            self.checkSprites.sprites()[2].rect.height = self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static)
            self.checkSprites.sprites()[2].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40/2 #type: ignore (rect not static)
            self.checkSprites.sprites()[3].rect.height = self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static)
            self.checkSprites.sprites()[3].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40/2 #type: ignore (rect not static)
        else:
            self.checkSprites.sprites()[1].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - 2*self.Data["screen"]["size"][0]/40 #type: ignore (rect not static)
            self.checkSprites.sprites()[2].rect.height = 2*self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static)
            self.checkSprites.sprites()[2].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static)
            self.checkSprites.sprites()[3].rect.height = 2*self.Data["screen"]["size"][0]/40 - 4 #type: ignore (rect not static)
            self.checkSprites.sprites()[3].rect.centery = self.checkSprites.sprites()[0].rect.centery - 2 - self.Data["screen"]["size"][0]/40 #type: ignore (rect not static)
        
        #load the image
        imagePath = "assets/used/Astro_" #constant file path
        imageSize = [1*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20] #40 and 20 if the number of lines and columns
        if self.isCrouching : 
            imagePath += "C" #add C to the path
            if self.imageState >= 4: self.imageState = 1 #same as line 117 but for crouching (only 3 images)
            imageSize[1] /= 2 #two times smaller in height
        playerImage = pygame.image.load(imagePath + str(math.floor(self.imageState)) + ".png").convert_alpha()
        playerImage = pygame.transform.scale(playerImage, imageSize) 
        self.rect = playerImage.get_rect(topleft = self.position)
        
        #get the inputs and change the movement of the player
        if keys[eval("pygame.K_" + self.Data["inputs"]["right"])] :
            self.direction.x = 1 * self.speed
        elif keys[eval("pygame.K_" + self.Data["inputs"]["left"])] :
            self.direction.x = -1 * self.speed
        else:
            self.direction.x = 0
        
        if keys[eval("pygame.K_" + self.Data["inputs"]["jump"])] and self.isGrounded: #to jump the player have to be on the ground
            self.direction.y = -4
        elif self.isCrouching:
            self.direction.x /= 2
            
        #rotate the image before direction correction
        if self.direction.x < 0: playerImage = pygame.transform.flip(playerImage, True, False)
        
        #for each check sprite if the player do a movement to go in the wall, then cancel this movement
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[1], terrainCollider) and self.direction.y < 0: self.direction.y = 0
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[0], terrainCollider) and self.direction.y > 0: self.direction.y = 0 
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[2], terrainCollider) and self.direction.x > 0: self.direction.x = 0
        if pygame.sprite.spritecollideany(self.checkSprites.sprites()[3], terrainCollider) and self.direction.x < 0: self.direction.x = 0
                
        #then move evrything and update the image
        for collider in self.checkSprites:  
            collider.rect.top += self.direction.y # type: ignore (rect not static)
            collider.rect.left += self.direction.x # type: ignore (rect not static)
            if self.Data["devMode"]: #draw it if in dev mode
                pygame.draw.rect(screen, (255, 0, 0), collider.rect) # type: ignore (rect not static)
        #take the top and left collision checkers to get the topleft corner of the image, so the position of the player
        self.position = (self.checkSprites.sprites()[3].rect.centerx, self.checkSprites.sprites()[1].rect.centery) # type: ignore (rect not static)

        #change the image of the player relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/8 per 1/10 = 10 images every 8 seconds
        if self.direction.x != 0 and time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 11, and if it's different
            self.imageState += 0.125
            if self.imageState == 5 : self.imageState = 1 #if we overflowed (no file named astro_5)
        
        screen.blit(playerImage, self.position)
        self.oldIsCrouching = self.isCrouching #shift the value of isCrouching
        
    def setPos(self, pos):
        """called to change the player position to the given one"""
        self.position = pos
        
class Mine(pygame.sprite.Sprite):
    """class to handle Mine object and all this features"""
    
    def __init__(self, screen, position, Data):
        """intialize mine class"""
        self.Data = Data.copy()
        self.imageState = 1
        #^same as line 11
        self.imageTimer = time.time_ns()//10**8 % 10
        self.position = position
        
        self.features = self.Data["entities"]["mine"].copy() #get all the mine features
    
    def tick(self, screen):
        """called each game tick"""
        
        if self.features["health"] < 0 : return None
        #load the image
        imagePath = "assets/used/MINE_" + str(math.floor(self.imageState)) + ".png"
        mineImage = pygame.image.load(imagePath).convert_alpha()
        mineImage = pygame.transform.scale(mineImage, (1*self.Data["screen"]["size"][0]/40, 1*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = mineImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/16 per 1/10 = 10 images every 16 seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 11, and if it's different
            self.imageState += 1/16
            if self.imageState == 3: self.imageState = 1 #if we overflowed (no file named MINE_3)
            
        #draw the mine if it's alive, else draw the explosion
        screen.blit(mineImage, self.position)
        return self

class Explosion(pygame.sprite.Sprite):
    """class to handle mine explosion effect"""
    
    def __init__(self, screen, position, Data):
        """initialize the class"""
        self.Data = Data.copy()
        self.position = position
        self.imageState = 1
        #^same as line 11
        self.imageTimer = time.time_ns()//10**8 % 10
        
        self.features = Data["entities"]["explosion"].copy()
        
    def tick(self, screen):
        """called each game tick"""
        
        #load the image
        imagePath = "assets/used/explosion_" + str(math.floor(self.imageState)) + ".png"
        explosionImage = pygame.image.load(imagePath).convert_alpha()
        explosionImage = pygame.transform.scale(explosionImage, (2*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = explosionImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/3 per 1/10 = 10 images every 3 seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 11, and if it's different
            self.imageState += 1/3
            if self.imageState >= 6 : return None
        
        screen.blit(explosionImage, self.position)
        return self
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, Data, Enemy=False):
        self.position = position
        self.enemy = Enemy
        self.direction = direction
        self.image = pygame.image.load("assets/used/laser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (Rescaler(40, 0), Rescaler(20, 1)))
        self.rect = self.image.get_rect(topleft=self.position)
        self.features = Data["entities"]["bullet"].copy()
        
    def tick(self, screen, terrainCollider):
        if pygame.sprite.spritecollideany(self, terrainCollider): return None
        else: 
            screen.blit(self.image, self.position)
            self.rect.topleft = self.position #type: ignore (rect not static)
            
            self.position = (self.direction * self.features["speed"] + self.position[0], self.position[1])
            
            return self
        
class Flyer(pygame.sprite.Sprite):
    """class to handle flyer object and all this features"""
    
    def __init__(self, screen, position, Data):
        """intialize flyer class"""
        self.Data = Data.copy()
        self.imageState = 1
        #^same as line 11
        self.imageTimer = time.time_ns()//10**8 % 10
        self.position = position
        
        self.features = self.Data["entities"]["flyer"].copy() #get all the mine features
    
    def tick(self, screen, player, bullets):
        """called each game tick"""
        if self.features["health"] <= 0 : return None
        #load the image
        imagePath = "assets/used/FLYER_" + str(math.floor(self.imageState)) + ".png"
        flyerImage = pygame.image.load(imagePath).convert_alpha()
        flyerImage = pygame.transform.scale(flyerImage, (1*self.Data["screen"]["size"][0]/40, 1*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = flyerImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and column
        
        #change the image of the mine relatyvely to the time passed
        #every 1/10 second, we add 1/8 to the image state
        #so 1/2 per 1/10 = 5 images every seconds
        if time.time_ns()//10**8 % 10 != self.imageTimer: #^same calcul as line 11, and if it's different
            self.imageState += 1/2
            if self.imageState == 5: self.imageState = 1 #if we overflowed (no file named MINE_3)
            
        if player.position[1] < self.position[1] : flyerImage = pygame.transform.flip(flyerImage, True, False)
            
        #draw the mine if it's alive, else draw the explosion
        screen.blit(flyerImage, self.position)
        return self