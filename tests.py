def tranform(str, Data):
    start = 0
    command = ""
    while "${" in str[start:len(str)+1]:
        arg = str[str.find("${", start)+2:str.find("}", start)]
        command += str[start:str.find("${", start)] + Data[str[str.find("${", start)+2:str.find("}", start)]]
        start = str.find("}", start) + 1
    print(command)

if __name__ == "__main__":
    tranform("this is a ${test} in a ${string}", dict)