# -*- coding: utf-8 -*-
import sys
import unittest
import pprint
from pyparsing import stringEnd

# from test_common import testOf
# import grammar
from test_common import testOf, grammar

@testOf(grammar.port_declaration)
def test_port_declaration(self):
    print(self.try_parse_pass('''input [3:0]
a'''
                          ).asXML())


@testOf(grammar.list_of_port_declarations)
def test_list_of_port_declarations(self):
    print(self.try_parse_pass('''(input [3:0] a, 
  output [10:4] b)'''
).asXML())
    print(self.try_parse_pass('''(
    input [3:0] a,
    input [3:0] b,
    output [3:0] c)
''').asXML())


@testOf(grammar.always_construct)
def test_always_construct(self):
    print(self.try_parse_pass('''always hoge=1+2;'''
).asXML())
    
# @testOf(grammar.procedural_timing_control_statement)
# def test_procedural_timing_control_statement(self):
#     print(self.try_parse_pass("@hoge;").asXML())
#     print(self.try_parse_pass("@*;").asXML())
    
@testOf(grammar.event_control)
def test_event_control(self):
    print(self.try_parse_pass("@hoge").asXML())

    print(self.try_parse_pass('''@hoge
''').asXML())
    print(self.try_parse_pass("@*").asXML())


if __name__=='__main__':
    unittest.main()

