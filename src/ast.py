# -*- coding: utf-8 -*-
import collections
from abc import abstractmethod, ABCMeta
import pyparsing as pp

class AstNode(object):
    def __str__(self):
        return self.__class__.__name__
    def __repr__(self):
        return self.__str__();

    def traverseChildren(self,visitor,arg):
        pass

    def traverse(self,visitor,arg):
        children = visitor.visit(self, arg)
        if children:
            newarg = arg.createChild(self)
            for c in children:
                c.traverse(visitor,newarg)
        else:
            self.traverseChildren(visitor,arg)
        return visitor

class Null(AstNode):
    pass
null = Null()

def nodeInfo(node):
    if isinstance(node,str):
        return "str: {0}".format(node)
    if isinstance(node,pp.ParseResults):
        return "pr: {0}".format([prop for prop in dir(node) if not prop.startswith("__")])
    if isinstance(node,AstNode):
        return "ast.{0}: {1}".format(node.__class__.__name__, repr(node))
    return type(node)

def repr_(inst, *kws):
    return "{cls}({props})".format(
        cls = inst.__class__.__name__,
        props = kws)
    
class Range(AstNode):
    def __init__(self,left,right):
        self._left_expr  = left
        self._right_expr = right
    def __str__(self):
        return "[{l}:{r}]".format(l= str(self._left_expr), r=str(self._right_expr))
    def __repr__(self):
        return repr_(self,{'left':self._left_expr, 'right':self._right_expr})

WaitTypeId   = 0
WaitTypeExpr = 1
WaitTypeAny  = 2
class EventControl(AstNode):
    def __init__(self, type, obj):
        self._type = type
        self._wait_obj = obj
    def __str__(self):
        if self._type==WaitTypeId or self._type==WaitTypeExpr:
            return "@(" + str(self._wait_obj) + ")"
        elif self._type==WaitTypeAny:
            return "@*"
        else: assert(False)

class DelayControl(AstNode):
    def __init__(self, exp):
        self._delay_exp = exp
    def __str__(self):
        return "#({0})".format(self._delay_exp)


# Numeric
class Numeric(AstNode):
    '''TODO: to be a child of numbers.Number abc class'''
    def __init__(self, string):
        self._string = string
    def __str__(self):
        return self._string
    def __repr__(self):
        return self.__class__.__name__ + "(" + self._string + ")"

class FixedWidthValue(Numeric):
    Binary  = 2
    Octal   = 8
    Hex     = 16
    Decimal = 10

    def __init__(self, string, bit_width, val_type):
        super(FixedWidthValue,self).__init__(string)
        self._bit_width = bit_width
        self._val_type  = val_type

    @staticmethod
    def type2str(vtype):
        tab = { FixedWidthValue.Binary  : "b", 
                FixedWidthValue.Octal   : "o", 
                FixedWidthValue.Hex     : "h", 
                FixedWidthValue.Decimal : "d" }
        return tab[vtype]


class Int2(FixedWidthValue):
    def __init__(self, string, bit_width, val_type, value):
        super(Int2,self).__init__(string, bit_width, val_type)
        self._value = value
    def __repr__(self):
        return self.__class__.__name__ + "({string}, {bit_width}, {val_type}, {value})".format(
            string    = self._string,
            bit_width = self._bit_width,
            val_type  = FixedWidthValue.type2str(self._val_type),
            value     = self._value)

class Int4(FixedWidthValue):
    def __init__(self, string, bit_width, val_type, bits):
        super(Int4,self).__init__(string, bit_width, val_type)
        self._bits = bits
    def __repr__(self):
        return self.__class__.__name__ + "({string}, {bit_width}, {val_type}, {bits})".format(
            string    = self._string,
            bit_width = self._bit_width,
            val_type  = FixedWidthValue.type2str(self._val_type),
            bits      = self._bits)
        
class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self._value = float(string)
    def __repr__(self):
        return self.__class__.__name__ + "({0})".format(self._string)


# Id
class Id(AstNode):
    def hasRange(self):
        return False
    def hasIndex(self):
        return False
    def isHierachical(self): 
        return False

