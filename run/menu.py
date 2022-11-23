#==========MENU CLASS FOR THE MENU DISPLAYING==========
#
# - called by main.py when the game start
# - call differents levels like tutorial.py or game.py when executed
#
import pygame
import random
import math
from data.useJSON import useJSON
from run.utils.execs import DataExecs

class Menu:
    def __init__(self, screen): #called at the beginning to initialize the menu displaying
        self.Data = useJSON.Get("data/menu.json")
        for component in self.Data["components"]: #load all the components of the MENU window
            pass #TODO : implement execs n stuff here