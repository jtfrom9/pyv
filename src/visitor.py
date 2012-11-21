# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
import collections
import ast

class Visitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit(self, node, arg):
        pass

class Arg(collections.Mapping):
    def __init__(self, parent, level=None):
        assert(isinstance(parent, ast.AstNode) or parent is None)
        self._dict = {}
        self._add('parent',parent)
        self._add('level',level)

    def __len__(self):
        return len(self._dict)

    def __getitem__(self,key):
        return self._dict[key]

    def __iter__(self):
        for k in self._dict.keys():
            yield k

    def _add(self, key, value):
        if key in self._dict:
            raise Exception("already has key '{0}' in self._dict".format(key))
        self._dict[ key ] = value
        #setattr(self, key, value)
        setattr(self.__class__, key, property(lambda self: self.__getitem__(key)))

    def createChild(self, parent, **kws):
        arg = Arg(parent, self.level + 1)
        for key, value in kws.items():
            arg._add(key,value)
        return arg

def suppress_traverse(fn):
    def _handler(*argv):
        fn(*argv)
        return (x for x in [])
    return _handler

def dispatch_handler( cls_list, visitor, node, default_handler, handler_prefix="handler" ):
    for cls in cls_list:
        if isinstance(node,cls):
            return getattr(visitor, handler_prefix + cls.__name__)
    else:
        return default_handler
        
class TraverseTraceVisitor(Visitor):
    def visit(self,node,arg):
        print("{spc}{node}(arg={arg})".format(
                spc  = " "*arg.level*2 ,
                node = repr(node),
                arg  = arg.items()))

class StatementPrettyPrinterVisitor(Visitor):
    def __init__(self, out_stream, indent=2):
        self._out_stream = out_stream
        self._indent     = indent

    def visit(self,node,arg):
        return dispatch_handler([ ast.ConditionalStatement,
                                  ast.Block,
                                  ast.ConstructStatementItem,
                                  ast.ContinuousAssignmentItems,
                                  ast.NodeList 
                                  ],
                                self, 
                                node,
                                self.handlerAny
                                )(node,arg)

    def _write(self, level, string):
        for s in string.split("\n"):
            self._out_stream.write(" " * (self._indent * level) + s + "\n")

    def handlerAny(self,node,arg):
        self._write(arg.level, str(node))

    @suppress_traverse
    def handlerConditionalStatement(self,node,arg):
        first = True
        for cond, stmt in node.eachCondAndStatements():
            if cond:
                self._write(arg.level,
                            "{key} {cond} then:".format(key  = "if" if first else "else if",
                                                        cond = str(cond)))
                first = False
            else:
                self._write(arg.level, "else:")
            self.visit(stmt,arg.createChild(node))

    @suppress_traverse
    def handlerBlock(self,block,arg):
        self._write(arg.level, "{key}".format(key="begin" if block.isSequencial else "fork"))
        newarg = arg.createChild(block)
        for s in block.eachStatements():
            self.visit(s,newarg)
        self._write(arg.level, "{key}".format(key="end" if block.isSequencial else "join"))

    @suppress_traverse
    def handlerConstructStatementItem(self,node,arg):
        self._write(arg.level,node.type)
        self.visit(node.statement,arg.createChild(node))

    @suppress_traverse
    def handlerContinuousAssignmentItems(self,node,arg):
        self._write(arg.level,node.type)
        for s in node.eachStatements():
            self.visit(s,arg.createChild(node))

    @suppress_traverse
    def handlerNodeList(self,nlist,arg):
        for n in nlist: 
            self.visit(n,arg)


