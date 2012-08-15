# -*- coding: utf-8 -*-
import pyparsing as pp
import parser as p
import sys

import unittest
from test_common import GrammarTestCase, TestCase

@TestCase(p)
def test_statement(self):
    print(self.check_pass("A=B;").asXML())
    print(self.check_pass("A<=B;").asXML())

@TestCase(p)
def test_blocking_assignment(self):
    print(self.check_pass("A=B").asXML())

@TestCase(p)
def test_nonblocking_assignment(self):
    print(self.check_pass("A <= 1").asXML())
    print(self.check_pass("A <=1").asXML())


if __name__=='__main__':
    unittest.main()

