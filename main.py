from boolAlg import *

userIn = input("Please input a boolean algebra expression\n")
printItAsk = input("\nDo you want a truth table printed? (Y/N)\n")
printIt = True
if printItAsk.upper() != "Y":
    printIt = False

expr = boolAlg(userIn, printIt)
