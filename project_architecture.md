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
    si scenecourante.next == scene courante :
        appel de la classe courante (args : [screen, inputs]) (utilisation d'une fonction tick() ?) {va dépendre de state (0:null, 1:menu, 2:game 3:gameOverScreen, 4:Intro)}
    sinon
        appel de la classe courante (args : [screen, inputs]) (utilisation d'une fonction __init__()) {va dépendre de state (0:null, 1:menu, 2:game 3:gameOverScreen, 4:Intro)}
    classe courante = classe courante.next

classe Menu:
    def __init__(screen):
        def des variables
        positionnement des objects
-
    def tick(screen, input):
        si la souris est sur un Tbutton : l'éclaircir et si la souris clique, executer la fonction associée à ce Tbutton
    

classe Game:
    def __init__(screen):
        def des variables
        positionnement des objects
-
    def tick():
        bouger les entités (entities.json)
        si collision retirer les points de vie associés
        si tir : ajouter bullet