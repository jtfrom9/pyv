from pyparsing import *

def main():
    id = Word(alphas,alphanums+'_')("name")
    idlist = delimitedList(id)("list")

    foo = Group("?" + id("name") + "!")("foo")
    bar = Group(("(" + delimitedList(foo) + ")"))("bar")
    
#     print id.parseString("""hoge""")
#     print idlist.parseString("""A, B, C""").asXML()
#     print foo.parseString("? abc !").asXML()
    
    print bar.parseString("(? abc ! )").asXML("")
    
if __name__=='__main__':
    main()
