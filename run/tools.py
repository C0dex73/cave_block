import json
import random
import pygame
import os

def GetData(jsonFilePath):
    with open(jsonFilePath, 'r') as jsonFile:
        return json.load(jsonFile)
    
def SetData(data, jsonFilePath):
    with open(jsonFilePath, 'w') as jsonFile:
        json.dump(data, jsonFile)

def Rescaler(pos, axis=-1):
    Data = json.load(open("data/app.json", "r"))
    actualResolution = Data["screen"]["size"]
    betaResolution = [1080, 720]
    
    if axis == -1 : axis = actualResolution.index(min(actualResolution))
    
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

def TerrainGen(Data):
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
    
    for line in range(20): #for each line (20 = number of lines)
        for column in range(40): #for each block (40 = number of columns)
            
            #if its a border block 
            if column == 0 or column == 40-1 or line == 0 or line == 20-1: #20 = number of lines and 40 = number of columns
                bit += random.randint(-1, 1) #add or remove 1 to the lenght of the borders                   
                if bit == -1 :
                    bit = 0
                if bit >= 20/4 : #20 = number of lines
                    bit = int(20/4-1) #20 = number of lines
                terrain[line][column] = "1" #set the border
            
            if column == 0: #if it's the left border then add the border lenght
                for i in range(column, column + bit+1):
                    terrain[line][i] = "1"
                        
            if column == 40-1: #if it's the right border then add the border lenght (40 = number of columns)
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
                    terrain[line][column] += ";" + "/"
                elif percent <= 10: #5% chance to be a theme vent with the assocate background for transparent parts
                    terrain[line][column] += ";" + theme + "a;//" + theme
                elif percent <= 45: #35% chance to be a crate
                    terrain[line][column] += ";" + theme + "C"
                elif percent <= 80: #35% chance to be a basic background (with the assocate theme)
                    terrain[line][column] += ";" + theme
                else: #20% chance to be a decorated crate
                    terrain[line][column] += ";" + theme + "C+"
                    
    positions = {
        "player" : (0, 0),
        "mines" : [],
        "flyers" : []
    }
    find = False
    for terrainLine in range(20 + 1): #20 = number of lines
        line = 20 - terrainLine -2 #20 = number of lines
        for case in range(10):
            if terrain[line][case].__contains__("0") and terrain[line+1][case].__contains__("0") and terrain[line][case+1].__contains__("0") and terrain[line+1][case+1].__contains__("0"):
                find = True
                terrain[line][case] = theme + "DD"
                terrain[line+1][case] = "A"
                terrain[line+1][case+1] = "A"
                terrain[line][case+1] = "A"
                positions["player"] = (case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20) #40 = number of columns
                break
        if find:
            break
    find = False
    for terrainCase in range(10):
        case = 40 - terrainCase -2 #40 = number of columns
        for terrainLine in range(20 + 1): #20 = number of lines
            line = 20 - terrainLine -2 #20 = number of lines
            if terrain[line][case].__contains__("0") and terrain[line+1][case].__contains__("0") and terrain[line][case+1].__contains__("0") and terrain[line+1][case+1].__contains__("0"):
                find = True
                terrain[line][case] = theme + "DF"
                terrain[line+1][case] = "A"
                terrain[line+1][case+1] = "A"
                terrain[line][case+1] = "A"
                break
        if find:
            break
        
        for mine in range(random.randint(Data["entities"]["mine"]["genMin"], Data["entities"]["mine"]["genMax"])-1):
            case, line = 0, 0
            while not terrain[line][case].__contains__("0") : case, line = random.randint(0, len(terrain[line])-1), random.randint(0, len(terrain)-1)
            positions["mines"].append((case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20))
            
        for flyer in range(random.randint(Data["entities"]["mine"]["genMin"], Data["entities"]["mine"]["genMax"])):
            case, line = 0, 0
            while not terrain[line][case].__contains__("0") : case, line = random.randint(0, len(terrain[line])-1), random.randint(0, len(terrain)-1)
            positions["flyers"].append((case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20))
            

    return terrain, positions #return the generated terrain
    
def DrawTerrain(screen, CodedTerrain, Data, saveFilePath=None): #TODO : implement the seed mechanism and the colliders
    finalTerrainSurface = pygame.Surface(Data["screen"]["size"]) #* this work tho
    finalColliderSurface = pygame.sprite.Group()
    doorColliderSurface = pygame.sprite.Sprite()
    if saveFilePath is not None:
        CodedTerrain = json.load(open(saveFilePath, 'r'))
        
    Decoder = Data["terrainDecoder"] #get the decoder data
    imageList = os.listdir("assets/used") #get all the assets
    
    for line in range(len(CodedTerrain)):
        for case in range(len(CodedTerrain[line])): #for each block
            for blockCalc in CodedTerrain[line][case].split(';'): #for each calc in a block
                finalImageList = [] #init or reset the finalImageList
                for image in imageList: #for each texture
                    for acceptedStr in Decoder[blockCalc]: #if it correspond to an accepted texture
                        if image.__contains__(acceptedStr):
                            finalImageList.append(image) #add it to finalImageList
                #set the size (units = blocks)
                size = [1, 1]
                if blockCalc.__contains__("D"): size = [2, 2] #if it's a door, it's 2 times bigger
                
                #then print it
                caseImage = pygame.image.load("assets/used/" + random.choice(finalImageList)).convert_alpha()
                caseImage = pygame.transform.scale(caseImage, (size[0] * Data["screen"]["size"][0] / 40, size[1] * Data["screen"]["size"][1] / 20)) #40 = number of columns and 20 = number of rows
                if blockCalc.__contains__("DF"): doorColliderSurface.rect = caseImage.get_rect(topleft=(case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20))
                finalTerrainSurface.blit(caseImage, (case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20)) #40 = number of columns and 20 = number of rows

                #and finally set the collider logic
                if blockCalc == "1":
                    blockSprite = pygame.sprite.Sprite()
                    blockSprite.rect = pygame.Rect(case*Data["screen"]["size"][0]/40, line*Data["screen"]["size"][1]/20, size[0] * Data["screen"]["size"][0] / 40, size[1] * Data["screen"]["size"][1] / 20) #40 = number of columns and 20 = number of rows
                    finalColliderSurface.add(blockSprite) # type: ignore
                    
                    
    return finalTerrainSurface, finalColliderSurface, doorColliderSurface