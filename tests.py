import random
import json
import pygame

pygame.init()
sur_obj=pygame.display.set_mode((400,300))
pygame.display.set_caption("Keyboard_Input")

while True:
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            exit()
    sur_obj.fill((255, 255, 255))
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[eval("pygame.K_KP0")] : print("0")