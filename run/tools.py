import json
import random
import pygame
import os

def Rescaler(pos, axis):
    Data = json.load(open("data/app.json", "r"))
    actualResolution = Data["screen"]["size"]
    betaResolution = [1080, 720]
    
    return round(actualResolution[axis] * pos / betaResolution[axis])
            
def testEvent(Tevents, Revents):
    if len(Tevents) == 1: #if there is only one event to ckeck
        for e in Revents: #for each event appenning
            if e.type == Tevents[0]: #if there are the event to check return true else return false
                return True
        return False
    returnVar = [] #the final value to return at the end
    for event in Tevents: #for each event to check
        for e in Revents: #for each event appenning
            if e.type == event: #if there are the event to check return true for this event else return false by addind the event to the final list
                returnVar.append({str(event) : True})
        returnVar.append({str(event) : False})
    return returnVar

def TerrainGen():
    #code the terrain by block with symbols
    #differents calcs is represented by differents symbols
    #there can be multiple calcs with a transparent background for example
    #there respective code will be separated by a ;
    
    terrain = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"],
               ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0","0", "0"]
               ]
    
    bit = 0
    theme = random.choice(["2", "3"]) #theme id (see app.json file)
    
    for line in range(len(terrain)):
        for column in range(len(terrain[line])): #for each block
            
            #if its a border block 
            if column == 0 or column == len(terrain[line])-1 or line == 0 or line == len(terrain)-1:
                bit += random.randint(-1, 1) #add or remove 1 to the lenght of the borders                   
                if bit == -1 :
                    bit = 0
                if bit >= len(terrain)/4 :
                    bit = int(len(terrain)/4-1)
                terrain[line][column] = "1" #set the border
            
            if column == 0: #if it's the left border then add the border lenght
                for i in range(column, column + bit+1):
                    terrain[line][i] = "1"
                        
            if column == len(terrain[line])-1: #if it's the right border then add the border lenght
                for i in range(column - bit+1, column):
                    terrain[line][i] = "1"
                        
            if line == 0: #if it's the roof then add the border lenght
                for i in range(line, line + bit+1):
                    terrain[i][column] = "1"
                if random.randint(0, 4) == 0 : #and might add a cable or a vine
                    terrain[line + bit + 1][column] = "0;*"
                        
            if line == len(terrain)-1 : #if it's the ground then add the border lenght
                for i in range(line - bit+1, line):
                    terrain[i][column] = "1"
                
            if terrain[line][column].__contains__("0"): #if its the background
                percent = random.randint(1, 100) #set percent as a variable wich will define the type of the block
                if percent <= 5: #5% chance to be a neutral vent (no theme)
                    terrain[line][column] = "/"
                elif percent <= 10: #5% chance to be a theme vent with the assocate background for transparent parts
                    terrain[line][column] = theme + "a;//" + theme
                elif percent <= 45:
                    terrain[line][column] = theme + "C"
                elif percent <= 80:
                    terrain[line][column] = theme
                else:
                    terrain[line][column] = theme + "C+"
        
    return terrain #return the generated terrain
    
def DrawTerrain(screen, CodedTerrain, Data, saveFilePath=None): #TODO : implement the seed mechanism and the colliders
    finalTerrainSurface = pygame.Surface(Data["screen"]["size"]) #* this work tho
    if saveFilePath is not None:
        CodedTerrain = json.load(open(saveFilePath, 'r'))
        
    Decoder = Data["terrainDecoder"] #get the decoder data
    imageList = os.listdir("textures/used") #get all the textures
    
    for line in range(len(CodedTerrain)):
        for case in range(len(CodedTerrain[line])): #for each block
            for blockCalc in CodedTerrain[line][case].split(';'): #for each calc in a block
                finalImageList = [] #init or reset the finalImageList
                for image in imageList: #for each texture
                    for acceptedStr in Decoder[blockCalc]: #if it correspond to an accepted texture
                        if image.__contains__(acceptedStr):
                            finalImageList.append(image) #add it to finalImageList
                            
                #then print it
                caseImage = pygame.image.load("textures/used/" + random.choice(finalImageList)).convert_alpha()
                caseImage = pygame.transform.scale(caseImage, (Data["screen"]["size"][0]/40, Data["screen"]["size"][1]/20))
                finalTerrainSurface.blit(caseImage, (case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20))
    return finalTerrainSurface