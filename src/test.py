import parser as p
import pyparsing as pp
from test_common import *

def main():
    test(p.sign,"+")
    test(p.unary_operator, " + ")
    test(p.unary_operator, " ~& ")
    test(p.unary_operator, " ~~ ")
    test(p.binary_operator, "=== ")
    test(p.binary_operator, " !== ")
    test(p.binary_operator, " && ")

    test(p.non_zero_unsigned_number,"0")
    test(p.non_zero_unsigned_number,"1")
    test(p.non_zero_unsigned_number,"2")
    test(p.non_zero_unsigned_number,"33")
    test(p.non_zero_unsigned_number," 3")
    test(p.non_zero_unsigned_number,"123_000",True)
    test(p.non_zero_unsigned_number,"023_000",True)
    test(p.non_zero_unsigned_number,"0 23_000",True)

    test(p.unsigned_number, "1342_432_9080")
    test(p.unsigned_number, "012")
    test(p.unsigned_number, "0 12")

    test(p.number, "1")
    

    test(p.string, "\"\"")
    test(p.string, "\"foo-bar\"")
    test(p.string, "\" !#$%&'()=-^~\|[]{}@`:*/?\_,<.> 	\t \"")

file = '''
module hoge ( a,b, c, d  , e ); 
 wire a, b;
 reg X;
 reg [1:0] Y;
endmodule
'''
def old():
    try:
        print(number.parseString("1").asXML())
        #print((_range).parseString("[1:0]"))
        # result = (source_text + stringEnd).parseString(file)
        # print(result.asXML())
    except ParseException,pfe:
        print("line={0}".format(pfe.line))
        print("msg={0}".format(pfe.msg))
        print(pfe)
        print(pfe.line);
    except ParseSyntaxException,pfe:
        # for p in dir(pfe):
        #     print("Error: "+p)
        # print("col={0}".format(pfe.col))
        print("line={0}".format(pfe.line))
        # print("lineno={0}".format(pfe.lineno))
        # print("loc={0}".format(pfe.loc))
        #print("markInputLine={0}".format(pfe.markInputLine()))
        print("msg={0}".format(pfe.msg))
        #print(LastParseLoc)
        print(pfe)
        print(pfe.line);
        # import itertools
        # s=""
        # print(s.join(" " for i in range(len(pfe.line)-1)) + "^")
        #for s in itertools.repeat(" ",len(pfe.line)):


if __name__=='__main__':
    main()
