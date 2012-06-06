# -*- coding: utf-8 -*-
from pyparsing import *
import sys
import collections
import pprint

RESERVED_KEYWORDS = ('module', 'endmodule')

ID = ~MatchFirst([Keyword(w) for w in RESERVED_KEYWORDS]) + Word(alphas, alphanums+'_')

#source_text << ZeroOrMore( Group(description) )("descriptions")
source_text << ZeroOrMore(description)("source_text")
description << Group( Group(module_declaration)("module") | ID("id").setParseAction(lambda t: "__id__") )("description")

# リテラルも事前にSuppress定義する
LP = Suppress("(")
RP = Suppress(")")
SM = Suppress(";")

# asXML()の出力がうまくいかなくなる


non_port_module_item = ID
list_of_port_declarations = LP + delimitedList(ID) + RP

# 非終端は基本的に全体をGroupで囲む
# 名前をつける(setResultsName)しても良いが、呼ばれる側で設定されていれば上書きされる
# 基本は名前を付ける
module_declaration = Group(\
    module + ID("modname") + Group(list_of_port_declarations)("params") + SM \
    + Group(ZeroOrMore(non_port_module_item))("body") \
    + endmodule)("module_declaration") \
    
# 他の非終端を呼ぶところでsetResultsNameすると、元々ついていた名前を上書く
description = Group( module_declaration("module_declaration_call") | ID("id2") )("description")

grammar = ZeroOrMore(description)


def recur_print(presult, indent=0):
    if isinstance(presult,str) or not isinstance(presult,collections.Iterable):
        for i in range(indent):
            sys.stdout.write(" ")
        sys.stdout.write(presult+"\n")
    else:
        print presult
        for e in presult:
            recur_print(e, indent+2)
        

def main():
    result = grammar.parseString('''
module hoge ( a,b, c, d  , e);
task
task
task
initial begin
endmodule

A
B

module hoge2(a1,bb,c,out);
func
always
endmodule
''')
#     print result
#     for index,desc in enumerate(result.descriptions):
#         print "desc[",index,"]=",desc
    
#     print result.dump()
#     for index,desc in enumerate(result.descriptions):
#         print desc.dump()

#    print result.asList()

#     print result
#     print result.asXML()

    for index,desc in enumerate(result.source_text):
#         print index, desc

#         print dir(desc)
        for i,d in enumerate(desc):
            print index, i, " +++ ", d, type(d)

        if(isinstance(d,str)):
            print "str"
        elif(isinstance(d,ParseResults)):
            print "Result"

    print result.asXML()
    
if __name__=='__main__':
    main()
