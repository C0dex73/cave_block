#use to execute commands with arguments relatively to the objects
#called by many scripts

class DataExecs: #for Data objects [json files]
    def tranform(strCommand, Data): #transform string into executable commands
        command = "" #the final command (we'll add substrings to this)
        i = 0
        while i < len(strCommand): #for all the characters in strCommand
            if strCommand[i] == "$" and strCommand[i+1] == "{": #if it's the start of an arg ('${')
                arg = strCommand[i+2:strCommand.find("}", i+2)] #take the arg
                arg.replace("'", '"') #replace the ' in json to " in python for the syntax

                command += str(Data[arg]) #add the value of the arg to the command
                i = strCommand.find("}", i+2) #set the search to after the arg
            else :
                command += strCommand[i] #add the char
            i += 1 #increment i
        print(strCommand[i-1])
        print(command)
        return command #return the command for the execution of it