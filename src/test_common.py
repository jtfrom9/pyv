# -*- coding: utf-8 -*-
import sys
import unittest
from pyparsing import stringEnd, ParseBaseException, ParseException, ParseSyntaxException, ParseFatalException, ParseResults

import ast

class GrammarTestCase(unittest.TestCase):
    import abc
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def grammar(self):
        pass

    def do_parse(self, text):
        return (self.grammar() + stringEnd).parseString(text)

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

def testOf(grammar):
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

# def _stmt_pprint(obj, level=0, indent=1, out=sys.stdout):
#     if len(obj)==0: return
#     if isinstance(obj,list):
#         start, end = ('[', ']')
#     out.write("{spc}{start}{top}\n".format(
#             spc = " " * level * indent,
#             start = start,
#             top = obj[0]))
#     for x in obj[1:]:
#         _stmt_pprint(x, level+1, indent, out)
#     out.write("{spc}{end}\n".format(
#             spc = " " * level * indent,
#             end = end))

def _stmt_print(obj, level=0, indent=3, out=sys.stdout):
    if isinstance(obj, ParseResults):
        out.write("{spc}{data}:\n".format(spc=" "*indent*level,
                                          data = obj.keys()[0]))
        #out.write(obj.resultsName +':\n')
        for x in obj:
            _stmt_print(x, level+1, indent)
    elif isinstance(obj, ast.IterableAstNode):
        #_stmt_pprint(obj.asList(), level, indent, out)
        import pprint
        out.write("{spc}{data}".format(spc=" "*indent*level,
                                       data=pprint.pformat(obj.asList(),indent=indent, width=10)))
    elif obj is not None:
        out.write(str(obj)+'\n')
    else:
        pass # if None

def debug(expr, on=True):
    expr.setName(expr.resultsName)
    expr.setDebug(on)

def fail(expr, action):
    expr.setName(expr.resultsName)
    expr.setFailAction(action)
    
