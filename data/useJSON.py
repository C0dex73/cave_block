#========== JSON manipulating file ==========
#
# - called a bit everywhere
# - call nothing else than the json library
#
import json #library to manipulate JSON files

class useJSON:
    def Get(path): # to convert JSON to python dictionary
        with open(path, 'r') as JSONFile: #'with' is used to not let the file open after reading it
            data = json.load(JSONFile) #convert with the json library
        return data #return the data dictionary