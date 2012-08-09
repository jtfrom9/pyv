import parser as p
import pyparsing as pp
from test_common import *


test(p.non_zero_decimal_digit.leaveWhitespace(), "1")
test(p.non_zero_decimal_digit.leaveWhitespace(), "1 2")
test(p.non_zero_decimal_digit.leaveWhitespace(), "12")
test(p.non_zero_decimal_digit, "1 2")

test(p.non_zero_unsigned_number,"1")
test(p.non_zero_unsigned_number," 1")
test(p.non_zero_unsigned_number,"1 ")
test(p.non_zero_unsigned_number,"120")
test(p.non_zero_unsigned_number,"120 345")

test(p.unsigned_number,"-1")
test(p.unsigned_number,"0")
test(p.unsigned_number,"000")
test(p.unsigned_number,"00012")
test(p.unsigned_number,"00012_800")
test(p.unsigned_number,"12345678_9")
test(p.unsigned_number,"12345678_9a0")
test(p.unsigned_number,"12345678 1")

test(p.binary_value,"0")
test(p.binary_value,"0_1")
test(p.binary_value,"x")
test(p.binary_value,"ZX_?")
test(p.binary_value,"00_1?_x")
test(p.binary_value,"0 ?")
test(p.binary_value,"_?")

test(p.octal_value,"0")
test(p.octal_value,"0_")
test(p.octal_value,"x1X_??")
test(p.octal_value,"086")

test(p.decimal_base,"'sd")
test(p.decimal_base,"'d")
test(p.decimal_base,"'Ds")
test(p.decimal_base,"'S")
test(p.decimal_base,"d")
test(p.decimal_base,"' d")

test(p.decimal_number,"123")
test(p.decimal_number,"01")
test(p.decimal_number,"'d0")
test(p.decimal_number,"5'd0")

test(p.decimal_number,"5'dx")
test(p.decimal_number,"5'dZ")
test(p.decimal_number,"5'd?")
test(p.decimal_number,"5'd?__")
test(p.decimal_number,"5'dXX")
test(p.decimal_number,"'dX___")
test(p.decimal_number,"'d?___")


test(p.binary_number,"4'b0000")
test(p.binary_number,"4'SB0?00")
test(p.binary_number,"8'Sbzzzz_xxxx")
test(p.binary_number,"'b0000")
test(p.binary_number,"'b00 00 ")
test(p.binary_number,"'b 0000 ")
test(p.binary_number," 32 'b 0000 ")
test(p.binary_number," 3 2 'b 0000 ")

test(p.real_number,"1.0e+1")
test(p.real_number,"23.5")
test(p.real_number,"0.0E-30")