class BasicId(Id):
    def __init__(self, string):
        self._string = string
    def __str__(self):
        return self._string
    def __repr__(self):
        return self.__class__.__name__ + "({0})".format(self._string)

class RangedId(BasicId):
    def __init__(self, string, brange):
        super(RangedId,self).__init__(string)
        self._brange = brange
    def hasRange(self):
        return True
    def getRange(self):
        return self._brange
    def __str__(self):
        return self._string + str(self._brange)
    def __repr__(self):
        return self.__class__.__name__ + "({0}, {1})".format(self._string, repr(self._brange))

class IndexedId(BasicId):
    def __init__(self, string, index):
        super(IndexedId,self).__init__(string)
        self._index = index
    def hasIndex(self):
        return True
    def getIndex(self):
        return self._index
    def __str__(self):
        return self._string + "[" + str(self._index) + "]"
    def __repr__(self):
        return self.__class__.__name__ + "({0}, {1})".format(self._string, repr(self._index))
        
class HierarchicalId(Id):
    def __init__(self, ids):
        self._ids = []
        if isinstance(ids, list):
            self._ids = ids
        elif isinstance(ids, collections.Iterable):
            self._ids = [x for x in ids]
        else:
            raise Exception("HierarchicalId: Invalid ids")
    def isHierachical(self): 
        return True
    def addId(self,id):
        self._ids.append(id)
    def __str__(self):
        return ".".join(str(i) for i in self._ids)
    def __repr__(self):
        return self.__class__.__name__ + "({0})".format(self._ids)
    def each_id(self):
        for i in self._ids:
            yield i

# Expression
class Expression(AstNode):
    def eval(self):
        pass

class Primary(Expression):
    pass

class NumberPrimary(Primary):
    def __init__(self, number):
        self._number = number
    def __str__(self):
        return str(self._number) 
    def __repr__(self):
        return repr(self._number)

class IdPrimary(Primary):
    def __init__(self, headid, index_exprs=[], range_expr=None):
        self._headid      = headid
        self._index_exprs = index_exprs
        self._range_exprs = range_expr
    def _each_symbols(self):
        yield self._headid
        for e in self._index_exprs: 
            yield e
        if self._range_exprs: 
            yield self._range_exprs
    def __str__(self):
        return ".".join(str(x) for x in self._each_symbols())
    def __rstr__(self):
        return ".".join("(" + repr(x) +")" for x in self._each_symbols())

class UnaryExpression(Expression):   # fixme. some types for op must be defined
    def __init__(self, op, expr):
        self._op   = op
        self._expr = expr
    def __str__(self):
        return "({0}({1}))".format(self._op, self._expr)

class BinaryExpression(Expression):  # fixme. not considered well for more than 3 exprs
    def __init__(self, op, exprs):
        self._op    = op
        self._exprs = exprs
    def __str__(self):
        return "(" + str(" " + self._op + " ").join( str(e) for e in self._exprs ) + ")"
    def traverseChildren(self,visitor,arg):
        for index, term in enumerate(self._exprs):
            term.traverse(visitor, arg.createChild(self, index=index))

class ConditionalExpression(Expression):
    def __init__(self, cond_expr, then_expr, else_expr):
        self._cond_expr = cond_expr
        self._then_expr = then_expr
        self._else_expr = else_expr
    def __str__(self):
        return "({cond})?({then}):({_else})".format(
            cond = str(self._cond_expr),
            then = str(self._then_expr),
            _else = str(self._else_expr))

class Concatenation(Expression):
    def __init__(self, exprs):
        self._exprs = exprs
    def __str__(self):
        return "{" + ",".join(str(exp) for exp in self._exprs) + "}"

class FunctionCall(Expression):
    def __init__(self, func_id, args):
        self._func_id = func_id
        self._args    = args
    def __str__(self):
        return "{func}({args})".format(
            func = self._func_id,
            args = ",".join(str(arg) for arg in self._args))

