# -*- coding: utf-8 -*-
from abc import abstractmethod, ABCMeta

class Visitor(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def visit(self, node):
        pass

class BaseNode(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def traverse(self,visitor):
        pass

class A(BaseNode):
    def __init__(self, children):
        self.children = children
    def traverse(self,visitor):
        visitor.visit(self)
        for c in self.children:
            c.traverse(visitor)

class B(BaseNode):
    def __init__(self,name):
        self.name = name
    def traverse(self,visitor):
        print("traverse: B({0})".format(self.name))
        visitor.visit(self)

class C(BaseNode):
    def traverse(self,visitor):
        print("traverse: C")
        visitor.visit(self)

class GenericVisitorMixin(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dispatch(self):
        pass

    @abstractmethod
    def default_handler(self):
        pass

    def visit(self, node):
        func = self.dispatch(node)
        if func:
            return func(node)
        else:
            return self.default_handler(node)


class TestVisitor(GenericVisitorMixin, Visitor):
    def dispatch(self, node):
        return { A: self.visitA,
                 B: self.visitB }.get(type(node),None)

    def default_handler(self, node):
        print("TestVisitor::default")

    def visitA(self, node):
        print("TestVisitor::visitA")

    def visitB(self, node):
        print("TestVisitor::visitB")


class HogeVisitor(GenericVisitorMixin, Visitor):
    def dispatch(self, node):
        if type(node) is C:
            return self.handler
        else:
            return None

    def handler(self, node):
        print("hoge::handler")

    def default_handler(self,node):
        print("HogeVisitor")


class CompositVisitor(GenericVisitorMixin, Visitor):
    def __init__(self):
        self._visitors = ( HogeVisitor(), TestVisitor() )
        
    def dispatch(self, node):
        for v in self._visitors:
            f = v.dispatch(node)
            if f: return f
        return None

    def default_handler(self,node):
        print("CompositVisitor")


blist = [ B("hoge"), B("foo"), B("bar"), C() ]
a = A(blist)

#v = TestVisitor()
v = CompositVisitor()
a.traverse(v)

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
