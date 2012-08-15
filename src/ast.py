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
        self.vale = value

class State4Value(FixedWidthValue):
    def __init__(self, string, width, vtype, bits):
        super(State4Value,self).__init__(string,width,vtype)
        self.bits = bits
        
    @staticmethod
    def makeAllBits(width, v):
        return v*width

class Float(Numeric):
    def __init__(self, string):
        super(Float,self).__init__(string)
        self.value = float(string)
    def __repr__(self):
        return self.value


