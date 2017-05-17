from helper import *
import unittest
from boolAlg import *

class TestBracketNestMethods(unittest.TestCase):

    def test_basic_fail(self):
        self.assertFalse(checkBracketParity(")("))
        self.assertFalse(checkBracketParity("("))
        self.assertFalse(checkBracketParity(")"))

    def test_missing_close(self):
        self.assertFalse(checkBracketParity("(()(())()"))

    def test_basic_success(self):
        self.assertTrue(checkBracketParity("()"))

    def test_complex_success(self):
        self.assertTrue(checkBracketParity("(()(())())"))

    def test_extra_characters_success(self):
        self.assertTrue(checkBracketParity("stringpart1(stringpart2)&stringpart3"))

    def test_extra_characters_fail(self):
        self.assertFalse(checkBracketParity("stringpart1(stringpart2&stringpart3"))

class TestBoolAlgParser(unittest.TestCase):
    def test_1(self):
        testing = boolAlg("(A+D)(BD)'+(AC+D')'")
        self.assertEquals("(A or D) and not (B and D) or not (A and C or not D)", testing.exp)
        # "(A+D)(BD)'+(AC+D')'"

    def test_2(self):
        testing = boolAlg("A+(B(C+(D(E+(F)')')')')'")
        self.assertEquals("A or not (B and not (C or not (D and not (E or not (F)))))", testing.exp)

    def test_3(self):
        testing = boolAlg("A+(B(C+(D(E+(F)))))")
        self.assertEquals("A or (B and (C or (D and (E or (F)))))", testing.exp)

    def test_4(self):
        testing = boolAlg("(((((A)+B)C)+D)E)+FG")
        self.assertEquals("(((((A) or B) and C) or D) and E) or F and G", testing.exp)

    def test_5(self):
        testing = boolAlg("(((((A)'+B)'C)'+D)'E)'+F'G'")
        self.assertEquals(" not ( not ( not ( not ( not (A) or B) and C) or D) and E) or not F and not G", testing.exp)

if __name__ == '__main__':
    unittest.main()