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
        self.parent = parent
        if init_level:
            self.level = init_level
        else:
            self.level = arg.level + 1 if arg else 0

    def __call__(self, arg_dict):
        for key,value in arg_dict.items():
            setattr(self,key,value)
        return self

root_arg = Arg(None)

class BasicPrinterVisitor(GenericVisitorMixin, Visitor):
    def __init__(self, out, indent=2):
        self.out = out
        self.indent = indent

    def dispatch(self, node):
        return None

    def default_handler(self,node,arg):
        #print("lv={0} : {1}".format(arg.level, node.__class__.__name__))
        self.out.write("{spc}{data}\n".format(spc  = " " * arg.level * self.indent,
                                              data = str(node)))




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
