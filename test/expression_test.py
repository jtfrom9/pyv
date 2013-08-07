# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    print_result, print_result_as_stmt, run_tests, debug, grammar )

@testOf(grammar.constant_function_call)
def test112(self):
    print_result(self.try_parse_pass("foo(0,1,2)"))
    print_result(self.try_parse_fail("foo(0,)"))
    print_result(self.try_parse_pass("foo(bar(0))"))
    print_result(self.try_parse_pass("foo(-10)"))
    print_result(self.try_parse_pass("foo( -bar(0) )"))
    print_result(self.try_parse_fail("foo( X+1 )"))
    print_result(self.try_parse_fail("A.b.c( 0)"))

@testOf(grammar.function_call)
def test113(self):
    print_result(self.try_parse_pass("foo()"))
    print_result(self.try_parse_pass("foo(0)"))
    print_result(self.try_parse_pass("foo(0,1,2)"))
    print_result(self.try_parse_pass("foo(bar(0))"))
    print_result(self.try_parse_pass("foo(-10)"))
    print_result(self.try_parse_pass("foo( -bar(0) )"))
    print_result(self.try_parse_pass("foo( X+1 )"))
    print_result(self.try_parse_pass("A.b.c( 0, 1, 2)"))
    print_result(self.try_parse_pass("A.b.c( X+1, -Z+1 )"))
    print_result(self.try_parse_pass("A.b.c( foo(0) )"))

@testOf(grammar.system_function_call)
def test114(self):
    print_result(self.try_parse_pass("$foo(0,1,2)"))
    print_result(self.try_parse_pass("$foo(bar(0))"))
    print_result(self.try_parse_pass("$foo(-10)"))
    print_result(self.try_parse_pass("$foo( -bar(0) )"))
    print_result(self.try_parse_pass("$foo( X+1 )"))
    print_result(self.try_parse_fail("$A.b.c( X+1, -Z+1 )"))

@testOf(grammar.conditional_expression)
def test116(self):
    print_result(self.try_parse_pass(" 0 ? 1 : 2"))
    print_result(self.try_parse_pass(" A ? 1 : 2"))
    print_result(self.try_parse_pass(" A+1 ? (X<0) : (Y==1)"))
    print_result(self.try_parse_pass(" A+1 ? X<0 : Y==1"))
    print_result(self.try_parse_pass(" 0?1:2 ? X<0 : Y==1"))
    print_result(self.try_parse_pass(" 0 ? 1 ? 2 : 3 : 4"))
    print_result(self.try_parse_pass(" 0 ? (1 ? 2 : 3) : 4"))
    print_result(self.try_parse_pass(" 0 ? (a() ? 2 : 3) : 4"))
    print_result(self.try_parse_pass(" 0 ? 1 : (a() ? 2 : 3)"))
    print_result(self.try_parse_pass(" 0 ? 1 : (a() ? b() : 3)"))
    print_result(self.try_parse_pass(" 0 ? (a() ? a() : 3) : 4"))
    print_result(self.try_parse_pass(" 1 ? ( a() ? a() : a() ) : 3"))


@testOf(grammar.constant_base_expression)
def test117(self):
    print_result(self.try_parse_pass("1"))
    print_result(self.try_parse_pass("1+2"))
    print_result(self.try_parse_fail("X+2"))
    print_result(self.try_parse_pass("0?1:2"))

@testOf(grammar.constant_expression)
def test118(self):
    print_result(self.try_parse_fail("A"))
    print_result(self.try_parse_pass("1"))
    print_result(self.try_parse_pass("(1)"))
    print_result(self.try_parse_pass("func(1)"))
    print_result(self.try_parse_pass("func()"))
    print_result(self.try_parse_pass("1 + 2"))
    print_result(self.try_parse_pass("1 + (2 * 3)"))
    print_result(self.try_parse_pass("(1 + 2) * 3"))
    print_result(self.try_parse_pass("0 ? 1 : 2"))
    print_result(self.try_parse_pass("IsOK() ? 1 : 2"))
    print_result(self.try_parse_pass("-0 ? 1 : 2"))
    #debug(grammar.constant_expression)
    print_result(self.try_parse_pass(" 1 ? ( a() ? a() : a() ): 3"))
    print_result(self.try_parse_pass(" 1 ?  a() ? a() : a() : 3"))
    print_result(self.try_parse_pass("1 + 2 * 3"))