class EdgeExpression(Expression):
    def __init__(self, edge_type, expr):
        ''' 
        - edge_type : str ( 'posedge' | 'negedge' )
        - expr      : Expression
        '''
        self._edge_type = edge_type 
        self._expr      = expr
    def __str__(self):
        return "(" + self._edge_type + ":" + str(self._expr) + ")"
    def __repr__(self):
        return repr_(self,{'edge_type':self._edge_type, 'expr':self._expr})


# Statement

class NodeList(AstNode):
    def __init__(self, nodes):
        self._nodes = nodes
    def __str__(self):
        other = ""
        if len(self._nodes)==1:
            other="({0})".format(str(self._nodes[0]))
        elif len(self._nodes)>1:
            other="({0},..)".format(str(self._nodes[0]))
        return self.__class__.__name__ + other
    def __iter__(self):
        for n in self._nodes: yield n

    def traverseChildren(self,visitor,arg):
        newarg = arg.createChild(self)
        for n in self._nodes:
            n.traverse(visitor,newarg)

class Statement(AstNode):
    pass

class Assignment(Statement):
    def __init__(self, left, delay_event, right, blocking=True):
        self._left_expr   = left
        self._delay_event = delay_event
        self._right_expr  = right
        self._blocking    = blocking
        self._continuous  = ""          # fixme

    isBlocking = property(lambda self: self._blocking)

    def __str__(self):
        return "{conti}{left}{eq}{right}".format(
            conti = self._continuous+" " if self._continuous else "",
            left  = str(self._left_expr),
            eq    = "=" if self._blocking else "<=",
            right = str(self._right_expr))

    def __repr__(self):
        return repr_(self,{'left':self._left_expr, 
                           'right':self._right_expr, 
                           'blocking':self._blocking})

    def traverse(self,visitor,arg):
        children = visitor.visit(self, arg)
        if children:
            newarg = arg.createChild(self)
            for c in children:
                c.traverse(visitor,newarg)
        else:
            self.traverseChildren(visitor,arg)
        return visitor

    def traverseChildren(self,visitor,arg):
        self._left_expr.traverse(visitor,arg.createChild(self, pos='left'))
        self._right_expr.traverse(visitor,arg.createChild(self, pos='right'))


class ReleaseLeftValue(Statement):
    def __init__(self, _type, lvalue):
        self._type   = _type
        self._lvalue = lvalue
    def __str__(self):
        return self._type + " " + str(self._lvalue)

class ConditionalStatement(Statement):
    def __init__(self, cond_stmt_list, else_stmt):
        self._cond_stmt_list = cond_stmt_list
        self._else_stmt      = else_stmt
    def longName(self):
        cond, stmt = self._cond_stmt_list[0]
        rest_if_ccs = ""
        # for statements longName() method no longer makes no sense.
        # Statement classes should has multi-line pretty print functionality
        return "({cls} {if_cs}{rest_if_cs}{else_s})".format(cls=self.__class__.__name__,
                                                            if_cs = "cond:{0}, then:{1}".format(cond.longName(), stmt.longName()),
                                                            rest_if_cs = "...",
                                                            else_s  = "else:{0}".format(self._else_stmt.longName() if self._else_stmt else ""))
    
    def traverseChildren(self, visitor, arg):
        for index, (cond, stmt) in enumerate(self._cond_stmt_list):
            cond.traverse(visitor, arg.createChild(self, index=index, last=False))
            stmt.traverse(visitor, arg.createChild(self, cond=cond, index=index, last=False))
        if self._else_stmt:
            self._else_stmt.traverse(visitor, arg.createChild(self,last=True))
            
    def eachCondAndStatements(self):
        for cond, stmt in self._cond_stmt_list:
            yield (cond, stmt)
        if self._else_stmt:
            yield (None, self._else_stmt)


