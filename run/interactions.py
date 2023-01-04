import pygame
import time
import run.scenes as scenes
from run.entities import *
from run.tools import Rescaler

def damage_collisions(screen, mines, player, flyers, explosions, bullets, Data, oldTime):
    
    playerCollideCheck = False
    if oldTime + 2 < time.time(): playerCollideCheck = True
    
    for mine in mines:
        if pygame.sprite.collide_rect(player, mine) and playerCollideCheck:
            oldTime = time.time()
            mine.features["health"] -= player.features["damage"]
            newExplosion = Explosion(screen, (mine.position[0]-0.5*Data["screen"]["size"][0]/40, mine.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
            explosions.extend([newExplosion])
            damageSound = pygame.mixer.Sound("assets/sounds/OOF.ogg")
            damageSound.set_volume(Data["volume"])
            damageSound.play()
            explosionSound = pygame.mixer.Sound("assets/sounds/Boom.ogg")
            explosionSound.set_volume(Data["volume"])
            explosionSound.play()
            player.features["health"] -= mine.features["damage"]
            
        for bullet in bullets:
            if pygame.sprite.collide_rect(mine, bullet):
                mine.features["health"] -= bullet.features["damage"]
                newExplosion = Explosion(screen, (mine.position[0]-0.5*Data["screen"]["size"][0]/40, mine.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
                explosions.extend([newExplosion])
                explosionSound = pygame.mixer.Sound("assets/sounds/Boom.ogg")
                explosionSound.set_volume(Data["volume"])
                explosionSound.play()
                
                bullets.remove(bullet)
                
    for flyer in flyers:
        if pygame.sprite.collide_rect(player, flyer) and playerCollideCheck:
            oldTime = time.time()
            flyer.features["health"] -= player.features["damage"]
            newExplosion = Explosion(screen, (flyer.position[0]-0.5*Data["screen"]["size"][0]/40, flyer.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
            explosions.extend([newExplosion])
            damageSound = pygame.mixer.Sound("assets/sounds/OOF.ogg")
            damageSound.set_volume(Data["volume"])
            damageSound.play()
            explosionSound = pygame.mixer.Sound("assets/sounds/Boom.ogg")
            explosionSound.set_volume(Data["volume"])
            explosionSound.play()
            player.features["health"] -= flyer.features["damage"]
            
        for bullet in bullets:
            if pygame.sprite.collide_rect(flyer, bullet):
                flyer.features["health"] -= bullet.features["damage"]
                newExplosion = Explosion(screen, (flyer.position[0]-0.5*Data["screen"]["size"][0]/40, flyer.position[1]-0.5*Data["screen"]["size"][1]/20), Data)
                explosions.extend([newExplosion])
                explosionSound = pygame.mixer.Sound("assets/sounds/Boom.ogg")
                explosionSound.set_volume(Data["volume"])
                explosionSound.play()
                
                bullets.remove(bullet)
        
    return mines, explosions, player, bullets, flyers, oldTime

def useKeyPressed(screen, scene):    
    if pygame.sprite.collide_rect(scene.player, scene.doorCollider):
        scene = scenes.Game(screen, scene.Data, timer=-1, playerHealth=scene.player.features["health"])
    
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
        shootSound = pygame.mixer.Sound("assets/sounds/Piou_piou.ogg")
        shootSound.set_volume(scene.Data["volume"])
        shootSound.play()
        scene.bullets.append(newBullet)
        scene.player.features["power"] -= 1