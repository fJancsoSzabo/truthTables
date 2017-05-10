#
#   Boolean Algebra System
#       - Main Code
#
#   Scripted by Felix Jancso-Szabo (2016)
#

from math import log
from helper import *

class boolAlg (object):
    def __init__(self, userInput, output):
        # stores the expression given by the user
        self.input = userInput
        self.inputLen = len(userInput)

        # initializes variables
        self.exp = ""
        self.var = []
        self.functionVal = []
        self.tree = Tree([])

        # If all brackets make up a matching pair
        if checkBracketParity(self.input):

            self.parse()
            self.calc()
            self.buildTree()
            if output:
                print(self.__repr__())
                self.printTable()
        else:
            print("Error: there are mismatched brackets in your expression")

    # Transforms the input boolean string into a structure this code can use
    def parse(self):

        bracketNest = 0

        bracketOpenPos = []

        # TODO: Change this to use enumerate
        for n in range(self.inputLen):
            if self.input[n] == "+":
                self.exp += " or "

            elif self.input[n] == "(":
                # Store where the bracket will be added in self.exp.  This is so that, if a "'" is found, we can add a not BEFORE the bracket
                bracketOpenPos.append(len(self.exp))
                bracketNest += 1
                self.exp += "("

            else:
                if self.input[n] == "'":
                    split_index = 0

                    # If this character is negating more than one character, then we have to find the corresponding opening bracket and insert the "not"
                    if self.input[n-1] == ")":
                        # Calculate the the index of the opening bracket
                        split_index = bracketOpenPos[len(bracketOpenPos)-bracketNest]

                        # Cut the current expression into two halves, the first one ending just before the opening bracket, the second one starting with the bracket
                        bracketNest -= 1

                    else:
                        split_index = len(self.exp)-1

                    first_half = self.exp[:split_index]
                    second_half = self.exp[split_index:]


                elif self.input[n] == ")":
                    # Not sure why this is here
                    if n != self.inputLen - 1 and self.input[n+1] != "'":
                        bracketNest -= 1

                    self.exp += ")"

                else:
                    # This character is a variable name or a space, add it.
                    self.var += self.input[n]
                    self.exp += self.input[n]

                # If this is not the last character in the input, and adding an "and" wouldn't create invalid syntax, add an "and".
                if n != self.inputLen - 1 and self.input[n+1] not in ["+", ")", "'"]:
                    self.exp += " and "

        self.var = sorted(set(self.var))

    # Generates code for the creation of the truth table
    def calc(self):
        # if output:
            # for item in self.var:
                # print(item, end = "  ")

            # print("Function Result")

        code = "def function():\n"
        code += ("    ret = []\n")
        for item in self.var:
            code +=("    " + item + " = 0\n")
        code += "    binCount = 0\n    for item in range(" + str(2**len(self.var)) + "):\n"
        binCountBasis = 0b1
        for n in reversed(range(len(self.var))):
            code += ("        " + self.var[n] + " = bool(binCount & " + str(bin(binCountBasis)) + ")\n")
            binCountBasis <<= 1
        # if output:
            # for n in range(len(self.var)):
                # code += ("        print(int(" + self.var[n] + "), end = " + chr(34) + chr(32) + chr(32) + chr(34) + ")\n")
        code += "        a = int(" + self.exp + ")\n"
        #code += "        print(a)\n"
        code += "        ret.append(a)\n"
        # if output:
            # code += ("        print(a)\n")
        code += ("        binCount += 1\n")
        code += ("    return ret\n")
        exec(code)
        exec("self.functionVal = function()")

# prints the boolean expression used for the calculations
    def __repr__(self):
        return self.exp


# prints the truth table for the object
    def printTable(self):
        ret = ""
        for item in self.var:
            ret += item + "  "

        ret += "Function Result\n"

        binCount = 0
        for n in range(2**len(self.var)):
            innerCount = 2**(len(self.var) - 1)
            for i in reversed(range(len(self.var))):
                ret += str(int(bool(binCount & innerCount))) + "  "
                innerCount >>= 1
            ret += str(self.functionVal[binCount]) + "\n"
            binCount += 1
        print(ret)

