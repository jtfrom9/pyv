# -*- coding: utf-8 -*-
import sys
import unittest
from pyparsing import stringEnd, ParseBaseException, ParseException, ParseSyntaxException, ParseFatalException, ParseResults

import ast

class GrammarException(ParseBaseException):
    def __init__(self, *args):
        super(ParseBaseException,self).__init__(self,*args)


class GrammarTestCase(unittest.TestCase):
    def grammar(self):
        pass

    def do_parse(self, text):
        result = None
        try:
            result = (self.grammar() + stringEnd).parseString(text)
        #except (ParseException, ParseSyntaxException, ParseFatalException) as e:
        except ParseBaseException as e:
            #e.msg = "input = \"{0}\": Expected: ".format(text) + e.msg
            #raise e
            #raise e.__call__("input = \"{0}\": ".format(text) + e.msg)
            #raise e.__new__(e.__class__, msg = "input = \"{0}\": ".format(text) + e.msg)
            # for prop in dir(e):
            #     print("{0} = {1}".format(prop, getattr(e,prop,None)))
            # #e.msg = "input = \"{0}\" {1}".format(text, e.msg) 
            #e.msg = "Expected: "
            #e.msg = "Syntax Error"
            raise e
            #raise GrammarException(e.pstr, e.loc, "input = \"{0}\": ".format(text) + e.msg)

        except Exception as e:
            # print(dir(e))
            # msgattr = getattr(e, "msg", None)
            # if msgattr:
            #     e.msg = "Caught unknown exception! " + e.msg
            # else:
            #     print(e)
            #e.args = "Caught unknown exception! " + e.args
            #print(e.args)
            raise e
        return result

        if expect:
            self.assertEqual(result, expect, "input = \"{0}\", expect = {1}".format(text,expect))
        else:
            self.assertTrue(True)
        return result

    def check_pass(self, text, expect=None):
        print("\ncheck_pass: \"{0}\"".format(text))
        try:
            result = self.do_parse(text)
        except Exception as e:
            print("{0}: {1}".format(e.__class__.__name__, str(e)))
            raise e
            
        print("parse OK.")
        if expect:
            self.assertEqual(result, expect, 
                             "input = \"{0}\", expect = {1}, result = {2}".format(text, expect, result))
        else:
            self.assertTrue(result)
        return result

    def check_fail(self, text):
        print("\ncheck_fail: \"{0}\"".format(text))
        #self.assertRaises(Exception, lambda : self.do_parse(text))
        try:
            self.do_parse(text)
        except ParseBaseException as e:
            print("{0}: {1}".format(e.__class__.__name__, str(e)))
            print("fail expected. OK.")
        else:
            self.fail("\"{0}\" expected fail...")
        return None

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

def run_tests(tests=[]):
    import sys
    if len(sys.argv)>1:
        for arg in sys.argv[1:]: tests.append(arg)
    if len(tests)==0:
        unittest.main()
    else:
        import inspect
        modname = inspect.currentframe(1).f_globals["__name__"]
        suite = unittest.defaultTestLoader.loadTestsFromNames([modname + "." + test for test in tests])
        unittest.TextTestRunner().run(suite)

def _print(result):
    if isinstance(result,ParseResults):
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




