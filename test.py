from boolAlg import *

# test = Tree([
    # "not",
    # "(",
    # Tree([
        # "A",
        # "+",
        # "B"]),
    # ")"])
# test.addChild([test2,2])
# print(test)


#print(checkBracketParity("(())"))
#print(checkBracketParity("(((("))
#rint(checkBracketParity("(()()ooooo)"))
#rint(checkBracketParity("(A)(AB)((AB))"))

test = boolAlg("(A+B)'+CD", False)

print("actual", test)

test.analyzeTree()

print((True or False ))