class CaseStatement(Statement):
    class Item(object):
        def __init__(self, cond_exprs, stmt):
            self.cond_exprs = cond_exprs
            self.stmt       = stmt
        def __str__(self):
            if len(self.cond_exprs) > 0:
                cond_str = "case " + ",".join(str(e) for e in self.cond_exprs)
            else:
                cond_str = "case-default"
            return "({cond}: {stmt})".format(
                cond = cond_str,
                stmt = str(self.stmt))
    def __init__(self, case_type, expr, case_items):
        """
        - case_type : str ( 'case' | 'casez' | 'casex' )
        - expr      : Expression
        - case_items: list (of Item)
        """
        self._case_type  = case_type
        self._expr       = expr
        self._case_items = case_items
    def __str__(self):
        return "{0}({1})".format(self._case_type, str(self._expr))

    def eachItems(self):
        for i in self._case_items:
            yield i

class LoopStatement(Statement):
    pass

class ForLoopStatement(LoopStatement):
    def __init__(self, init_assign, cond_expr, next_assign, stmt):
        """
        - init_assign : Assignment
        - cond_expr   : Expression
        - next_assign : Assignment
        - stmt        : Statement
        """
        self._init_assign = init_assign
        self._cond_expr   = cond_expr
        self._next_assign = next_assign
        self._stmt        = stmt
    def __str__(self):
        return "For({0};{1};{2})...".format(str(self._init_assign),
                                            str(self._cond_expr),
                                            str(self._next_assign))

class Block(Statement):
    def __init__(self, item_decls, statements, seq=True):
        self._item_decls = item_decls
        self._statements = statements
        self._seq        = seq

    isSequencial = property(lambda self: self._seq)

    def __str__(self):
        if self._seq: return "Block(begin-end)"
        else: return "Block(fork-join)"
    
    def traverseChildren(self, visitor, arg):
        decl_arg = arg.createChild(self, decl=True)
        for decl in self._item_decls:
            decl.traverse(visitor, decl_arg)
        stmt_arg = arg.createChild(self, decl=False)
        for stmt in self._statements:
            stmt.traverse(visitor, stmt_arg)
    
    def eachStatements(self):
        for s in self._statements: yield s


class Trigger(Statement):
    def __init__(self,_id):
        self._id = _id
    def __str__(self):
        return "->" + str(self._id)

class Wait(Statement):
    def __init__(self, exp, stmt):
        self._exp = exp
        self._stmt = stmt
    def __str__(self):
        return "(wait @{0} {1})".format(self._exp, self._stmt)

class TimingControlStatement(Statement):
    def __init__(self, timing, stmt):
        self._timing = timing
        self._stmt   = stmt
    def __iter__(self):
        for s in self._stmt: yield s
    def __str__(self):
        return "{0}{1}".format(self._timing, self._stmt)
    def traverseChildren(self, visitor, arg):
        self._stmt.traverse(visitor,arg.createChild(self))

# ModuleGenerateItem

class ConstructStatementItem(Statement):
    def __init__(self, construct_type, stmt):
        """
        - construct_type : str ( 'always' | 'initial' )
        - stmt           : Statement
        """
        assert(isinstance(stmt,Statement))
        self._construct_type = construct_type
        self._stmt           = stmt
    
    type      = property(lambda self: self._construct_type)
    statement = property(lambda self: self._stmt)

    def __str__(self):
        return self._construct_type + ":" + str(self._stmt)
    def traverseChildren(self, visitor, arg):
        self._stmt.traverse(visitor,arg.createChild(self))

class ContinuousAssignmentItems(Statement):
    def __init__(self, continuous_type, stmt_list):
        """
        - continuous_type : str ('assign' | 'force' )
        - stmt_list       : NodeList
        """
        assert(isinstance(stmt_list, NodeList))
        for s in stmt_list:
            if not s.isBlocking: raise Exception('contents of ContinuousAssignmentItems must be blocking assignment')

        self._stmt_list       = stmt_list
        self._continuous_type = continuous_type

    type = property(lambda self: self._continuous_type)

    def eachStatements(self):
        for s in self._stmt_list:
            yield s

    def __str__(self):
        return self._continuous_type + ":" + str(self._stmt_list)

    def traverseChildren(self, visitor, arg):
        self._stmt_list.traverse(visitor,arg.createChild(self))

