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

bin=("0", "1", "x", "Z", "?", "z?")

for d in bin:
    test(p.binary_value,d)

