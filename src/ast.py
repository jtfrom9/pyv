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


