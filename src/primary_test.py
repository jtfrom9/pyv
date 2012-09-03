# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _print
import grammar
import action

@TestCase2(grammar.constant_primary)
def test131(self):
    _print(self.check_fail("A"))
    _print(self.check_pass("1"))
    

@TestCase2(grammar.module_path_primary)
def test132(self):
    pass


@TestCase2(grammar.primary)
def test133(self):
    _print(self.check_pass("10"))
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][3:1]")) # now fail


@TestCase2(grammar.net_lvalue)
def test134(self):
#    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge.foo[1:0]").asXML())
    print(self.check_pass("hoge.foo[0][1][2][1:0]").asXML())

@TestCase2(grammar.variable_lvalue)
def test135(self):
    pass


if __name__=='__main__':
    unittest.main()

