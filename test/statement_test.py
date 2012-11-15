# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import testOf, _print, _stmt_print, run_tests, debug, fail, grammar, ast

@testOf(grammar.conditional_statement)
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


@testOf(grammar.continuous_assign)
def test65(self):
    #debug(grammar.continuous_assign)
    _stmt_print(self.check_pass("assign a=1"))
    _stmt_print(self.check_pass("assign a=1,b=2"))

@testOf(grammar.list_of_net_assignment)
def test66(self):
    _stmt_print(self.check_pass("a=1"))
    _stmt_print(self.check_pass("a=1,b=2"))

@testOf(grammar.net_assignment)
def test67(self):
   _stmt_print(self.check_pass("a=1"))

@testOf(grammar.initial_construct)
def test68(self):
    _stmt_print(self.check_pass("initial a=1;"))

@testOf(grammar.always_construct)
def test69(self):
    _stmt_print(self.check_pass("always a=1;"))
    _stmt_print(self.check_pass("always begin a=1; b=2; end"))

@testOf(grammar.blocking_assignment)
def test70(self):
    _stmt_print(self.check_pass("a=1"))


@testOf(grammar.nonblocking_assignment)
def test71(self):
    _stmt_print(self.check_pass("a<=1"))


@testOf(grammar.procedural_continuous_assignments)
def test72(self):
    _stmt_print(self.check_pass("deassign A"))
    _stmt_print(self.check_pass("assign A=1"))
    _stmt_print(self.check_pass("force A=1"))
    _stmt_print(self.check_pass("release A"))

@testOf(grammar.function_blocking_assignment)
def test73(self):
    _stmt_print(self.check_pass("A = 1"))
    _stmt_print(self.check_pass("A = foo(0,1)"))

@testOf(grammar.variable_assignment)
def test76(self):
    _stmt_print(self.check_pass("A = 1"))
    _stmt_print(self.check_pass("A = foo(0,1)"))

@testOf(grammar.function_seq_block)
def test75(self):
    _stmt_print(self.check_pass("""begin 
end
"""))
    _stmt_print(self.check_pass("""begin  a=1; end"""))
    _stmt_print(self.check_pass("""begin  a=1; b=2; c=func(x); end"""))
    _stmt_print(self.check_pass("""
begin 
 a=1; 
 b=2; 
 c=func(x); 
 begin 
   d = 10'd5;
   e = x.abc[0];
 end
end"""))

@testOf(grammar.seq_block)
def test77(self):
    # debug(grammar.seq_block)
    # debug(grammar.statement)
    # debug(grammar.blocking_assignment)
    _stmt_print(self.check_pass("""begin end"""))
    _stmt_print(self.check_pass("""begin a=1; end"""))
    _stmt_print(self.check_pass("""begin a=1; b=2; end"""))
    _stmt_print(self.check_pass("""begin 
a = foo(); 
b <= a[3];
begin
  c <= 0;
end
end"""))
    _stmt_print(self.check_pass("""
begin 
 a=1; 
 b=2; 
 c=func(x); 
 begin 
   d <= 10'd5;
   e <= x.abc[0];
   f <= { 0, 1, 2 };
 end
end"""))


@testOf(grammar.par_block)
def test78(self):
    _stmt_print(self.check_pass("""fork
join
"""))


@testOf(grammar.statement)
def test79(self):
    _stmt_print(self.check_pass("a<=1;"))
    _stmt_print(self.check_pass("a=1;"))
    _stmt_print(self.check_pass("""begin a=1; end"""))
    _stmt_print(self.check_fail("a<=1"))
    _stmt_print(self.check_fail("a=1"))
    _stmt_print(self.check_pass("assign x = 1;"))
    _stmt_print(self.check_pass("""begin 
force x= y + 1;
deassign x;
release x;
end """))

@testOf(grammar.function_statement)
def test81(self):
    _stmt_print(self.check_fail("a<=1;"))
    _stmt_print(self.check_pass("a=1;"))


@testOf(grammar.function_statement_or_null)
def test74(self):
    _stmt_print(self.check_pass(";"))
    _stmt_print(self.check_pass("A=1;"))

@testOf(grammar.statement_or_null)
def test80(self):
    _stmt_print(self.check_pass(";"))
    _stmt_print(self.check_pass("A=1;"))


@testOf(grammar.delay_control)
def test82(self):
    _print(self.check_pass("#10"))
    _print(self.check_pass("#X+1"))
    _print(self.check_pass("#(X+1)"))
    _print(self.check_pass("#X +1"))

