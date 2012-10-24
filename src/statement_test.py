# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase, TestCase2, _print
import pyparsing as pp
import grammar

@TestCase2(grammar.conditional_statement)
def test(self):
    _print(self.check_pass("if(ABC < 0) ;"))
    _print(self.check_pass(" if ( ABC < 0) A=B;"))
    _print(self.check_pass('''
if ( -1 < X )
     A = 0;
else 
     A = 2;
''').asXML())
    print(self.check_pass('''
if ( -1 < X )
     A = 0;
else  if ( 0 < X)
     A = 1;
else
     A = 2;
'''))
    print(self.check_pass('''
if ( -1 < X )
     A = 0;
else  if ( 0 <= X)
     A = 1;
else  if ( 0 < X)
     A = 1;
else  if ( 0 < X)
     A = 1;
else  if ( 0 > X)
     A = 1;
else
     A = 2;
''').asXML())


@TestCase2(grammar.continuous_assign)
def test65(self):
    #_print(self.check_pass("assign a=1"))
    _print(self.check_pass("assign a=1,b=2"))
    # _print(self.check_pass("assign a=1,b=2"))
    # r = self.check_pass("assign a=1,b=2")
    # import ast
    # print(r)
    # print(r.continuous_assign)
    # print(ast.nodeInfo(r.continuous_assign))
    # print(ast.nodeInfo(r.continuous_assign[0]))
    # import pprint
    # pprint.pprint(r)

@TestCase2(grammar.list_of_net_assignment)
def test66(self):
   _print(self.check_pass("a=1"))
   _print(self.check_pass("a=1,b=2"))

@TestCase2(grammar.net_assignment)
def test67(self):
   _print(self.check_pass("a=1"))

@TestCase2(grammar.initial_construct)
def test68(self):
    pass


@TestCase2(grammar.always_construct)
def test69(self):
    pass


@TestCase2(grammar.blocking_assignment)
def test70(self):
    pass


@TestCase2(grammar.nonblocking_assignment)
def test71(self):
    pass


@TestCase2(grammar.procedural_continuous_assignments)
def test72(self):
    pass


@TestCase2(grammar.function_blocking_assignment)
def test73(self):
    pass


@TestCase2(grammar.function_statement_or_null)
def test74(self):
    pass


@TestCase2(grammar.function_seq_block)
def test75(self):
    pass


@TestCase2(grammar.variable_assignment)
def test76(self):
    pass


@TestCase2(grammar.par_block)
def test77(self):
    pass


@TestCase2(grammar.seq_block)
def test78(self):
    pass

@TestCase2(grammar.statement)
def test79(self):
    pass


@TestCase2(grammar.statement_or_null)
def test80(self):
    pass


@TestCase2(grammar.function_statement)
def test81(self):
    pass


@TestCase2(grammar.delay_control)
def test82(self):
    pass


@TestCase2(grammar.delay_or_event_control)
def test83(self):
    pass


@TestCase2(grammar.disable_statement)
def test84(self):
    pass


@TestCase2(grammar.event_control)
def test85(self):
    pass


@TestCase2(grammar.event_trigger)
def test86(self):
    pass


@TestCase2(grammar.event_expression)
def test87(self):
    pass


@TestCase2(grammar.procedural_timing_control_statement)
def test88(self):
    pass


@TestCase2(grammar.wait_statement)
def test89(self):
    pass


@TestCase2(grammar.conditional_statement)
def test90(self):
    pass


@TestCase2(grammar.if_else_if_statement)
def test91(self):
    pass


@TestCase2(grammar.function_conditional_statement)
def test92(self):
    pass


@TestCase2(grammar.function_if_else_if_statement)
def test93(self):
    pass


@TestCase2(grammar.case_statement)
def test94(self):
    pass


@TestCase2(grammar.case_item)
def test95(self):
    pass


@TestCase2(grammar.function_case_statement)
def test96(self):
    pass


@TestCase2(grammar.function_case_item)
def test97(self):
    pass


@TestCase2(grammar.function_loop_statement)
def test98(self):
    pass


@TestCase2(grammar.loop_statement)
def test99(self):
    pass


@TestCase2(grammar.system_task_enable)
def test100(self):
    pass


@TestCase2(grammar.task_enable)
def test101(self):
    pass

if __name__=='__main__':
    unittest.main()

    # g = pp.Group(
    #     grammar.IF + grammar.LP + grammar.expression + grammar.RP + grammar.statement_or_null("name") 
    #     ) + pp.stringEnd

    # def action():
    #     print("action")
    # g.setParseAction(action)

    # #result = g.parseString("if ;")
    # result = g.parseString("if (A <2) ;")

    # if result:
    #     print(result)
    # else:
    #     print("NG")

    g = pp.Group(grammar.statement_or_null("stmt") + pp.stringEnd)
    def action(t):
        print(t.stmt)
    g.setParseAction(action)
    r = g.parseString(";")
    print(r)

