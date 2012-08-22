# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action

@TestCase(grammar)
def test_number(self):
    print(self.check_pass("23.5").asXML())
    print(self.check_pass("1.0e+1").asXML())
    print(self.check_pass("0.0E-30").asXML())
    print(self.check_pass("0.0").asXML())
    print(self.check_pass("123").asXML())
    print(self.check_pass("01").asXML())
    print(self.check_pass("'d0").asXML())
    print(self.check_pass("5'd0").asXML())

if __name__=='__main__':
    unittest.main()
