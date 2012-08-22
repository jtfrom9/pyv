# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2
import grammar
import action

@TestCase2(grammar.simple_identifier)
def test0(self):        
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.simple_arrayed_identifier)
def test1(self):        
    print(self.check_pass("hoge[10:5]").asXML())

@TestCase2(grammar.escaped_identifier)
def test2(self):
    pass

@TestCase2(grammar.escaped_arrayed_identifier)
def test3(self):
    pass

@TestCase2(grammar.identifier)
def test4(self):        
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.arrayed_identifier)
def test5(self):        
    print(self.check_pass("hoge[10:5]").asXML())
    print(self.check_pass("hoge_[1:0]").asXML())
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.event_identifier)
def test6(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.function_identifier)
def test62(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.module_identifier)
def test63(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.module_instance_identifier)
def test64(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.net_identifier)
def test65(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.port_identifier)
def test66(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.real_identifier)
def test66(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.real_identifier)
def test67(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.task_identifier)
def test68(self):
    print(self.check_pass("hoge").asXML())

@TestCase2(grammar.variable_identifier)
def test69(self):
    print(self.check_pass("hoge").asXML())

# @TestCase2(grammar)
# def test_event_control(self):
#     print(self.check_pass("@hoge").asXML())
    
# @TestCase2(grammar)
# def test__range(self):
#     print(self.check_pass("[10:5]").asXML())

@TestCase2(grammar.module_instance_identifier)
def test7(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[2:3]").asXML())

@TestCase2(grammar.module_instance_identifier)
def test8(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[2:3]").asXML())

@TestCase2(grammar.simple_hierarchical_identifier)
def test9(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[0]").asXML())

@TestCase2(grammar.simple_hierarchical_branch)
def test10(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].foo[1]").asXML())
    print(self.check_pass("hoge[5].foo.bar").asXML())
    print(self.check_pass("hoge[5].foo.bar.A[10]").asXML())

@TestCase2(grammar.simple_hierarchical_identifier)
def test11(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())
    
@TestCase2(grammar.hierarchical_identifier)
def test12(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())
    

if __name__=='__main__':
    unittest.main()

