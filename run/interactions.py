import pygame
from run.entities import *

def damage_collisions(screen, mines, player, flyers, explosions, bullets, Data):
    for mine in mines:
        if pygame.sprite.collide_rect(player, mine):
            mine.features["health"] = 0
            newExplosion = Explosion(screen, (mine.position[0]-0.5*Data["screen"]["size"][0]/40, mine.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
            explosions.extend([newExplosion])
            player.features["health"] -= newExplosion.features["damage"]
            mines.remove(mine)
            
    return mines, explosions, player

def useKeyPressed(screen, player, bullets, scene):
    pass