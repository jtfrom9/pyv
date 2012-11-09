# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import testOf, _print, run_tests
import grammar


@testOf(grammar.constant_function_call)
def test112(self):
    _print(self.check_pass("foo(0,1,2)"))
    _print(self.check_fail("foo(0,)"))
    _print(self.check_pass("foo(bar(0))"))
    _print(self.check_pass("foo(-10)"))
    _print(self.check_pass("foo( -bar(0) )"))
    _print(self.check_fail("foo( X+1 )"))
    _print(self.check_fail("A.b.c( 0)"))

@testOf(grammar.function_call)
def test113(self):
    _print(self.check_pass("foo(0)"))
    _print(self.check_pass("foo(0,1,2)"))
    _print(self.check_pass("foo(bar(0))"))
    _print(self.check_pass("foo(-10)"))
    _print(self.check_pass("foo( -bar(0) )"))
    _print(self.check_pass("foo( X+1 )"))
    _print(self.check_pass("A.b.c( 0, 1, 2)"))
    _print(self.check_pass("A.b.c( X+1, -Z+1 )"))
    _print(self.check_pass("A.b.c( foo(0) )"))

@testOf(grammar.system_function_call)
def test114(self):
    _print(self.check_pass("$foo(0,1,2)"))
    _print(self.check_pass("$foo(bar(0))"))
    _print(self.check_pass("$foo(-10)"))
    _print(self.check_pass("$foo( -bar(0) )"))
    _print(self.check_pass("$foo( X+1 )"))
    _print(self.check_fail("$A.b.c( X+1, -Z+1 )"))

@testOf(grammar.conditional_expression)
def test116(self):
    _print(self.check_pass(" 0 ? 1 : 2"))
    _print(self.check_pass(" A ? 1 : 2"))
    _print(self.check_pass(" A+1 ? X<0 : Y==1"))
    _print(self.check_pass(" 0?1:2 ? X<0 : Y==1"))

@testOf(grammar.constant_base_expression)
def test117(self):
    _print(self.check_pass("1"))
    _print(self.check_pass("1+2"))
    _print(self.check_fail("X+2"))
    _print(self.check_pass("0?1:2"))

@testOf(grammar.constant_expression)
def test118(self):
    _print(self.check_fail("A"))
    _print(self.check_pass("1"))
    _print(self.check_pass("(1)"))
    _print(self.check_pass("func(1)"))
    _print(self.check_pass("func()"))
    _print(self.check_pass("1 + 2"))
    _print(self.check_pass("1 + 2 * 3"))
    _print(self.check_pass("1 + (2 * 3)"))
    _print(self.check_pass("(1 + 2) * 3"))
    _print(self.check_pass("0 ? 1 : 2"))
    _print(self.check_pass("IsOK() ? 1 : 2"))
    _print(self.check_pass("-0 ? 1 : 2"))
    _print(self.check_pass(" 1 ? ( a() ? a() : a() ): 3"))
    _print(self.check_pass(" 1 ?  a() ? a() : a() : 3"))

@testOf(grammar.constant_mintypmax_expression)
def test119(self):
    _print(self.check_fail("A"))
    _print(self.check_pass("1"))
    _print(self.check_pass("(1)"))
    _print(self.check_pass("func(1)"))
    _print(self.check_pass("func()"))
    _print(self.check_pass("1 + 2"))
    _print(self.check_pass("1 + 2 * 3"))
    _print(self.check_pass("1 + (2 * 3)"))
    _print(self.check_pass("(1 + 2) * 3"))
    _print(self.check_pass("0 ? 1 : 2"))
    _print(self.check_pass("IsOK() ? 1 : 2"))
    _print(self.check_pass("-0 ? 1 : 2"))


@testOf(grammar.constant_range_expression)
def test120(self):
    _print(self.check_pass("1:0"))
    _print(self.check_pass("1:0+10"))
    _print(self.check_fail("1:X"))
    _print(self.check_pass("func(0):{1,2}"))

@testOf(grammar.dimension_constant_expression)
def test121(self):
    _print(self.check_fail("A"))
    _print(self.check_pass("1"))
    _print(self.check_pass("(1)"))
    _print(self.check_pass("func(1)"))
    _print(self.check_pass("func()"))
    _print(self.check_pass("1 + 2"))
    _print(self.check_pass("1 + 2 * 3"))
    _print(self.check_pass("1 + (2 * 3)"))
    _print(self.check_pass("(1 + 2) * 3"))
    _print(self.check_pass("0 ? 1 : 2"))
    _print(self.check_pass("IsOK() ? 1 : 2"))
    _print(self.check_pass("-0 ? 1 : 2"))
    _print(self.check_pass(" 1 ? ( a() ? a() : a() ): 3"))
    _print(self.check_pass(" 1 ?  a() ? a() : a() : 3"))

@testOf(grammar.expression)
def test122(self):
    _print(self.check_pass("0"))
    _print(self.check_pass("A+10"))
    _print(self.check_pass("-X"))
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("-X+1"))
    _print(self.check_pass("-X+1+A"))
    _print(self.check_pass("-X+1*A"))
    _print(self.check_pass("1?2:3"))
    _print(self.check_pass("-1?2:3"))
    _print(self.check_pass("A ? B : C"))
    _print(self.check_pass("A ? B : A ? B : C"))
    _print(self.check_pass("0 ? 1 : 2 ? 1 : 2"))
    _print(self.check_pass("0 ? 0 ? 1 : 2 : 2"))
    _print(self.check_pass("(0 ? 1 : 2) ? 3 : 4"))
    _print(self.check_pass("func(1)"))

@testOf(grammar.lsb_constant_expression)
def test123(self):
    _print(self.check_fail("1:0"))
    _print(self.check_pass("20"))
    _print(self.check_fail("X"))


@testOf(grammar.mintypmax_expression)
def test124(self):
    _print(self.check_pass("0"))
    _print(self.check_pass("A+10"))
    _print(self.check_pass("-X"))
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("-X+1"))
    _print(self.check_pass("-X+1+A"))
    _print(self.check_pass("-X+1*A"))
    _print(self.check_pass("1?2:3"))
    _print(self.check_pass("-1?2:3"))
    _print(self.check_pass("A ? B : C"))
    _print(self.check_pass("A ? B : A ? B : C"))
    _print(self.check_pass("0 ? 1 : 2 ? 1 : 2"))
    _print(self.check_pass("0 ? 0 ? 1 : 2 : 2"))
    _print(self.check_pass("(0 ? 1 : 2) ? 3 : 4"))
    _print(self.check_pass("func(1)"))


@testOf(grammar.module_path_conditional_expression)
def test125(self):
    pass


@testOf(grammar.module_path_expression)
def test126(self):
    pass


@testOf(grammar.module_path_mintypmax_expression)
def test127(self):
    pass


@testOf(grammar.msb_constant_expression)
def test128(self):
    _print(self.check_fail("1:0"))
    _print(self.check_pass("20"))


@testOf(grammar.range_expression)
def test129(self):
    _print(self.check_pass("1+2+3"))
    _print(self.check_pass("1:0"))
    _print(self.check_fail("1+:0"))

@testOf(grammar.width_constant_expression)
def test130(self):
    pass

if __name__=='__main__':
    run_tests()
    #run_tests(["test112"])
    #run_tests(["test114", "test113"])
    #run_tests(["test118"])
    #run_tests(["test122"])
    #run_tests(["test116"])

