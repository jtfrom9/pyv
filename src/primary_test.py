# -*- coding: utf-8 -*-
import parser as p
import sys

import unittest
from test_common import GrammarTestCase, TestCase

@TestCase(p)
def test_primary(self):
    # print(self.check_pass("10").asXML())
    # print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge(a)").asXML())
    #self.check_pass("hoge(a)")

@TestCase(p)
def test_function_call(self):
    print(self.check_pass("hoge(a)").asXML())
    # result = self.check_pass("hoge(a)")
    # for p in dir(result):
    #     prop = getattr(result,p)
    #     #print(prop)
    #     print("prop={0}, value={1}".format(p,str(prop)))



if __name__=='__main__':
    unittest.main()

