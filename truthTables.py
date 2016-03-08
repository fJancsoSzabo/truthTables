userInput = input("Please enter a boolean algebra expression\n")
output = ""
var = []
inputLen = len(userInput)
unacc = ["+", ")", chr(39)]
bracketNest = 0
bracketOpenPos = []
for n in range(inputLen):
    if userInput[n] == "+":
        output += " or "
    elif userInput[n] == "(":
        bracketOpenPos.append(len(output))
        bracketNest += 1
        output += "("
    elif userInput[n] == chr(39):
        if userInput[n-1] == ")":
            output = output[:bracketOpenPos[len(bracketOpenPos)-bracketNest]] + " not " + output[bracketOpenPos[len(bracketOpenPos)-bracketNest]:]
            bracketNest -= 1
            if n+1 < inputLen and userInput[n+1] not in unacc:
                output += " and "
        else:
            output = output[:len(output)-1] + " not " + output[len(output)-1]
            if n+1 < inputLen and userInput[n+1] not in unacc:
                output += " and "
    elif userInput[n] == ")":
        if n+1 < inputLen and userInput[n+1] != chr(39):
            bracketNest -= 1
        output += ")"
        if n+1 < inputLen:
            if userInput[n+1] not in unacc:
                output += " and "
    elif n + 1 < inputLen:
        var += userInput[n]
        output += userInput[n]
        if userInput[n+1] not in unacc:
            output += " and "
    else:
        var += userInput[n]
        output += userInput[n]
    #print(output)
    #print(bracketNest, bracketOpenPos)

#print(output)
editedOutput = ""
for char in output:
    if char not in "orandt ()":
        editedOutput += "self." + char
    else:
        editedOutput += char

var = sorted(set(var))
for item in var:
    print(item, end = "  ")

print("Function Result")

code = ""
code += ("class algExp(object):\n    def __init__(self):\n")
for item in var:
    code +=("        self." + item + " = 0\n")
code += ("        self.calculate()\n")
code += ("    def exp(self):\n        print(int(" + editedOutput + "))\n")
code += ("    def calculate(self):\n        binCount = 0\n        for item in range(" + str(2**len(var)) + "):\n")
binCountBasis = 0b1
for n in reversed(range(len(var))):
    code += ("            self." + var[n] + " = bool(binCount & " + str(bin(binCountBasis)) + ")\n")
    binCountBasis <<= 1
for n in range(len(var)):
    code += ("            print(int(self." + var[n] + "), end = " + chr(34) + chr(32) + chr(32) + chr(34) + ")\n")
code += ("            self.exp()\n")
code += ("            binCount += 1")
code += ("\ntest = algExp()")
#print(code)
exec(code)
