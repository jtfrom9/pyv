# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action

    
@TestCase(grammar)
def test_constant_primary(self):
    pass

@TestCase(grammar)
def test_primary(self):
    print(self.check_pass("10").asXML())
    print(self.check_pass("foo.bar.hoge[5].A[1]").asXML())
    print(self.check_pass("foo.bar.hoge[5].A[1][X][y]").asXML())




if __name__=='__main__':
    unittest.main()

