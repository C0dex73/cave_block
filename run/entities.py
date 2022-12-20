import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, Data, pos):
        self.image = pygame.Surface((Data["screen"]["size"][0]/40, 2*Data["screen"]["size"][1]/20))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
    
    def get_inputs(self, screen, keys, events, Data):
        
        if keys[eval("pygame.K_" + Data["inputs"]["right"])] : 
            self.direction.x = 1
        elif keys[eval("pygame.K_" + Data["inputs"]["left"])] :
            self.direction.x = -1
        else :
            self.direction.x = 0
            
    def update(self, screen):
        self.rect.x += self.direction.x #type: ignore
        
    
class FlyMachine:
    def __init__(self, screen):
        pass
    
    def tick(self, screen):
        pass
    
class Mine:
    def __init__(self, screen):
        pass
    
    def tick(self, screen):
        pass