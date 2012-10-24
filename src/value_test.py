# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase
import grammar

@TestCase(grammar)
def test_non_zero_unsigned_number(self):
    self.check_pass("1")
    self.check_pass(" 1")
    self.check_pass("1 ")
    self.check_pass("120")
    self.check_fail("120 345")
    self.check_fail("0")

@TestCase(grammar)
def test_unsigned_number(self):
    self.check_fail("-1")
    self.check_pass("0")
    self.check_pass("000")
    self.check_pass("00012")
    self.check_pass("00012_800")
    self.check_pass("12345678_9")
    self.check_fail("12345678_9a0")
    self.check_fail("12345678 1")
    self.check_pass("12345678_1")
    self.check_pass("0_0_0")
    self.check_fail("0_0_0 1")

@TestCase(grammar)
def test_binary_value(self):
    self.check_pass("0")
    self.check_pass("0_1")
    self.check_pass("x")
    self.check_pass("ZX_?")
    self.check_pass("00_1?_x")
    self.check_fail("0 ?")
    self.check_fail("_?")
    self.check_pass("0_1_x_z_?")
    self.check_fail("0_1_x_z_!")
    self.check_pass("?_0")

@TestCase(grammar)
def test_octal_value(self):
    self.check_pass("0")
    self.check_pass("0_1")
    self.check_pass("x")
    self.check_pass("ZX_?")
    self.check_pass("00_1?_x")
    self.check_fail("0 ?")
    self.check_fail("_?")
    self.check_pass("0_1_x_z_?")
    self.check_fail("0_1_x_z_!")
    self.check_pass("?_0")
    self.check_pass("0")
    self.check_pass("0_")
    self.check_pass("x1X_??")
    self.check_fail("086")
    self.check_fail("a")
    self.check_fail("f")
    self.check_fail("g")
    self.check_pass("1x")
    self.check_pass("z1234567_0x_?")
    self.check_fail("z1234567_08x?")

@TestCase(grammar)
def test_hex_value(self):
    self.check_pass("0")
    self.check_pass("0_1")
    self.check_pass("x")
    self.check_pass("ZX_?")
    self.check_pass("00_1?_x")
    self.check_fail("0 ?")
    self.check_fail("_?")
    self.check_pass("0_1_x_z_?")
    self.check_fail("0_1_x_z_!")
    self.check_pass("?_0")
    self.check_pass("0")
    self.check_pass("0_")
    self.check_pass("x1X_??")
    self.check_pass("086")
    self.check_pass("a")
    self.check_pass("f")
    self.check_fail("g")
    self.check_pass("1x")
    self.check_pass("z1234567_0x_?")
    self.check_pass("z1234567_08x?")
    

@TestCase(grammar)
def test_decimal_base(self):
    self.check_pass("'sd")
    self.check_pass("'d")
    self.check_fail("'Ds")
    self.check_fail("'S")
    self.check_fail("d")
    self.check_fail("' d")
    self.check_fail("'b")

@TestCase(grammar)
def test_binary_base(self):
    self.check_pass("'sb")
    self.check_pass("'b")
    self.check_fail("'Bs")
    self.check_fail("'S")
    self.check_pass("'B")
    self.check_fail("b")
    self.check_fail("' b")
    self.check_fail("'h")

@TestCase(grammar)
def test_octal_base(self):
    self.check_pass("'so")
    self.check_pass("'o")
    self.check_fail("'Os")
    self.check_fail("'S")
    self.check_fail("o")
    self.check_fail("' o")
    self.check_fail("'h")
    self.check_pass("'O")

@TestCase(grammar)
def test_hex_base(self):
    self.check_pass("'sh")
    self.check_pass("'h")
    self.check_fail("'Hs")
    self.check_fail("'S")
    self.check_fail("h")
    self.check_fail("' h")
    self.check_fail("'b")
    self.check_pass("'H")


@TestCase(grammar)
def test_decimal_number(self):
    self.check_pass("123")
    self.check_pass("01")
    self.check_pass("'d0")
    print(self.check_pass("5'd0").asXML())
    self.check_pass("5'dx")
    self.check_pass("5'dZ")
    self.check_pass("5'd?")
    self.check_pass("5'd?__")
    self.check_fail("5'dXX")
    self.check_pass("'dX___")
    self.check_pass("'d?___")
    self.check_fail("'d?___0")
    self.check_fail("1'd")
    self.check_pass("1'd1")
    self.check_fail("0'd1")
    self.check_fail("1'd1x")
    print(self.check_pass("1'd5").asXML())
    print(self.check_pass("10'dx").asXML())
    print(self.check_pass("1'd?").asXML())
    print(self.check_pass("20").asXML())

@TestCase(grammar)
def test_binary_number(self):
    self.check_pass("4'b0000")
    self.check_pass("4'SB0?00")
    self.check_pass("8'Sbzzzz_xxxx")
    self.check_pass("'b0000")
    self.check_fail("'b00 00 ")
    self.check_pass("'b 0000 ")
    self.check_pass(" 32 'b 0000 ")
    self.check_fail(" 3 2 'b 0000 ")
    print(self.check_pass("'b0000").asXML())
    print(self.check_pass("'b1000").asXML())
    print(self.check_pass("8'B11").asXML())
    print(self.check_pass("8'b110x0").asXML())
    print(self.check_pass("40'b1??Zx0z011?1").asXML())

@TestCase(grammar)
def test_octal_number(self):
    print(self.check_pass("'o0000").asXML())
    print(self.check_pass("'o01234567").asXML())
    print(self.check_pass("8'o77").asXML())
    print(self.check_pass("8'o110x0").asXML())
    print(self.check_pass("40'o1??Zx0z011?1").asXML())


@TestCase(grammar)
def test_hex_number(self):
    print(self.check_pass("'h0000").asXML())
    print(self.check_pass("'h0123456789abcdef").asXML())
    print(self.check_pass("8'h77").asXML())
    print(self.check_pass("8'hF1Fx0").asXML())
    print(self.check_pass("40'h1??Zx0z011?1").asXML())

@TestCase(grammar)
def test_real_number(self):
    self.check_pass("1.0e+1")
    self.check_pass("23.5")
    self.check_pass("0.0E-30")
    self.check_pass("0.0")
    self.check_pass("0.12345")
    self.check_pass("1.0e-0")
    self.check_pass("1.0e+0")
    self.check_fail("-0.0")
    

if __name__=='__main__':
    unittest.main()

