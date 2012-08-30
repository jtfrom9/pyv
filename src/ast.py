# -*- coding: utf-8 -*-
from collections import Iterable
import pyparsing as pp

class AstNode(object):
    def shortName(self):
        return self.__class__.__name__
    def longName(self):
        return self.shortName()
    def __repr__(self):
        return self.longName()

def nodeInfo(node):
    if isinstance(node,str):
        return "str: {0}".format(node)
    if isinstance(node,pp.ParseResults):
        return "pr: {0}".format([prop for prop in dir(node) if not prop.startswith("__")])
    if isinstance(node,AstNode):
        return "ast: {0}".format(str(node))
    
class Null(AstNode):
    pass
null = Null()

class Numeric(AstNode):
    def __init__(self, string):
        self.string = string
    def longName(self):
        return "(" + self.__class__.__name__ + ":" + self.string + ")"
    def value(self):
        pass

class FixedWidthValue(Numeric):
    Binary = 2
    Octal  = 8
    Hex    = 16
    Decimal = 10

    def __init__(self, string, width, vtype):
        self.string = string
        self.width  = width
        self.vtype  = vtype

    @staticmethod
    def type2str(vtype):
        tab = { FixedWidthValue.Binary: "b", 
                FixedWidthValue.Octal : "o", 
                FixedWidthValue.Hex : "h", 
                FixedWidthValue.Decimal : "d" }
        return tab[vtype]


class Int2(FixedWidthValue):
    def __init__(self, string, width, vtype, value):
        super(Int2,self).__init__(string, width, vtype)
        self.value = value
    def shortName(self):
        return "(I2:{0}:{1})".format(FixedWidthValue.type2str(self.vtype), str(int(self.value,vtype)))
    def longName(self):
        return "(I2:{value}({vtype}:{string} [{left}:{right}]))".format(
            clsname = self.__class__.__name__,
            vtype   = FixedWidthValue.type2str(self.vtype),
            left    = self.width-1,
            right   = 0,
            value   = self.value,
            string  = self.string)

class Int4(FixedWidthValue):
    def __init__(self, string, width, vtype, bits):
        super(Int4,self).__init__(string,width,vtype)
        self.bits = bits
    def shortName(self):
        return "(S4V:{vtype}:{string})".format(
            vtype   = FixedWidthValue.type2str(self.vtype),
            string  = self.string)
    def longName(self):
        return "(S4V:{vtype}:{string} [{left}:{right}])".format(
            clsname = self.__class__.__name__,
            vtype   = FixedWidthValue.type2str(self.vtype),
            left    = self.width-1,
            right   = 0,
            string  = self.string)
        
class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self.value = float(string)
    def shortName(self):
        return "(F:{0})".format(self.string)
    def longName(self):
        return self.shortName()

class Id(AstNode):
    def hasRange(self):
        return getattr(self,'range',False)
    def hasIndex(self):
        return getattr(self,'index',False)
    def isHierachical(self): 
        return False

class BasicId(Id):
    def __init__(self,string):
        assert isinstance(string,str)
        self.string = string
    def shortName(self):
        return "(i:{0})".format(self.string)
    def longName(self):
        return "({cls} {s})".format(cls=self.__class__.__name__, s=self.string)

class RangedId(BasicId):
    def __init__(self,string,_range):
        super(RangedId,self).__init__(string)
        self.range = _range
    def shortName(self):
        return "(i:{0}{1})".format(self.string, self.range.shortName())
    def longName(self):
        return "({cls} {s}{r})".format(cls=self.__class__.__name__, s=self.string, r=str(self.range))

class IndexedId(BasicId):
    def __init__(self,string,index):
        super(IndexedId,self).__init__(string)
        self.index = index
    def shortName(self):
        return "(i:{0}[{1}])".format(self.string, self.index)
    def longName(self):
        return "({cls} {s}[{i}])".format(cls=self.__class__.__name__, s=self.string, i=self.index)
        
class HierarchicalId(Id):
    def __init__(self, ids):
        self.ids = []
        if isinstance(ids, Iterable):
            self.ids = [x for x in ids]
        elif isinstance(ids, list):
            self.ids = ids
        else:
            raise Exception("Invalid ids")

    def isHierachical(self): 
        return True

    def addId(self,id):
        self.ids.append(id)

    def shortName(self):
        return "(i:{0})".format(".".join(id.shortName() for id in self.ids))

    def longName(self):
        return "({cls} {str})".format(cls = self.__class__.__name__,
                                      str = "".join(id.longName() for id in self.ids))

