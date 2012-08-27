# -*- coding: utf-8 -*-
import sys
import unittest
from pyparsing import stringEnd, ParseException, ParseSyntaxException

import ast

class GrammarTestCase(unittest.TestCase):
    def grammar(self):
        pass

    def _check(self, text, success, expect):
        result = None
        try:
            result = (self.grammar() + stringEnd).parseString(text)
        except (ParseException, ParseSyntaxException) as e:
            if success:
                print(dir(e))
                print(type(e))
                print("input = \"{0}\", expect = {1}, msg = {2}".format(text, expect, e))
                print("line={0}, lineno={1}, loc={2}".format(e.line, e.lineno, e.loc))
                print("parserElement={0}".format(e.parserElement))
                print("pstr={0}".format(e.pstr))
                self.fail("input = \"{0}\", expect = {1}, msg = {2}".format(text, expect, e))
                sys.exit()
            else:
                self.assertTrue(True)
            return
        except Exception as e:
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
        print("\ncheck_pass: \"{0}\"".format(text))
        return self._check(text, True, expect)

    def check_fail(self, text):
        print("\ncheck_fail: \"{0}\"".format(text))
        return self._check(text, False, None)


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
        
def TestCase2(grammar):
    def _decolator(test_func):
        class _TestCase(GrammarTestCase):
            def setUp(self):
                print("\n{0}: Test({1}) Start:".format(grammar.resultsName, test_func.__name__))
            def tearDown(self):
                print("\n{0}: Test({1}) End".format(grammar.resultsName,test_func.__name__))
            def grammar(self):
                return grammar
            def runTest(self):
                test_func(self)
        _TestCase.__name__   = test_func.__name__
        _TestCase.__module__ = test_func.__module__
        return _TestCase
    return _decolator

def _print(result):
    print(result.asXML())
    print(ast.nodeInfo(result))

def _id_print(result):
    print(result.asXML())
    idAst = result[0]
    print("shortName={0}".format(idAst.shortName()))
    print("longName={0}".format(idAst.longName()))
    if idAst.hasIndex(): print("Index={0}".format(idAst.index))
    if idAst.hasRange(): print("Range={0}".format(idAst.range))
    if idAst.isHierachical():
        for index,id in enumerate(idAst.ids):
            print("  name[{0}] short={1}, long={2}".format(index,id.shortName(),id.longName()))




