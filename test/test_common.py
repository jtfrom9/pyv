# -*- coding: utf-8 -*-
import sys, os
import unittest
from pyparsing import stringEnd, ParseBaseException, ParseException, ParseSyntaxException, ParseFatalException, ParseResults

sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir))
from src import grammar, ast, visitor

class GrammarTestCase(unittest.TestCase):
    import abc
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def grammar(self):
        pass

    def do_parse(self, text):
        return (self.grammar() + stringEnd).parseString(text)

    def check_pass(self, text, expect=None, msg=None):
        print("\ncheck_pass: \"{0}\"".format(text))
        try:
            result = self.do_parse(text)
        except Exception as e:
            print("{0}: {1}".format(e.__class__.__name__, str(e)))
            raise e
            
        print("parse OK.")
        if expect:
            errmsg = "input = \"{0}\", expect = {1}, result = {2}".format(text, expect, result)
            if msg: 
                errmsg += "\n   " + msg
            self.assertEqual(result, expect, errmsg)
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
    if idAst.hasIndex(): print("Index={0}".format(idAst.getIndex()))
    if idAst.hasRange(): print("Range={0}".format(idAst.getRange()))
    if idAst.isHierachical():
        for index,id in enumerate(idAst.each_id()):
            print("  name[{0}] str={1}, repr={2}".format(index,str(id),repr(id)))

def ___stmt_print(obj, level=0, indent=3, out=sys.stdout, debug=False):
    if debug:
        print("_stmt_print: level={0}, obj={1} ({2})".format(level, ast.nodeInfo(obj), type(obj)))
    if isinstance(obj, ParseResults):
        out.write("{spc}{data}:\n".format(spc=" "*indent*level,
                                          data = obj.keys()[0]))
        #out.write(obj.resultsName +':\n')
        for x in obj:
            _stmt_print(x, level+1, indent, debug = debug)
    elif isinstance(obj, ast.IterableAstNode):
        #_stmt_pprint(obj.asList(), level, indent, out)
        import pprint
        out.write("{spc}{data}\n".format(spc=" "*indent*level,
                                       data=pprint.pformat(obj.asList(),indent=indent, width=10)))
    elif obj is not None:
        out.write(str(obj)+'\n')
    else:
        pass # if None


def _stmt_print(result, out=sys.stdout, debug=False):
    if not result:
        return

    if debug:
        print("_stmt_print: level={0}, obj={1} ({2})".format(level, ast.nodeInfo(obj), type(obj)))

    out.write("{0}:\n".format(result.keys()[0]))
    node = result[0]
    node.traverse(visitor.StatementPrettyPrinterVisitor(out),visitor.Arg(None,init_level=1))


# def _defaultStartDebugAction( instring, loc, expr ):
#     print ("Match " + _ustr(expr) + " at loc " + _ustr(loc) + "(%d,%d)" % ( lineno(loc,instring), col(loc,instring) ))
# def _defaultSuccessDebugAction( instring, startloc, endloc, expr, toks ):
#     print ("Matched " + _ustr(expr) + " -> " + str(toks.asList()))
# def _defaultExceptionDebugAction( instring, loc, expr, exc ):
#     print ("Exception raised:" + _ustr(exc))


def debug(expr, on=True):
    expr.setName(expr.resultsName)
    expr.setDebug(on)
    # def start(*argv):
    #     print("start {0}".format(argv))
    # def success(*argv):
    #     print("success {0}".format(argv))
    # def excep(*argv):
    #     print("excep {0}".format(argv))
    # expr.setDebugActions(start,success,excep)

def fail(expr, action):
    expr.setName(expr.resultsName)
    expr.setFailAction(action)
    
