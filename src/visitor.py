# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta
import ast

class Visitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self, node, arg):
        pass

class GenericVisitorMixin(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispatch(self, node):
        """ must return handler function for node """
        pass

    @abstractmethod
    def default_handler(self, node, arg):
        """ called if no handler dispatched (when dispatch returned None) """
        pass

    def __call__(self, node, arg):
        func = self.dispatch(node)
        if func:
            return func(node, arg)
        else:
            return self.default_handler(node, arg)

class Arg(object):
    def __init__(self, parent, arg=None, init_level=None):
        self._dict = {}
        self.add_prop('parent',parent)
        if init_level:
            self.add_prop('level',init_level)
        else:
            self.add_prop('level',arg.level + 1 if arg else 0)

    def __contains__(self, key):
        return key in self._dict

    def add_prop(self, key, value):
        if key in self._dict:
            raise Exception("already has key '{0}' in self._dict".format(key))
        self._dict[ key ] = value
        setattr(self, key, value)

    def __call__(self, **kws):
        for key, value in kws.items():
            self.add_prop(key,value)
        return self

    def clone(self):
        arg = Arg(self.parent, self)
        for key in (key for key in self._dict.keys() if key not in ('parent','level')):
            arg.add_prop(key,value)
        return arg

root_arg = Arg(None)


def suppress_traverse(fn):
    def _handler(*argv):
        fn(*argv)
        return (x for x in [])
    return _handler


class StatementPrettyPrinterVisitor(Visitor):
    def __init__(self, out_stream, indent=2):
        self._out_stream = out_stream
        self._indent     = indent

    def __call__(self,node,arg):
        if isinstance(node, ast.ConditionalStatement):
            return self.handlerConditionalStatement(node,arg)
        if isinstance(node, ast.Block):
            return self.handlerBlock(node,arg)
        elif isinstance(node, ast.ConstructStatementItem):
            return self.handlerConstructStatementItem(node,arg)
        elif isinstance(node, ast.ContinuousAssignmentItems):
            return self.handlerContinuousAssignmentItems(node,arg)
        elif isinstance(node, ast.NodeList):
            return self.handlerNodeList(node,arg)
        #elif isinstance(node, ast.Statement):
        else:
            return self.handlerAny(node,arg)

    def _write(self, string, level=0):
        for s in string.split("\n"):
            self._out_stream.write(" " * (self._indent * level) + s + "\n")

    def handlerAny(self,node,arg):
        self._write(str(node), arg.level)

    @suppress_traverse
    def handlerConditionalStatement(self,node,arg):
        first = True
        for cond, stmt in node.eachCondAndStatements():
            if cond:
                self._write("{key} {cond} then:".format(
                        key  = "if" if first else "else if",
                        cond = str(cond)), arg.level)
                first = False
            else:
                self._write("else:", arg.level)

            self(stmt,Arg(node,arg))

    @suppress_traverse
    def handlerBlock(self,block,arg):
        self._write("{key}".format(key="begin" if block.isSequencial else "fork"), arg.level)
        newarg = Arg(block,arg)
        for s in block.eachStatements():
            self(s,newarg)
        self._write("{key}".format(key="end" if block.isSequencial else "join"), arg.level)

    @suppress_traverse
    def handlerConstructStatementItem(self,node,arg):
        self._write(node.type, arg.level)
        self(node.statement,Arg(node,arg))

    @suppress_traverse
    def handlerContinuousAssignmentItems(self,node,arg):
        self._write(node.type, arg.level)
        for s in node.eachStatements():
            self(s,Arg(node,arg))

    @suppress_traverse
    def handlerNodeList(self,nlist,arg):
        for n in nlist: self(n,arg)


# # visit.py

# import inspect

# __all__ = ['on', 'when']

# def on(param_name):
#   def f(fn):
#     dispatcher = Dispatcher(param_name, fn)
#     return dispatcher
#   return f


# def when(param_type):
#   def f(fn):
#     frame = inspect.currentframe().f_back
#     dispatcher = frame.f_locals[fn.func_name]
#     if not isinstance(dispatcher, Dispatcher):
#       dispatcher = dispatcher.dispatcher
#     dispatcher.add_target(param_type, fn)
#     def ff(*args, **kw):
#       return dispatcher(*args, **kw)
#     ff.dispatcher = dispatcher
#     return ff
#   return f


# class Dispatcher(object):
#   def __init__(self, param_name, fn):
#     frame = inspect.currentframe().f_back.f_back
#     top_level = frame.f_locals == frame.f_globals
#     self.param_index = inspect.getargspec(fn).args.index(param_name)
#     self.param_name = param_name
#     self.targets = {}

#   def __call__(self, *args, **kw):
#     typ = type(args[self.param_index])
#     d = self.targets.get(typ)
#     if d is not None:
#       return d(*args, **kw)
#     else:
#       issub = issubclass
#       t = self.targets
#       ks = t.iterkeys()
#       return [t[k](*args, **kw) for k in ks if issub(typ, k)]

#   def add_target(self, typ, target):
#     self.targets[typ] = target

# class AbstractSyntaxTreeVisitor(object):
#     @visit.on('node')
#     def visit(self, node):
#         """
#         This is the generic method that initializes the
#         dynamic dispatcher.
#         """

#     @visit.when(BaseNode)
#     def visit(self, node):
#         """
#         Will run for nodes that do specifically match the
#         provided type.
#         """
#         print "Unrecognized node:", node
 
#     @visit.when(AssignmentExpression)
#     def visit(self, node):
#         """ Matches nodes of type AssignmentExpression. """
#         node.children[0].accept(self)
#         print '='
#         node.children[1].accept(self)
 
#     @visit.when(VariableNode)
#     def visit(self, node):
#         """ Matches nodes that contain variables. """
#         print node.name
 
#     @visit.when(Literal)
#     def visit(self, node):
#         """ Matches nodes that contain literal values. """
#         print node.value