@testOf(grammar.delay_or_event_control)
def test83(self):
    _stmt_print(self.check_pass("@A"))
    _stmt_print(self.check_pass("#A"))

@testOf(grammar.disable_statement)
def test84(self):
    pass

@testOf(grammar.delay_value)
def _test(self):
    debug(grammar.delay_value)
    _print(self.check_pass("10"))
    _print(self.check_pass("X+2"))

@testOf(grammar.event_control)
def test85(self):
    _stmt_print(self.check_pass("@A"))
    _stmt_print(self.check_pass("@( hoge )"))
    _stmt_print(self.check_pass("@*"))
    _stmt_print(self.check_pass("@(*)"))
    _stmt_print(self.check_pass("@( posedge CLK or ~RESET )"))

@testOf(grammar.event_trigger)
def test86(self):
    _stmt_print(self.check_pass("->A;"))


@testOf(grammar.event_expression)
def test87(self):
    _stmt_print(self.check_pass("~en"))
    _stmt_print(self.check_pass("posedge A or negedge CLK"))
    _stmt_print(self.check_pass("posedge A , negedge CLK"))
    _stmt_print(self.check_pass("~en or posedge A or negedge CLK"))
    _stmt_print(self.check_pass("~en , posedge A or negedge CLK"))  # must be pass! not implemented recursive Binary Exp print
    _stmt_print(self.check_pass("~en ,posedge A or negedge CLK"))

@testOf(grammar.procedural_timing_control_statement)
def test88(self):
    _stmt_print(self.check_pass("#10 A<=1;"))
    _stmt_print(self.check_pass("@clk A=1;"))
    _stmt_print(self.check_pass("#X+2 A=1;"))
    _stmt_print(self.check_pass("@(posedge clk or negedge reset) A=1;"))
    _stmt_print(self.check_pass("""@(posedge clk or negedge reset) begin 
 A<=1;
 B<=func(A,B);
end
"""))


@testOf(grammar.wait_statement)
def test89(self):
    _stmt_print(self.check_pass("wait (X) A=1;"))
    _stmt_print(self.check_pass("wait (X) ;"))


@testOf(grammar.conditional_statement)
def test90(self):
    # debug(grammar.conditional_statement)
    # debug(grammar.if_else_if_statement)
    # debug(grammar.expression)
    # debug(grammar.function_call)
    # debug(grammar.statement_or_null)
    _stmt_print(self.check_pass("""
 if (X > 0)  ;
 """))
    _stmt_print(self.check_pass("""
 if (X > 0)  A = B;
 """))
    _stmt_print(self.check_pass("""
 if (X > 0) a = foo(); 
 """))
    _stmt_print(self.check_pass("""
 if (X > 0) a = foo(); else b = 1;
 """))
    _stmt_print(self.check_pass("""
 if (X > 3) a = 1;
 else if (X > 2) a = 2;
 else a = 3;
 """))
    _stmt_print(self.check_pass("""
 if (X > 3) begin a = 1; end
 """))
    _stmt_print(self.check_pass("""
 if (X > 3) begin a = 1; end
 else begin b = 2; end
 """))
    _stmt_print(self.check_pass("""
 if (X > 3) begin a = 1; end
 else begin 
    b = 2; 
    if ( a==0 ) x = 1;
 end
 """))
 #    _stmt_print(self.check_pass("""
 # if (X > 3) a = 1;
 # else begin
 #    if (X > 2) begin 
 #       a = 2;
 #    end else begin
 #       X = 1;
 #       Y = 1;
 #    end
 # else a = 3;
 # """))


@testOf(grammar.if_else_if_statement)
def test91(self):
    debug(grammar.conditional_statement)
    debug(grammar.if_else_if_statement)



@testOf(grammar.function_conditional_statement)
def test92(self):
    pass


@testOf(grammar.function_if_else_if_statement)
def test93(self):
    pass


@testOf(grammar.case_statement)
def test94(self):
    pass


@testOf(grammar.case_item)
def test95(self):
    pass


@testOf(grammar.function_case_statement)
def test96(self):
    pass


@testOf(grammar.function_case_item)
def test97(self):
    pass


@testOf(grammar.function_loop_statement)
def test98(self):
    pass


@testOf(grammar.loop_statement)
def test99(self):
    pass


@testOf(grammar.system_task_enable)
def test100(self):
    pass


@testOf(grammar.task_enable)
def test101(self):
    pass

if __name__=='__main__':
    run_tests()