# class HierarchicalId(BasicId):
#     def __init__(self, headId, headIndex, tailIds):
#         super(HierarchicalId,self).__init__(headId.string)
#         self.headId    = headId
#         self.headIndex = headIndex
#         self.tailIds   = tailIds

#     def shortName(self):
#         tailStr =".".join(id.shortName() for id in self.tailIds) 
#         if tailStr: tailStr = "." + tailStr
#         return "(i:{head}{index}{tail})".format(head  = self.string,
#                                                 index = "[{0}]".format(self.headIndex) if self.headIndex else "",
#                                                 tail  = tailStr)
#     def longName(self):
#         tailStr =".".join(str(id) for id in self.tailIds) 
#         if tailStr: tailStr = "."+tailStr
#         return "({cls} {head}{index}{tail})".format(cls   = self.__class__.__name__,
#                                                     head  = self.string,
#                                                     index = "[{0}]".format(self.headIndex) if self.headIndex else "",
#                                                     tail  = tailStr)
#     def addId(self,id):
#         self.tailIds.append(id)
    
class Range(AstNode):
    def __init__(self,left,right):
        print("left={0}, right={0}".format(nodeInfo(left),nodeInfo(right)))
        self.left   = left
        self.right  = right
    def shortName(self):
        return "{l}:{r}".format(l=self.left, r=self.right)
    def longName(self):
        return "[{l}:{r}]".format(l=self.left, r=self.right)

class Statement(AstNode):
    def dump(self):
        pass

class Assignment(Statement):
    def __init__(self, left, delay_event, exp, blocking=True):
        self.left        = left
        self.delay_event = delay_event
        self.exp         = exp
        self.blocking    = blocking

class ContinuousAssignment(Assignment):
    def __init__(self, prefix, assignmentStatement):
        self.prefix              = prefix
        self.assignmentStatement = assignmentStatement

class Conditional(Statement):
    def __init__(self, cs_list, else_s):
        assert len(cs_list) > 0
        self.cs_list = cs_list
        self.else_s  = else_s
    def longName(self):
        first_exp, first_s = self.cs_list[0]
        rest_if_ccs = ""
        # for statements longName() method no longer makes no sense.
        # Statement classes should has multi-line pretty print functionality
        return "({cls} {if_cs}{rest_if_cs}{else_s})".format(cls=self.__class__.__name__,
                                                            if_cs = "cond:{0}, then:{1}".format(first_exp, first_s.longName()),
                                                            rest_if_cs = "...",
                                                            else_s  = "else:{0}".format(self.else_s.longName() if self.else_s else ""))
    

class Case(Statement):
    pass

class Loop(Statement):
    pass

class SequencialBlock(Statement):
    def __init__(self, item_decls, statements):
        self.item_decls = item_decls
        self.statements = statements

class ProceduralContinuousAssignment(Assignment): #assign
    pass

class ProceduralTimingControl(Statement): # #, @
    pass

class WaitEvent(Statement):
    pass

class EventTrigger(Statement):
    pass

class Expression(AstNode):
    def __init__(self):
        pass
    
class Primary(Expression):
    def primaryLongInfo():
        return ""
    def primaryShortInfo():
        return ""
    def longName(self):
        return "(Primary {0})".format(self.primaryLongInfo())
    def shortName(self):
        return "(Primary {0})".format(self.primaryShortInfo())

class NumberPrimary(Primary):
    def __init__(self, number):
        self.number = number
    def primaryLongInfo(self):
        return self.number.longName()
    def primaryShortInfo(self):
        return self.number.shortName()

class IdPrimary(Primary):
    def __init__(self, id, exps, range):
        self.id    = id
        self.exps  = exps
        print("IdPrimary: exps={0}".format(exps))
        self.range = range


    def primaryLongInfo(self):
        return self.id.longName() \
            + "".join("[" + e.longName() + "]" for e in self.exps ) \
            + (("[" + self.range.longName() + "]") if self.range else "")
    def primaryShortInfo(self):
        return self.id.longName() \
            + "".join("[" + e.shortName() + "]" for e in self.exps ) \
            + (("[" + self.range.shortName() + "]") if self.range else "")
    

class UnaryExpression(Expression):
    def __init__(self, op, exp):
        self.op = op
        self.exp = exp
    def longName(self):
        return "({0} {1})".format(self.op, self.exp)

class BinaryExpression(Expression):
    def __init__(self,op,left,right):
        self.op   =op
        self.lexp = left
        self.rexp = right
    def longName(self):
        return "({0} {1} {2})".format(self.op, self.lexp[0], self.rexp[0])

class LeftSideValue(Expression):
    def __init__(self, id, indexes, range):
        self.id      = id
        self.indexes = indexes
        self.range   = range

class Concatenation(Expression):
    pass
