# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase, _print
import grammar
import action

    
@TestCase(grammar)
def test_constant_primary(self):
    pass

@TestCase(grammar)
def test_primary(self):
    _print(self.check_pass("10"))
    _print(self.check_pass("foo.bar.hoge[5].A[1]"))
    _print(self.check_pass("foo.bar.hoge[5].A[1][X][y]"))




if __name__=='__main__':
    unittest.main()

