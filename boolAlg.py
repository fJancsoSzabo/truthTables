#
#   Boolean Algebra System
#       - Main Code
#

from math import log
from helper import *

class boolAlg (object):
    def __init__(self, userInput):
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

                    self.exp = first_half + " not " + second_half

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

        # Replace any groups of spaces with one space
        self.exp = ' '.join(self.exp.split())

        self.var = sorted(set(self.var))

    # Generates code for the creation of the truth table
    def calc(self):

        code = "def function():\n"
        code += ("    ret = []\n")

        for variable in self.var:
            code +=("    " + variable + " = 0\n")

        code += "    binCount = 0\n"
        code += "    for item in range(" + str(2**len(self.var)) + "):\n"

        binCountBasis = 0b1

        # TODO: Change this to use enumerate
        # TODO: Explain the weird ordering here
        for n in reversed(range(len(self.var))):
            code += ("        " + self.var[n] + " = bool(binCount & " + str(binCountBasis) + ")\n")
            binCountBasis <<= 1

        code += "        a = int(" + self.exp + ")\n"
        code += "        ret.append(a)\n"

        code += ("        binCount += 1\n")
        code += ("    return ret\n")

        exec(code)

        self.functionVal = function()

        # ^ Formerly: exec("self.functionVal = function()")

    # prints the boolean expression used for the calculations
    def __repr__(self):
        return self.exp


    # prints the truth table for the object
    def printTable(self):
        result = ""
        for item in self.var:
            result += item + "  "

        result += "Function Result\n"

        permutations = 2**len(self.var)

        binCount = 0
        for n in range(permutations):
            innerCount = permutations >> 1

            for i in reversed(range(len(self.var))):
                result += str(int(bool(binCount & innerCount))) + "  "
                innerCount >>= 1

            result += str(self.functionVal[binCount]) + "\n"
            binCount += 1
        print(result)

    # Returns whether two different boolean functions are equivalent
    def __eq__(self, obj):
        if not isinstance(obj, boolAlg):
            return NotImplemented

        return self.functionVal == obj.functionVal

    # A function that returns whether two different boolean functions are not equivalent
    def __ne__(self, obj):
        if not isinstance(obj, boolAlg):
            return NotImplemented

        return self.functionVal != obj.functionVal

    # This function derives a minterm expression for a function from its truth table
    @staticmethod
    def calculateExp(self, values, literals):
        # If the length of the input isn't a power of two, unsure how to handle this?
        if not powerOfTwo(len(values)):
            raise NotImplementedError

        # Calculate the number of values we're expecting, based on the number of literals provided
        maxVal = pow(2, len(literals))

        # if the number of values provided differs from the expectation, it's an error
        if len(values) != maxVal:
            raise Exception

        literals.sort(reverse=True)

        minterm_list = []

        for count in range(maxVal):
            # If this result in the truth table is false, we don't need to add a min term.  Skip to the next result
            if values[count] != 1:
                continue

            minterm = ""
            for key, literal in enumerate(literals):

                minterm += literal

                # If the current bit is 0 for the current literal (e.g. 0b110 and the literals are A, B and C), then invert that literal in this term (add a "'" to "ABC")
                if (1 << key) & count == 0:
                    minterm += "'"

            minterm_list.append(minterm)

        return "+".join(minterm_list)

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
            return boolAlg(string)
        else:
            return string
