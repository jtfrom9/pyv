# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar
import action

@TestCase(grammar)
def test_simple_identifier(self):        
    print(self.check_pass("hoge").asXML())

@TestCase(grammar)
def test_identifier(self):        
    print(self.check_pass("hoge").asXML())

@TestCase(grammar)
def test_event_identifier(self):
    print(self.check_pass("hoge").asXML())
    
@TestCase(grammar)
def test_event_control(self):
    print(self.check_pass("@hoge").asXML())
    
@TestCase(grammar)
def test__range(self):
    print(self.check_pass("[10:5]").asXML())

@TestCase(grammar)
def test_simple_arrayed_identifier(self):        
    print(self.check_pass("hoge[10:5]").asXML())

@TestCase(grammar)
def test_arrayed_identifier(self):        
    print(self.check_pass("hoge[10:5]").asXML())
    print(self.check_pass("hoge_[1:0]").asXML())
    print(self.check_pass("hoge").asXML())

@TestCase(grammar)
def test_module_instance_identifier(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[2:3]").asXML())

@TestCase(grammar)
def test_module_instance_identifier(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[2:3]").asXML())

@TestCase(grammar)
def test_simple_hierarchical_identifier(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[0]").asXML())

@TestCase(grammar)
def test_simple_hierarchical_branch(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].foo[1]").asXML())
    print(self.check_pass("hoge[5].foo.bar").asXML())
    print(self.check_pass("hoge[5].foo.bar.A[10]").asXML())

@TestCase(grammar)
def test_simple_hierarchical_identifier(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())
    

@TestCase(grammar)
def test_hierarchical_identifier(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())
    

# import pyparsing as pp
# hoge = pp.Group( pp.ZeroOrMore( grammar.ID )("id_list") )
# class X(object):
#     pass
# x = X()
# x.hoge = hoge

# @action.Action(x.hoge)
# def action(s,loc,token):
#     print(token.id_list)
#     for id in token.id_list:
#         print(id)

# @TestCase(x)
# def test_hoge(self):
#     print(self.check_pass("A B C").asXML())


if __name__=='__main__':
    unittest.main()

