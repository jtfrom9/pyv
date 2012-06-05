from pyparsing import *

source_text = Forward()
description = Forward()
module_declaration = Forward()
list_of_port_declarations = Forward()
non_port_module_item = Forward()

RESERVED_KEYWORDS = ('module', 'endmodule')


ID = ~MatchFirst([Keyword(w) for w in RESERVED_KEYWORDS]) + Word(alphas, alphanums+'_')

#source_text << ZeroOrMore( Group(description) )("descriptions")
source_text << ZeroOrMore(description)("descriptions")
description << Group( Group(module_declaration)("module") ^ ID("id") )("desc")

module_declaration << Suppress(Keyword("module")) + ID("name") + Group(list_of_port_declarations)("params") + Suppress(";") \
    + Group(ZeroOrMore(non_port_module_item))("body") \
    + Suppress(Keyword("endmodule"))

non_port_module_item << ID

list_of_port_declarations << Suppress("(") + ZeroOrMore(ID) + ZeroOrMore( Suppress(",") + ID ) + Suppress(")")



def main():
#     print list_of_port_declarations.parseString(" ( a,  b,c  , d)")
    result = source_text.parseString('''
module hoge(a,b);
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

    print result.dump()
#     for index,desc in enumerate(result.descriptions):
#         print desc.dump()

    print result.asXML()

    for index,desc in enumerate(result.descriptions):
        print index, desc
        print desc.module, desc.id

    
if __name__=='__main__':
    main()
