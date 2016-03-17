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


print(checkBracketParity("(())"))
print(checkBracketParity("(((("))
print(checkBracketParity("(()()ooooo)"))
print(checkBracketParity("(A)(AB)((AB))"))
