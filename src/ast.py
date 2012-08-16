# -*- coding: utf-8 -*-

class Numeric(object):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
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

class State2Value(FixedWidthValue):
    def __init__(self, string, width, vtype, value):
        super(State2Value,self).__init__(string, width, vtype)
        self.value = value
    def __repr__(self):
        return "{clsname}({value},[{left}:{right}],{string})".format(
            clsname=self.__class__.__name__,
            left=self.width-1,
            right=0,
            value=self.value,
            string=self.string)

class State4Value(FixedWidthValue):
    def __init__(self, string, width, vtype, bits):
        super(State4Value,self).__init__(string,width,vtype)
        self.bits = bits
        
class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self.value = float(string)


class Id(object):
    pass

class BasicId(Id):
    def __init__(self,string):
        assert isinstance(string,str)
        self.string = string
    def __repr__(self):
        return "{cls}({s})".format(cls=self.__class__.__name__, s=self.string)

class RangedId(BasicId):
    def __init__(self,string,_range):
        super(RangedId,self).__init__(string)
        self.range = _range
    def __repr__(self):
        return "{cls}({s}{r})".format(cls=self.__class__.__name__, s=self.string, r=str(self.range))

class IndexedId(BasicId):
    def __init__(self,string,index):
        super(IndexedId,self).__init__(string)
        self.index = index
    def __repr__(self):
        return "{cls}({s}[{i}])".format(cls=self.__class__.__name__, s=self.string, i=self.index)
        

class HierarchicalId(BasicId):
    def __init__(self, string, headId, headIndex, tailIds):
        super(HierarchicalId,self).__init__(string)
        self.headId = headId
        self.headIndex = headIndex
        self.tailIds = tailIds

    def __repr__(self):
        tailStr =".".join(str(id) for id in self.tailIds) 
        if tailStr: tailStr = "."+tailStr
        return "{cls}({head}[{index}]{tail})".format(cls=self.__class__.__name__,
                                                     head=self.headId,
                                                     index=self.headIndex,
                                                     tail=tailStr)
    def addId(self,id):
        self.tailIds.append(id)
    
class Range(object):
    def __init__(self,s,left,right):
        self.string = s
        self.left   = left
        self.right  = right
    def __repr__(self):
        return "[{l}:{r}]".format(l=self.left, r=self.right)

