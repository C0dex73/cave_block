class DataExecs:
    def tranform(strCommand, Data):
        strCommand = strCommand.replace("'", '"')
        start = 0
        command = ""
        while "${" in strCommand[start:len(strCommand)+1]:
            args = strCommand[strCommand.find("${", start)+2:strCommand.find("}", start)]
            print(args)
            command += strCommand[start:strCommand.find("${", start)] + str(Data[strCommand[strCommand.find("${", start)+2:strCommand.find("}", start)]])
            start = strCommand.find("}", start+1)
        print(strCommand[start])
        command += strCommand[start:len(strCommand)+1]
        return command