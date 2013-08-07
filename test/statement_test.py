# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    print_result, print_result_as_stmt, run_tests, debug, fail, 
    grammar, ast )

@testOf(grammar.conditional_statement)
def test(self):
    print_result(self.try_parse_pass("if(ABC < 0) ;"))
    print_result(self.try_parse_pass(" if ( ABC < 0) A=B;"))
    print_result(self.try_parse_pass('''
if ( -1 < X )
     A = 0;
else 
     A = 2;
''').asXML())
    print(self.try_parse_pass('''
if ( -1 < X )
     A = 0;
else  if ( 0 < X)
     A = 1;
else
     A = 2;
'''))
    print(self.try_parse_pass('''
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
    print_result_as_stmt(self.try_parse_pass("assign a=1"))
    print_result_as_stmt(self.try_parse_pass("assign a=1,b=2"))

@testOf(grammar.list_of_net_assignment)
def test66(self):
    print_result_as_stmt(self.try_parse_pass("a=1"))
    print_result_as_stmt(self.try_parse_pass("a=1,b=2"))

@testOf(grammar.net_assignment)
def test67(self):
   print_result_as_stmt(self.try_parse_pass("a=1"))

@testOf(grammar.initial_construct)
def test68(self):
    print_result_as_stmt(self.try_parse_pass("initial a=1;"))

@testOf(grammar.always_construct)
def test69(self):
    print_result_as_stmt(self.try_parse_pass("always a=1;"))
    print_result_as_stmt(self.try_parse_pass("always begin a=1; b=2; end"))

@testOf(grammar.blocking_assignment)
def test70(self):
    print_result_as_stmt(self.try_parse_pass("a=1"))


@testOf(grammar.nonblocking_assignment)
def test71(self):
    print_result_as_stmt(self.try_parse_pass("a<=1"))


@testOf(grammar.procedural_continuous_assignments)
def test72(self):
    print_result_as_stmt(self.try_parse_pass("deassign A"))
    print_result_as_stmt(self.try_parse_pass("assign A=1"))
    print_result_as_stmt(self.try_parse_pass("force A=1"))
    print_result_as_stmt(self.try_parse_pass("release A"))

@testOf(grammar.function_blocking_assignment)
def test73(self):
    print_result_as_stmt(self.try_parse_pass("A = 1"))
    print_result_as_stmt(self.try_parse_pass("A = foo(0,1)"))

@testOf(grammar.variable_assignment)
def test76(self):
    print_result_as_stmt(self.try_parse_pass("A = 1"))
    print_result_as_stmt(self.try_parse_pass("A = foo(0,1)"))

@testOf(grammar.function_seq_block)
def test75(self):
    print_result_as_stmt(self.try_parse_pass("""begin 
end
"""))
    print_result_as_stmt(self.try_parse_pass("""begin  a=1; end"""))
    print_result_as_stmt(self.try_parse_pass("""begin  a=1; b=2; c=func(x); end"""))
    print_result_as_stmt(self.try_parse_pass("""
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
    print_result_as_stmt(self.try_parse_pass("""begin end"""))
    print_result_as_stmt(self.try_parse_pass("""begin a=1; end"""))
    print_result_as_stmt(self.try_parse_pass("""begin a=1; b=2; end"""))
    print_result_as_stmt(self.try_parse_pass("""begin 
a = foo(); 
b <= a[3];
begin
  c <= 0;
end
end"""))
    print_result_as_stmt(self.try_parse_pass("""
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
    print_result_as_stmt(self.try_parse_pass("""fork
join
"""))


@testOf(grammar.statement)
def test79(self):
    print_result_as_stmt(self.try_parse_pass("e = x.abc[0];"))
    print_result_as_stmt(self.try_parse_pass("a<=1;"))
    print_result_as_stmt(self.try_parse_pass("a=1;"))
    print_result_as_stmt(self.try_parse_pass("""begin a=1; end"""))
    print_result_as_stmt(self.try_parse_fail("a<=1"))
    print_result_as_stmt(self.try_parse_fail("a=1"))
    print_result_as_stmt(self.try_parse_pass("assign x = 1;"))
    print_result_as_stmt(self.try_parse_pass("""begin 
force x= y + 1;
deassign x;
release x;
end """))

@testOf(grammar.function_statement)
def test81(self):
    print_result_as_stmt(self.try_parse_fail("a<=1;"))
    print_result_as_stmt(self.try_parse_pass("a=1;"))


@testOf(grammar.function_statement_or_null)
def test74(self):
    print_result_as_stmt(self.try_parse_pass(";"))
    print_result_as_stmt(self.try_parse_pass("A=1;"))

@testOf(grammar.statement_or_null)
def test80(self):
    print_result_as_stmt(self.try_parse_pass(";"))
    print_result_as_stmt(self.try_parse_pass("A=1;"))


@testOf(grammar.delay_control)
def test82(self):
    print_result(self.try_parse_pass("#10"))
    print_result(self.try_parse_pass("#X+1"))
    print_result(self.try_parse_pass("#(X+1)"))
    print_result(self.try_parse_pass("#X +1"))

@testOf(grammar.delay_or_event_control)
def test83(self):
    print_result_as_stmt(self.try_parse_pass("@A"))
    print_result_as_stmt(self.try_parse_pass("#A"))

@testOfSkipped(grammar.disable_statement)
def test84(self):
    pass

@testOf(grammar.delay_value)
def _test(self):
    #debug(grammar.delay_value)
    print_result(self.try_parse_pass("10"))
    print_result(self.try_parse_pass("X+2"))

@testOf(grammar.event_control)
def test85(self):
    print_result_as_stmt(self.try_parse_pass("@A"))
    print_result_as_stmt(self.try_parse_pass("@( hoge )"))
    print_result_as_stmt(self.try_parse_pass("@*"))
    print_result_as_stmt(self.try_parse_pass("@(*)"))
    print_result_as_stmt(self.try_parse_pass("@( posedge CLK or ~RESET )"))

@testOf(grammar.event_trigger)
def test86(self):
    print_result_as_stmt(self.try_parse_pass("->A;"))


@testOf(grammar.event_expression)
def test87(self):
    #debug(grammar.event_expression)
    print_result_as_stmt(self.try_parse_pass("~en"))
    print_result_as_stmt(self.try_parse_pass("posedge A or negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("posedge A , negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("~en or posedge A or negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("~en , (posedge A or negedge CLK)"))  # must be pass! not implemented recursive Binary Exp print
    print_result(self.try_parse_pass("~en ,posedge A or negedge CLK"))

@testOf(grammar.procedural_timing_control_statement)
def test88(self):
    print_result_as_stmt(self.try_parse_pass("#10 A<=1;"))
    print_result_as_stmt(self.try_parse_pass("@clk A=1;"))
    print_result_as_stmt(self.try_parse_pass("#X+2 A=1;"))
    print_result_as_stmt(self.try_parse_pass("@(posedge clk or negedge reset) A=1;"))
    print_result_as_stmt(self.try_parse_pass("""@(posedge clk or negedge reset) begin 
 A<=1;
 B<=func(A,B);
end
"""))


@testOf(grammar.wait_statement)
def test89(self):
    print_result_as_stmt(self.try_parse_pass("wait (X) A=1;"))
    print_result_as_stmt(self.try_parse_pass("wait (X) ;"))


@testOf(grammar.conditional_statement)
def test90(self):
    # debug(grammar.conditional_statement)
    # debug(grammar.if_else_if_statement)
    # debug(grammar.expression)
    # debug(grammar.function_call)
    # debug(grammar.statement_or_null)
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0)  ;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0)  A = B;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0) a = foo(); 
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0) a = foo(); else b = 1;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) a = 1;
 else if (X > 2) a = 2;
 else a = 3;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 else begin b = 2; end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 else begin 
    b = 2; 
    if ( a==0 ) x = 1;
 end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) a = 1;
 else begin
    if (X > 2) begin 
       a = 2;
    end else begin
       X = 1;
       Y = 1;
    end
 end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (A > 0) a = 1;
 else if (B > 0) begin
    b = 1;
 end else 
    c = 1;
 """))


@testOf(grammar.if_else_if_statement)
def test91(self):
    print_result_as_stmt(self.try_parse_fail("""if (A > 0) a = 1;
 else if (B > 0) b = 1;
 end else        f = 1;
 else if (C > 0) c = 1;
 else if (D > 0) d = 1;
 else if (E > 0) e = 1;
 """))
    print_result_as_stmt(self.try_parse_pass("""if (A > 0) a = 1;
 else if (B > 0) b = 1;
 else if (C > 0) c = 1;
 else if (D > 0) d = 1;
 else if (E > 0) e = 1;
 else        f = 1;
 """))
    

@testOf(grammar.function_conditional_statement)
def test92(self):
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0)  ;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0)  A = B;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0) a = foo(); 
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 0) a = foo(); else b = 1;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) a = 1;
 else if (X > 2) a = 2;
 else a = 3;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 else begin b = 2; end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) begin a = 1; end
 else begin 
    b = 2; 
    if ( a==0 ) x = 1;
 end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (X > 3) a = 1;
 else begin
    if (X > 2) begin 
       a = 2;
    end else begin
       X = 1;
       Y = 1;
    end
 end
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (A > 0) a = 1;
 else if (B > 0) begin
    b = 1;
 end else 
    c = 1;
 """))


@testOf(grammar.function_if_else_if_statement)
def test93(self):
    print_result_as_stmt(self.try_parse_fail("""
 if (A > 0) a = 1;
 else if (B > 0) b = 1;
 end else        f = 1;
 else if (C > 0) c = 1;
 else if (D > 0) d = 1;
 else if (E > 0) e = 1;
 """))
    print_result_as_stmt(self.try_parse_pass("""
 if (A > 0) a = 1;
 else if (B > 0) b = 1;
 else if (C > 0) c = 1;
 else if (D > 0) d = 1;
 else if (E > 0) e = 1;
 else        f = 1;
 """))


@testOf(grammar.case_statement)
def test94(self):
    print_result_as_stmt(self.try_parse_pass("""
case( 1 )
 X: x = 0;
 Y: y = 0;
endcase
"""))
    print_result_as_stmt(self.try_parse_pass("""
casex( 1 )
 X: x = 0;
 Y: y = 0;
endcase
"""))


@testOf(grammar.case_item)
def test95(self):
    print_result(self.try_parse_pass("A: a=1;"))
    print_result(self.try_parse_pass("A,B: a=1;"))
    print_result(self.try_parse_pass("default: a=1;"))
    

@testOfSkipped(grammar.function_case_statement)
def test96(self):
    pass


@testOfSkipped(grammar.function_case_item)
def test97(self):
    pass


@testOfSkipped(grammar.function_loop_statement)
def test98(self):
    pass


@testOf(grammar.loop_statement)
def test99(self):
    print_result_as_stmt(self.try_parse_pass("""
 for ( i=0; i<10; i=i+1) 
  count <= foo(i);
"""))
#     print_result_as_stmt(self.try_parse_pass("""
#  while( 1 ) begin
#    if (reset)
#      x = 0;
#   else begin
#     count <= foo(i);
#   end
#  end
# """))


@testOfSkipped(grammar.system_task_enable)
def test100(self):
    pass


@testOfSkipped(grammar.task_enable)
def test101(self):
    pass

if __name__=='__main__':
    run_tests()

