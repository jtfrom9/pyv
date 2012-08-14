# -*- coding: utf-8 -*-
import pyparsing as pp
import parser as p
import sys

import unittest
from test_common import GrammarTestCase, TestCase

class TestModule(unittest.TestCase):
    def do_test(self, text):
        result = (p.source_text + pp.stringEnd).parseString(text)
        print(result.asXML())
        
    def test1(self):
        text = '''
module hoge(a,b,c);
endmodule
'''
        self.do_test(text)

    def test2(self):
        text = '''
module hoge(a,b,c);

input [1:0] a;
inout [10:0] b;
output [3:4] c;

reg [3:4] c;
endmodule
'''
        self.do_test(text)
        
    def test3(self):
        text = '''
module add(
  input [1:0] a,
  inout [3:4] b,
  output [10:0] c);

   reg [3:0]     c;

   always@* begin
      c <= a + b;
   end
   
endmodule

'''
        self.do_test(text)


@TestCase(p)
def test_port_declaration(self):
    print(self.check_pass('''input [3:0]
a'''
                          ).asXML())


@TestCase(p)
def test_list_of_port_declarations(self):
    print(self.check_pass('''(input [3:0] a, 
  output [10:4] b)'''
).asXML())
    print(self.check_pass('''(
    input [3:0] a,
    input [3:0] b,
    output [3:0] c)
''').asXML())


@TestCase(p)
def test_always_construct(self):
    print(self.check_pass('''always hoge=1+2;'''
).asXML())
    
@TestCase(p)
def test_procedural_timing_control_statement(self):
    print(self.check_pass("@hoge;").asXML())
    print(self.check_pass("@*;").asXML())
    
@TestCase(p)
def test_event_control(self):
    print(self.check_pass("@hoge").asXML())

    print(self.check_pass('''@hoge
''').asXML())
    print(self.check_pass("@*").asXML())

@TestCase(p)
def test_statement_or_null(self):
    print(self.check_pass(";").asXML())
    print(self.check_pass("hoge = 1 + 2;").asXML())

@TestCase(p)
def test_variable_lvalue(self):
    print(self.check_pass("hoge").asXML())
    
@TestCase(p)    
def test_blocking_assignment(self):
    print(self.check_pass("hoge = 1 + 2").asXML())

@TestCase(p)
def test_expression(self):
    print(self.check_pass("1").asXML())
    print(self.check_pass("+2").asXML())
    print(self.check_pass("1 + 2 ").asXML())
    print(self.check_pass("A-B").asXML())

if __name__=='__main__':
    unittest.main()

