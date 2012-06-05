from pyparsing import *

source_text = Forward()
description = Forward()
module_declaration = Forward()
list_of_port_declarations = Forward()
non_port_module_item = Forward()

ID = Word(alphas, alphanums+'_')
LP = Suppress("(")
RP = Suppress(")")
SEMCOLON = Suppress(";")

source_text << ZeroOrMore(description)
description << module_declaration

#module_declaration << Keyword("module") + ID + list_of_port_declarations + SEMCOLON + ZeroOrMore(non_port_module_item) + Keyword("endmodule")
module_declaration << Keyword("module") + ID("name") + Group(list_of_port_declarations) + SEMCOLON \
    + non_port_module_item \
    + Keyword("endmodule")

non_port_module_item << ID("body")

list_of_port_declarations << LP + ZeroOrMore(ID) + ZeroOrMore( Suppress(",") + ID ) + RP

def main():
    print list_of_port_declarations.parseString(" ( a,  b,c  , d)")
    print module_declaration.parseString('''
module hoge(a,b);
always
endmodule
''')
#     print module_declaration.parseString('''
# module hoge( a, b, c);
# endmodule
# ''')


if __name__=='__main__':
    main()
