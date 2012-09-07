# -*- coding: utf-8 -*-

with open("non_terminal_symbols.txt","r") as f:
    for sym in f:
        split = sym.split("_")
        funcname = split[0] + "".join(word[0].upper() + word[1:] for word in split[1:])
        print('''
@Action(grammar.{0})
@NotImplemented
def {1}Action(s,l,token):
    pass
'''.format(sym.strip(), funcname.strip()))


