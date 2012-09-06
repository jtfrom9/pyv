# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _print
from pyparsing import stringEnd
import grammar
import action

    
@TestCase2(grammar.base_expression)
def test115(self):
    _print(self.check_pass("1+2"))
    _print(self.check_pass("X+2"))
    _print(self.check_pass("0"))
    _print(self.check_pass("A+10"))
    _print(self.check_pass("-X"))
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("-X+1"))
    _print(self.check_pass("-X+1+A"))
    _print(self.check_pass("-X+1*A"))


@TestCase2(grammar.conditional_expression)
def test116(self):
    _print(self.check_pass(" 0 ? 1 : 2"))
    _print(self.check_pass(" A ? 1 : 2"))
    _print(self.check_pass(" A+1 ? X<0 : Y==1"))


@TestCase2(grammar.constant_base_expression)
def test117(self):
    _print(self.check_pass("1"))
    _print(self.check_pass("1+2"))
    _print(self.check_fail("X+2"))

@TestCase2(grammar.constant_expression)
def test118(self):
    _print(self.check_fail("A"))
    _print(self.check_pass("1"))
    _print(self.check_pass("1 + 2"))

@TestCase2(grammar.constant_mintypmax_expression)
def test119(self):
    pass

@TestCase2(grammar.constant_range_expression)
def test120(self):
    _print(self.check_pass("1:0"))
    _print(self.check_pass("1:0+10"))
    _print(self.check_fail("1:X"))


@TestCase2(grammar.dimension_constant_expression)
def test121(self):
    _print(self.check_fail("1:0"))
    _print(self.check_pass("20"))


@TestCase2(grammar.expression)
def test122(self):
    _print(self.check_pass("0"))
    _print(self.check_pass("A+10"))
    _print(self.check_pass("-X"))
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("-X+1"))
    _print(self.check_pass("-X+1+A"))
    _print(self.check_pass("-X+1*A"))

@TestCase2(grammar.lsb_constant_expression)
def test123(self):
    _print(self.check_fail("1:0"))
    _print(self.check_pass("20"))


@TestCase2(grammar.mintypmax_expression)
def test124(self):
    pass


@TestCase2(grammar.module_path_conditional_expression)
def test125(self):
    pass


@TestCase2(grammar.module_path_expression)
def test126(self):
    pass


@TestCase2(grammar.module_path_mintypmax_expression)
def test127(self):
    pass


@TestCase2(grammar.msb_constant_expression)
def test128(self):
    _print(self.check_fail("1:0"))
    _print(self.check_pass("20"))


@TestCase2(grammar.range_expression)
def test129(self):
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("1:0"))
    _print(self.check_fail("1+:0"))

@TestCase2(grammar.width_constant_expression)
def test130(self):
    pass

if __name__=='__main__':
    unittest.main()

