#CaveBlock

Name : caveblock
style : metroid, mario,... in a spaceraft (around the earth ?)

MENU (first window):
    Background : ./caveBlock/pictures/menu.gif
    Interactions :  EXIT button
                    LOAD button
                    NEW button
                    OPTIONS button

fonctionnement :

Lancement du jeu,
initialisation de la boucle, de l'écran et de ses propriété
initialisation du menu
state = 0
mainloop :
    event checking
    appel de la classe courante (args : [screen, inputs]) (utilisation d'une fonction tick() ?) {va dépendre de state (0:null, 1:menu, 2:game, 3:gameOverScreen, 4:Intro)}
