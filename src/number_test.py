# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _print
import grammar
import action

@TestCase2(grammar.number)
def test(self):
    _print(self.check_pass("23.5"))
    _print(self.check_pass("1.0e+1"))
    _print(self.check_pass("0.0E-30"))
    _print(self.check_pass("0.0"))
    _print(self.check_pass("123"))
    _print(self.check_pass("01"))
    _print(self.check_pass("'d0"))
    _print(self.check_pass("5'd0"))

@TestCase2(grammar.real_number)
def test141(self):
    pass


@TestCase2(grammar.exp)
def test142(self):
    _print(self.check_pass("e"))


@TestCase2(grammar.decimal_number)
def test143(self):
    pass


@TestCase2(grammar.binary_number)
def test144(self):
    pass


@TestCase2(grammar.octal_number)
def test145(self):
    pass


@TestCase2(grammar.hex_number)
def test146(self):
    pass


@TestCase2(grammar.sign)
def test147(self):
    pass


@TestCase2(grammar.size)
def test148(self):
    pass


@TestCase2(grammar.non_zero_unsigned_number)
def test149(self):
    pass


@TestCase2(grammar.unsigned_number)
def test150(self):
    _print(self.check_pass("1"))
    _print(self.check_pass("123"))


@TestCase2(grammar.binary_value)
def test151(self):
    pass


@TestCase2(grammar.octal_value)
def test152(self):
    pass


@TestCase2(grammar.hex_value)
def test153(self):
    pass


@TestCase2(grammar.decimal_base)
def test154(self):
    pass


@TestCase2(grammar.binary_base)
def test155(self):
    pass


@TestCase2(grammar.octal_base)
def test156(self):
    pass


@TestCase2(grammar.hex_base)
def test157(self):
    pass


@TestCase2(grammar.non_zero_decimal_digit)
def test158(self):
    pass


@TestCase2(grammar.decimal_digit)
def test159(self):
    pass


@TestCase2(grammar.binary_digit)
def test160(self):
    pass


@TestCase2(grammar.octal_digit)
def test161(self):
    pass


@TestCase2(grammar.hex_digit)
def test162(self):
    pass


@TestCase2(grammar.x_digit)
def test163(self):
    pass


@TestCase2(grammar.z_digit)
def test164(self):
    pass



if __name__=='__main__':
    unittest.main()

    # import pyparsing as pp
    # r = (grammar.number + grammar.number + pp.stringEnd).parseString("1.1 1.2")
    # print(dir(r))
    # print(r)