@testOf(grammar.constant_mintypmax_expression)
def test119(self):
    print_result(self.try_parse_fail("A"))
    print_result(self.try_parse_pass("1"))
    print_result(self.try_parse_pass("(1)"))
    print_result(self.try_parse_pass("func(1)"))
    print_result(self.try_parse_pass("func()"))
    print_result(self.try_parse_pass("1 + 2"))
    print_result(self.try_parse_pass("1 + 2 * 3"))
    print_result(self.try_parse_pass("1 + (2 * 3)"))
    print_result(self.try_parse_pass("(1 + 2) * 3"))
    print_result(self.try_parse_pass("0 ? 1 : 2"))
    print_result(self.try_parse_pass("IsOK() ? 1 : 2"))
    print_result(self.try_parse_pass("-0 ? 1 : 2"))


@testOf(grammar.constant_range_expression)
def test120(self):
    print_result(self.try_parse_pass("1:0"))
    print_result(self.try_parse_pass("1:0+10"))
    print_result(self.try_parse_fail("1:X"))
    print_result(self.try_parse_pass("func(0):{1,2}"))

@testOf(grammar.dimension_constant_expression)
def test121(self):
    print_result(self.try_parse_fail("A"))
    print_result(self.try_parse_pass("1"))
    print_result(self.try_parse_pass("(1)"))
    print_result(self.try_parse_pass("func(1)"))
    print_result(self.try_parse_pass("func()"))
    print_result(self.try_parse_pass("1 + 2"))
    print_result(self.try_parse_pass("1 + 2 * 3"))
    print_result(self.try_parse_pass("1 + (2 * 3)"))
    print_result(self.try_parse_pass("(1 + 2) * 3"))
    print_result(self.try_parse_pass("0 ? 1 : 2"))
    print_result(self.try_parse_pass("IsOK() ? 1 : 2"))
    print_result(self.try_parse_pass("-0 ? 1 : 2"))
    print_result(self.try_parse_pass(" 1 ? ( a() ? a() : a() ): 3"))
    print_result(self.try_parse_pass(" 1 ?  a() ? a() : a() : 3"))

@testOf(grammar.expression)
def test122(self):
    #debug(grammar.expression)
    print_result(self.try_parse_pass("0"))
    print_result(self.try_parse_pass("A+10"))
    print_result(self.try_parse_pass("-X"))
    print_result(self.try_parse_pass("1+2+3"))
    print_result(self.try_parse_pass("-X+1"))
    print_result(self.try_parse_pass("-X+1/A"))
    print_result(self.try_parse_pass("1+2*3"))
    print_result(self.try_parse_pass("1-2*3+4/5"))
    print_result(self.try_parse_pass("1-(2*3+4)/5"))
    print_result(self.try_parse_pass("-X+1*A"))
    print_result(self.try_parse_pass("1?2:3"))
    print_result(self.try_parse_pass("-1?2:3"))
    print_result(self.try_parse_pass("A ? B : C"))
    print_result(self.try_parse_pass("A ? B : C ? D : E"))
    print_result(self.try_parse_pass("A ? B ? C : D : E"))
    print_result(self.try_parse_pass("A ? (B ? C : D) : E"))

    print_result(self.try_parse_pass("0 ? 1 : 2 ? 1 : 2"))
    print_result(self.try_parse_pass("0 ? 0 ? 1 : 2 : 2"))
    print_result(self.try_parse_pass("(0 ? 1 : 2) ? 3 : 4"))

    print_result(self.try_parse_pass("func(1)"))
    print_result(self.try_parse_pass("a + (b * c)"))
    print_result(self.try_parse_pass("(a + b) * c"))
    print_result(self.try_parse_pass("-1 + (b * c)"))
    print_result(self.try_parse_pass("-1 + (-b * ^c)"))
    print_result(self.try_parse_pass(" 1 ? ( a() ? a() : a() ): 3"))
    print_result(self.try_parse_pass(" 1 ?  a() ? a() : a() : 3"))

    print_result(self.try_parse_pass("1 + 2 * 3"))
    print_result(self.try_parse_pass("1 + 2 * 3 / 4 ** 5"))
    print_result(self.try_parse_pass("1 + 2 ? 3 : 4 * 5"))
    print_result(self.try_parse_pass("1 + (2 ? 3 : 4) * 5"))


