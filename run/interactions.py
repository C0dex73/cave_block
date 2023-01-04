import pygame
import run.scenes as scenes
from run.entities import *
from run.tools import Rescaler

def damage_collisions(screen, mines, player, flyers, explosions, bullets, Data):
    
    
    for mine in mines:
        if pygame.sprite.collide_rect(player, mine):
            mine.features["health"] = 0
            newExplosion = Explosion(screen, (mine.position[0]-0.5*Data["screen"]["size"][0]/40, mine.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
            explosions.extend([newExplosion])
            player.features["health"] -= newExplosion.features["damage"]
            mines.remove(mine)
            
        for bullet in bullets:
            if pygame.sprite.collide_rect(mine, bullet):
                mine.features["health"] = 0
                newExplosion = Explosion(screen, (mine.position[0]-0.5*Data["screen"]["size"][0]/40, mine.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
                explosions.extend([newExplosion])
                mines.remove(mine)
                
                bullets.remove(bullet)
            
    return mines, explosions, player, bullets

def useKeyPressed(screen, scene):    
    if pygame.sprite.collide_rect(scene.player, scene.doorCollider):
        scene = scenes.Game(screen, scene.Data, playerHealth=scene.player.features["health"])
    
    return scene

def shootKeyPressed(screen, scene, keys):
    factor = 0.5
    groundedFactor = 1
    if keys[eval("pygame.K_" + scene.Data["inputs"]["crouch"])]: groundedFactor = 0.4
    if keys[eval("pygame.K_" + scene.Data["inputs"]["left"])] and not keys[eval("pygame.K_" + scene.Data["inputs"]["right"])]: direction = -1 ; factor = 3
    else: direction = 1
    position = (scene.player.rect.centerx + factor*direction*scene.player.rect.width/2, scene.player.position[1] + Rescaler(25)*groundedFactor)
    
    if scene.player.features["power"] > 0 :
        newBullet = Bullet(position, direction, scene.Data)
        scene.bullets.append(newBullet)
        scene.player.features["power"] -= 1