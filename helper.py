# 
#   Boolean Algebra System
#       - Helper Functions and Classes
#
#   Scripted by Felix Jancso-Szabo (2016)
#


# Tree data structure used to express the boolean algebra expressions for simplification
class Tree (object):
    def __init__(self, children):
        self.children = children

    # Function that adds a child to the node
    def addChild(self, child):
        if isinstance(child, (list, tuple)):
            self.children += list(child)
        else:
            self.children.append(child)
    
    # Allows the tree to be printed
    def __repr__(self, level=0):
        ret = ""
        for child in self.children:
            if not isinstance(child, Tree):
                ret += "\t" * level + "'" + str(child) + "'\n"
            else:
                ret += child.__repr__(level+1)
        return ret

# Function that checks whether there is proper bracket nesting (and whether all brackets are closed)
def checkBracketParity(string):
    nesting_count = 0
    for index, char in enumerate(string):
        if char == "(":
            nesting_count += 1
        elif char == ")":
            nesting_count -= 1

        if nesting_count < 0
            return false

    return nesting_count == 0
    

# Analyzes whether a number is a power of two without using log functions (no floats)        
def powerOfTwo(num):
    return num != 0 and ((num & (num - 1)) == 0)