# Returns whether two different boolean functions are equivalent
    def __eq__(self, obj):
        if isinstance(obj, boolAlg):
            return self.functionVal == obj.functionVal
        else:
            print("Invalid comparison: <class 'boolAlg'> and " + str(type(obj)))
            return None

# A function that returns whether two different boolean functions are not equivalent
    def __ne__(self, obj):
        if isinstance(obj, boolAlg):
            return self.functionVal != obj.functionVal
        else:
            print("Invalid comparison: <class 'boolAlg'> and " + str(type(obj)))
            return None

# This function derives a minterm expression for a function from its truth table
    def calculateExp(self):
        print("Please input values of the truth table one at a time.  Enter any other character to end the input")
        inp = "1"
        tempVal = []
        while inp == "1" or inp == "0":
            inp = input()
            if inp == "1" or inp == "0":
                tempVal.append(int(inp))
        if not powerOfTwo(len(tempVal)):
            print("Invalid length of truth table.")
            return None
        tempVar = []
        output = []
        varCount = int(log(len(tempVal), 2))
        maxVal = pow(2, varCount)
        print("Please input, one at a time, the literals you want your expression in.")
        for n in range(varCount):
            tempVar.append(input())
        tempVar = sorted(tempVar)[::-1]
        binCount = 0
        while binCount < maxVal:
            if tempVal[binCount] == 1:
                innerCount = 1
                counter = 1
                while counter <= varCount:
                    if innerCount == 1:
                        output.append(tempVar[counter - 1])
                    else:
                        output[len(output) - 1] += tempVar[counter - 1]
                    if not bool(innerCount & binCount):
                        output[len(output) - 1] += "'"
                    counter += 1
                    innerCount <<= 1
            binCount += 1
        ret = boolAlg("+".join(output), False)
        return ret

# Function that builds the tree by calling the recursive function.  Nests things based on brackets
    def buildTree(self):
        n = 0
        while n < len(self.exp):
            if self.exp[n] != "(" and self.exp[n] != ")" and self.exp[n] != " ":
                if self.exp[n] == "o":
                    self.tree.addChild(self.exp[n:n+2])
                    n += 1
                elif self.exp[n] == "a":
                    self.tree.addChild(self.exp[n:n+3])
                    n += 2
                elif self.exp[n] == "n":
                    self.tree.addChild(self.exp[n:n+3])
                    n += 2
                else:
                    self.tree.addChild(self.exp[n])
            elif self.exp[n] == "(":
                self.tree.addChild(Tree([]))
                n = self.buildTreeRecurse(self.tree.children[len(self.tree.children)-1], n + 1)
            n += 1

# The recursive function that is called by the function designed to be general purpose (buildTree).
# Separate from the main function because their loops have different termination points
    def buildTreeRecurse(self, node, n):
        while self.exp[n] != ")":
            if self.exp[n] == "(":
                node.addChild(Tree([]))
                n = self.buildTreeRecurse(node.children[len(node.children)-1], n + 1)
            elif self.exp[n] != " ":
                if self.exp[n] == "o":
                    node.addChild(self.exp[n:n+2])
                    n += 1
                elif self.exp[n] == "a":
                    node.addChild(self.exp[n:n+3])
                    n += 2
                elif self.exp[n] == "n":
                    node.addChild(self.exp[n:n+3])
                    n += 2
                else:
                    node.addChild(self.exp[n])
            n += 1
        n -= 1
        return n

# Builds an expression based on the tree structure.  Allows for an expression to be converted to a tree, simplified, and then returned to an expression format
    def buildExp(self, node = None, root = True):
        if root:
            node = self.tree
        string = ""
        for child in node.children:
            if isinstance(child, Tree):
                string += "(" + self.analyzeTree(child, False) + ") "
            else:
                string += child + " "
        if root:
            return boolAlg(string, False)
        else:
            return string
