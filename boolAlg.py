class boolAlg (object):
    def __init__(self, userInput, output):
        self.input = userInput
        self.output = ""
        self.var = []
        self.inputLen = len(userInput)
        self.functionVal = []
        self.parse()
        self.calc(output)

    def parse(self):
        unacc = ["+", ")", chr(39)]
        bracketNest = 0
        bracketOpenPos = []
        for n in range(self.inputLen):
            if self.input[n] == "+":
                self.output += " or "
            elif self.input[n] == "(":
                bracketOpenPos.append(len(self.output))
                bracketNest += 1
                self.output += "("
            elif self.input[n] == chr(39):
                if self.input[n-1] == ")":
                    self.output = self.output[:bracketOpenPos[len(bracketOpenPos)-bracketNest]] + " not " + self.output[bracketOpenPos[len(bracketOpenPos)-bracketNest]:]
                    bracketNest -= 1
                    if n+1 < self.inputLen and self.input[n+1] not in unacc:
                        self.output += " and "
                else:
                    self.output = self.output[:len(self.output)-1] + " not " + self.output[len(self.output)-1]
                    if n+1 < self.inputLen and self.input[n+1] not in unacc:
                        self.output += " and "
            elif self.input[n] == ")":
                if n+1 < self.inputLen and self.input[n+1] != chr(39):
                    bracketNest -= 1
                self.output += ")"
                if n+1 < self.inputLen:
                    if self.input[n+1] not in unacc:
                        self.output += " and "
            elif n + 1 < self.inputLen:
                self.var += self.input[n]
                self.output += self.input[n]
                if self.input[n+1] not in unacc:
                    self.output += " and "
            else:
                self.var += self.input[n]
                self.output += self.input[n]
        self.var = sorted(set(self.var))
        
    def calc(self, output):
        if output:
            for item in self.var:
                print(item, end = "  ")

            print("Function Result")

        code = "def function():\n"
        code += ("    ret = []\n")
        for item in self.var:
            code +=("    " + item + " = 0\n")
        code += "    binCount = 0\n    for item in range(" + str(2**len(self.var)) + "):\n"
        binCountBasis = 0b1
        for n in reversed(range(len(self.var))):
            code += ("        " + self.var[n] + " = bool(binCount & " + str(bin(binCountBasis)) + ")\n")
            binCountBasis <<= 1
        if output:
            for n in range(len(self.var)):
                code += ("        print(int(" + self.var[n] + "), end = " + chr(34) + chr(32) + chr(32) + chr(34) + ")\n")
        code += "        a = int(" + self.output + ")\n"
        code += "        ret.append(a)\n"
        if output:
            code += ("        print(a)\n")
        code += ("        binCount += 1\n")
        code += ("    return ret\n")
        
        exec(code)
        exec("self.functionVal = function()")
        
        
    def __eq__(self, obj): 
        if isinstance(obj, boolAlg):
            return self.functionVal == obj.functionVal
        else:
            print("Invalid comparison: <class 'boolAlg'> and " + str(type(obj)))
            return None
        
    def __ne__(self, obj):
        if isinstance(obj, boolAlg):
            return self.functionVal != obj.functionVal
        else:
            print("Invalid comparison: <class 'boolAlg'> and " + str(type(obj)))
            return None
