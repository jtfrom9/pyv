# -*- coding: utf-8 -*-
import unittest
from pyparsing import stringEnd, ParseException, ParseSyntaxException

class GrammarTestCase(unittest.TestCase):
    def grammar(self):
        pass

    def _check(self, text, success, expect):
        result = None
        try:
            result = (self.grammar() + stringEnd).parseString(text)
        except (ParseException, ParseSyntaxException) as e:
            if success:
                self.fail("input = \"{0}\", expect = {1}, msg = {2}".format(text, expect, e.msg))
            else:
                self.assertTrue(True)
            return
        except Exception, e:
            if success:
                self.fail("input = \"{0}\", expect = {1}, msg = {2}".format(text, expect, e))
            else:
                self.assertTrue(True)
            return

        self.assertTrue(success,"input = \"{0}\", expect = {1}, result = {2}".format(text, expect, result))
        if expect:
            self.assertEqual(result, expect, "input = \"{0}\", expect = {1}".format(text,expect))
        else:
            self.assertTrue(True)
        return result

    def check_pass(self, text, expect=None):
        return self._check(text, True, expect)

    def check_fail(self, text):
        return self._check(text, False, None)

# def TestCase(grammar):
#     def _decolator(test_func):
#         class _TestCase(GrammarTestCase):
#             def grammar(self):
#                 return grammar
#             def runTest(self):
#                 test_func(self)
#         return _TestCase
#     return _decolator
        
def TestCase(grammarSet):
    prefix = "test_"

    def _decolator(test_func):
        func_name = test_func.__name__
        grammar_name_index = func_name.index(prefix)
        grammar_name = func_name[len(prefix):]
        g = getattr(grammarSet, grammar_name)
        class _TestCase(GrammarTestCase):
            def grammar(self):
                return g
            def runTest(self):
                test_func(self)
        _TestCase.__name__   = test_func.__name__
        _TestCase.__module__ = test_func.__module__
        return _TestCase
    return _decolator
        


