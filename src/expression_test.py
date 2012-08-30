# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2
import grammar
import action

    
@TestCase2(grammar.event_expression)
def test87(self):
    pass


@TestCase2(grammar.base_expression)
def test115(self):
    pass


@TestCase2(grammar.conditional_expression)
def test116(self):
    pass


@TestCase2(grammar.constant_base_expression)
def test117(self):
    pass


@TestCase2(grammar.constant_expression)
def test118(self):
#    print(self.check_pass("func()").asXML())
    print(self.check_pass("A").asXML())


@TestCase2(grammar.constant_mintypmax_expression)
def test119(self):
    pass


@TestCase2(grammar.constant_range_expression)
def test120(self):
    print(self.check_pass("1:0").asXML())


@TestCase2(grammar.dimension_constant_expression)
def test121(self):
    pass


@TestCase2(grammar.expression)
def test122(self):
    print(self.check_pass("A+10").asXML())
    print(self.check_pass("-X").asXML())
    print(self.check_pass("-X+10+A").asXML())


@TestCase2(grammar.lsb_constant_expression)
def test123(self):
    pass


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
    pass


@TestCase2(grammar.range_expression)
def test129(self):
    pass


@TestCase2(grammar.width_constant_expression)
def test130(self):
    pass

if __name__=='__main__':
    unittest.main()
