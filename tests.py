strings = ["12", "34", "56", "78", "910", "1112"]
for string in strings:
    for char in string:
        if char == "1" or char == "5":
            print(string)
            break
    