import pygame
from run.tools import Rescaler
import time
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, position, Data):
        self.Data = Data
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
        playerImage = pygame.image.load("textures/used/Astro_" + str(self.imageState) + ".png").convert_alpha()
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
        
        

    def tick(self, screen, events, keys, terrainCollider):
        
        #bool(Sprite()) will return True if the Sprite exists, we check if the 
        isGrounded = bool(pygame.sprite.spritecollideany(self.checkSprites.sprites()[0], terrainCollider))
        
        #draw the image
        playerImage = pygame.image.load("textures/used/Astro_" + str(math.floor(self.imageState)) + ".png").convert_alpha()
        playerImage = pygame.transform.scale(playerImage, (1*self.Data["screen"]["size"][0]/40, 2*self.Data["screen"]["size"][1]/20)) #40 and 20 if the number of lines and columns
        self.rect = playerImage.get_rect(topleft = self.position) #40 and 20 if the number of lines and columns
        
        #get the inputs and change the movement of the player
        if keys[eval("pygame.K_" + self.Data["inputs"]["right"])] :
            self.direction.x = 1 * self.speed
        elif keys[eval("pygame.K_" + self.Data["inputs"]["left"])] :
            self.direction.x = -1 * self.speed
        else:
            self.direction.x = 0
        
        if keys[eval("pygame.K_" + self.Data["inputs"]["jump"])] :
            self.direction.y = -1 * self.speed
        elif keys[eval("pygame.K_" + self.Data["inputs"]["crouch"])] :
            self.direction.y = 1
        else:
            self.direction.y = 0
            
        #rotate the image before direction correction
        if self.direction.x < 0: playerImage = pygame.transform.flip(playerImage, True, False)
        
        #for each collider detection face
        for collider in self.checkSprites:
            if self.Data["devMode"]: #draw it if in dev mode
                pygame.draw.rect(screen, (255, 0, 0), collider.rect) # type: ignore (rect not static)
            if pygame.sprite.spritecollideany(collider, terrainCollider): #if there is collision
                # locate wich face collided with the terrain by checking the distance between the center of the check collider and the center of the player
                colliderDelta = tuple(map(lambda i, j: i - j, collider.rect.center, self.rect.center)) # type: ignore (rect not static) 
                #?What are we doing ?
                #*we check between 2 and -2 for 0 due to the actualisation time, the colliders are a bit late when the player moves
                #*we also check the direction to be sure the collision is due to this type of movements
                #!for exemple if the player go right, he can also be colliding with the floor, then he can't jump anymore and that's a bug
                if colliderDelta[0] <= 2 and colliderDelta[0] >= -2 and colliderDelta[1] < 0 and self.direction.y < 0: #if dx = 0 and dy < 0 then its the top (the y axis is reversed : 0;0 is topleft)
                    self.direction.y = 0
                if colliderDelta[0] <= 2 and colliderDelta[0] >= -2 and colliderDelta[1] > 0 and self.direction.y > 0: #if dx = 0 and dy > 0 then its the bottom (the y axis is reversed : 0;0 is topleft)
                    self.direction.y = 0
                if colliderDelta[1] <= 2 and colliderDelta[1] >= -2 and colliderDelta[0] > 0 and self.direction.x > 0: #if dx > 0 and dy = 0 then its the 
                    self.direction.x = 0
                if colliderDelta[1] <= 2 and colliderDelta[1] >= -2 and colliderDelta[0] < 0 and self.direction.x < 0:
                    self.direction.x = 0
                
        #then move evrything and update the image
        for collider in self.checkSprites:  
            collider.rect.top += self.direction.y # type: ignore (rect not static)
            collider.rect.left += self.direction.x # type: ignore (rect not static)
        self.position += self.direction
        
        
        screen.blit(playerImage, self.position)
        
        
        if self.direction.x != 0 and time.time_ns()//10**8 % 10 != self.imageTimer:
            self.imageState += 0.125
            if self.imageState == 5 : self.imageState = 1
        