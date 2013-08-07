# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    _print, run_tests,debug, grammar )

@testOf(grammar.number)
def test(self):
    _print(self.check_pass("23.5"))
    _print(self.check_pass("1.0e+1"))
    _print(self.check_pass("0.0E-30"))
    _print(self.check_pass("0.0"))
    _print(self.check_pass("123"))
    _print(self.check_pass("01"))
    _print(self.check_pass("'d0"))
    _print(self.check_pass("5'd0"))

@testOf(grammar.real_number)
def test141(self):
    _print(self.check_pass("23.5"))

@testOf(grammar.exp)
def test142(self):
    _print(self.check_pass("e"))


@testOfSkipped(grammar.decimal_number)
def test143(self):
    pass


@testOfSkipped(grammar.binary_number)
def test144(self):
    pass


@testOfSkipped(grammar.octal_number)
def test145(self):
    pass


@testOfSkipped(grammar.hex_number)
def test146(self):
    pass


@testOfSkipped(grammar.sign)
def test147(self):
    pass


@testOfSkipped(grammar.size)
def test148(self):
    pass


@testOfSkipped(grammar.non_zero_unsigned_number)
def test149(self):
    pass


@testOf(grammar.unsigned_number)
def test150(self):
    _print(self.check_pass("1"))
    _print(self.check_pass("123"))


@testOfSkipped(grammar.binary_value)
def test151(self):
    pass


@testOfSkipped(grammar.octal_value)
def test152(self):
    pass


@testOfSkipped(grammar.hex_value)
def test153(self):
    pass


@testOfSkipped(grammar.decimal_base)
def test154(self):
    pass


@testOfSkipped(grammar.binary_base)
def test155(self):
    pass


@testOfSkipped(grammar.octal_base)
def test156(self):
    pass


@testOfSkipped(grammar.hex_base)
def test157(self):
    pass


@testOfSkipped(grammar.non_zero_decimal_digit)
def test158(self):
    pass


@testOfSkipped(grammar.decimal_digit)
def test159(self):
    pass


@testOfSkipped(grammar.binary_digit)
def test160(self):
    pass


@testOfSkipped(grammar.octal_digit)
def test161(self):
    pass


@testOfSkipped(grammar.hex_digit)
def test162(self):
    pass


@testOfSkipped(grammar.x_digit)
def test163(self):
    pass


@testOfSkipped(grammar.z_digit)
def test164(self):
    pass



if __name__=='__main__':
    run_tests()