@testOf(grammar.event_expression)
def test87(self):
    # debug(grammar.event_expression)
    # debug(grammar.expression)
    # print_result_as_stmt(self.try_parse_pass("~en"))
    # print_result_as_stmt(self.try_parse_pass("posedge A or negedge CLK"))
    # print_result_as_stmt(self.try_parse_pass("posedge A , negedge CLK"))
    # print_result_as_stmt(self.try_parse_pass("~en or posedge A or negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("~en or posedge A , negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("~en or posedge A or negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("(~en or posedge A  )or negedge CLK"))
    print_result_as_stmt(self.try_parse_pass("~en or (posedge A or negedge CLK)"))  # must be pass! not implemented recursive Binary Exp print
    print_result_as_stmt(self.try_parse_pass("~en ,posedge A or negedge CLK"))

@testOf(grammar.lsb_constant_expression)
def test123(self):
    print_result(self.try_parse_fail("1:0"))
    print_result(self.try_parse_pass("20"))
    print_result(self.try_parse_fail("X"))


@testOf(grammar.mintypmax_expression)
def test124(self):
    print_result(self.try_parse_pass("0"))
    print_result(self.try_parse_pass("A+10"))
    print_result(self.try_parse_pass("-X"))
    print_result(self.try_parse_pass("1+2+3"))
    print_result(self.try_parse_pass("-X+1"))
    print_result(self.try_parse_pass("-X+1+A"))
    print_result(self.try_parse_pass("-X+1*A"))
    print_result(self.try_parse_pass("1?2:3"))
    print_result(self.try_parse_pass("-1?2:3"))
    print_result(self.try_parse_pass("A ? B : C"))
    print_result(self.try_parse_pass("A ? B : A ? B : C"))
    print_result(self.try_parse_pass("0 ? 1 : 2 ? 1 : 2"))
    print_result(self.try_parse_pass("0 ? 0 ? 1 : 2 : 2"))
    print_result(self.try_parse_pass("(0 ? 1 : 2) ? 3 : 4"))
    print_result(self.try_parse_pass("func(1)"))


@testOfSkipped(grammar.module_path_conditional_expression)
def test125(self):
    pass


@testOfSkipped(grammar.module_path_expression)
def test126(self):
    pass


@testOfSkipped(grammar.module_path_mintypmax_expression)
def test127(self):
    pass


@testOf(grammar.msb_constant_expression)
def test128(self):
    print_result(self.try_parse_fail("1:0"))
    print_result(self.try_parse_pass("20"))


@testOf(grammar.range_expression)
def test129(self):
    print_result(self.try_parse_pass("1+2+3"))
    print_result(self.try_parse_pass("1:0"))
    print_result(self.try_parse_fail("1+:0"))

@testOfSkipped(grammar.width_constant_expression)
def test130(self):
    pass

if __name__=='__main__':
    run_tests()
    #run_tests(["test112"])
    #run_tests(["test114", "test113"])
    #run_tests(["test118"])
    #run_tests(["test122"])
    #run_tests(["test116"])

