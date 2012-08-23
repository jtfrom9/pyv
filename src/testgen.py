
with open("non_terminal_symbols.txt","r") as f:
    for index,sym in enumerate(f):
        print('''
@TestCase2(grammar.{sym})
def test{index}(self):
    pass
'''.format(sym=sym.strip(), index=index))


