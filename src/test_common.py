import parser as p
import pyparsing as pp
import unittest

class TestGrammer(unittest.TestCase):
    def getGrammer(self):
        pass

    def _test(self, text):
        try:
            result = (self.getGrammer() + pp.stringEnd).parseString(text)
        except (pp.ParseException, pp.ParseSyntaxException) as e:
            print("** line={0},msg={1}".format(e.line, e.msg))
            return None
        return result

    def _testp(self,text):
        result = self._test(text)
        if result: 
            print("******")
            for p in dir(result):
                print(p)
            print("result={0}".format(result.asXML()))
        return result

class Test_binary_number(TestGrammer):
    def getGrammer(self):
        return p.binary_number

    def test1(self):
        self.assertTrue(self._testp("4'b0000"))
        self.assertTrue(self._test("4'SB0?00"))
        self.assertTrue(self._test("8'Sbzzzz_xxxx"))
        self.assertTrue(self._test("'b0000"))
        self.assertFalse(self._test("'b00 00 "))
        self.assertTrue(self._test("'b 0000 "))
        self.assertTrue(self._test(" 32 'b 0000 "))
        self.assertFalse(self._test(" 3 2 'b 0000 "))


suite = unittest.TestLoader().loadTestsFromTestCase(Test_binary_number)
unittest.TextTestRunner(verbosity=2).run(suite)

