class DataExecs:
    def tranform(str, Data):
        start = 0
        while "${" in str[start:len(str)+1]:
            arg = str[str.find("${", start)+2:str.find("}", start)]
            str[str.find("${", start):str.find("}", start)] = arg
            start = str.find("}", start) + 1