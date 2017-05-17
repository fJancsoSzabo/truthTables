from helper import *
import unittest

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


if __name__ == '__main__':
    unittest.main()