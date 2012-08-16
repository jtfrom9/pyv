# -*- coding: utf-8 -*-

class AstNode(object):
    def shortName(self):
        return self.__class__.__name__
    def longName(self):
        return self.shortName()
    def __repr__(self):
        return self.longName()

class Numeric(AstNode):
    def __init__(self, string):
        self.string = string
    def longName(self):
        return self.__class__.__name__ + "(" + self.string + ")"

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

class State2Value(FixedWidthValue):
    def __init__(self, string, width, vtype, value):
        super(State2Value,self).__init__(string, width, vtype)
        self.value = value
    def shortName(self):
        return "(S2:{0}:{1})".format(FixedWidthValue.type2str(self.vtype), str(int(self.value,vtype)))
    def longName(self):
        return "({clsname} {value}({vtype}:{string} [{left}:{right}]))".format(
            clsname = self.__class__.__name__,
            vtype   = FixedWidthValue.type2str(self.vtype),
            left    = self.width-1,
            right   = 0,
            value   = self.value,
            string  = self.string)

class State4Value(FixedWidthValue):
    def __init__(self, string, width, vtype, bits):
        super(State4Value,self).__init__(string,width,vtype)
        self.bits = bits
    def shortName(self):
        return "(S4 {vtype}:{string})".format(
            vtype   = FixedWidthValue.type2str(self.vtype),
            string  = self.string)
    def longName(self):
        return "({clsname} {vtype}:{string} [{left}:{right}])".format(
            clsname = self.__class__.__name__,
            vtype   = FixedWidthValue.type2str(self.vtype),
            left    = self.width-1,
            right   = 0,
            string  = self.string)
        
class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self.value = float(string)


class Id(AstNode):
    pass

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
        return "(i:{0}{1})".format(self.string, str(self.range))
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
        
class HierarchicalId(BasicId):
    def __init__(self, headId, headIndex, tailIds):
        super(HierarchicalId,self).__init__(headId.string)
        self.headId    = headId
        self.headIndex = headIndex
        self.tailIds   = tailIds

    def shortName(self):
        tailStr =".".join(id.shortName() for id in self.tailIds) 
        if tailStr: tailStr = "." + tailStr
        return "(i:{head}{index}{tail})".format(head = self.string,
                                                index = "[{0}]".format(self.headIndex) if self.headIndex else "",
                                                tail = tailStr)
    def longName(self):
        tailStr =".".join(str(id) for id in self.tailIds) 
        if tailStr: tailStr = "."+tailStr
        return "({cls} {head}{index}{tail})".format(cls=self.__class__.__name__,
                                                   head=self.string,
                                                   index="[{0}]".format(self.headIndex) if self.headIndex else "",
                                                   tail=tailStr)
    def addId(self,id):
        self.tailIds.append(id)
    
class Range(AstNode):
    def __init__(self,left,right):
        self.left   = left
        self.right  = right
    def shortName(self):
        return "{l}:{r}".format(l=self.left.shortName(), r=self.right.shortName())
    def longName(self):
        return "[{l}:{r}]".format(l=self.left, r=self.right)

