# 
#   Boolean Algebra System
#       - Helper Functions and Classes
#
#   Scripted by Felix Jancso-Szabo (2016)
#


# Tree data structure used to express the boolean algebra expressions for simplification
class Tree (object):
    def __init__(self, children):
        if len(children) != 0:
            self.children = children
        else:
            self.children = []
    
    #function that adds a child to the node
    def addChild(self, child):
        if isinstance(child, (list, tuple)):
            self.children += list(child)
        else:
            self.children.append(child)
    
    #allows the tree to be printed recursively
    def __repr__(self, level=0):
        ret = ""
        for child in self.children:
            if not isinstance(child, Tree):
                ret += "\t" * level + "'" + str(child) + "'\n"
            else:
                ret += child.__repr__(level+1)
        return ret

#function that checks whether there is proper bracket nesting (and whether all brackets are closed)
def checkBracketParity(string):
    stack = []
    for n in range(len(string)):
        if string[n] == "(":
            if n + 1 < len(string) and string[n+1] == ")":
                return False
            else:
                stack.append("(")
        if string[n] == ")":
            if len(stack) == 0 or stack[len(stack) - 1] != "(":
                return False
            elif stack[len(stack) - 1] == "(":
                stack.pop()
                
    if len(stack) == 0:
        return True  
    return False
    

# Analyzes whether a number is a power of two without using log functions (no floats)        
def powerOfTwo(num):
    return num != 0 and ((num & (num - 1)) == 0)

