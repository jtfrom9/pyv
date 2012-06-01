from pypeg2 import *

class Type(Keyword):
    grammar = Enum( K("int"), K("long") )

#     def __call__(self):
#         return attr("type",Type)
    
def type():
     return attr("type",Type)

class Parameter:
    grammar = type(), name()

    def __repr__(self):
        return "Parameter = { type=" + self.type + ", name=" + self.name + "}"
    
class Parameters(Namespace):
    grammar = optional(csl(Parameter))
# class Parameters(List):
#     grammar = optional(csl(type(),blank,name()))

class Instruction(str):
    def heading(self, parser):
        return "/* on level " + str(parser.indention_level) + " */", endl
    grammar = heading, word, ";", endl

block = "{", endl, maybe_some(indent(Instruction)), "}", endl

class Function(List):
    grammar = type(), blank, name(), "(", attr("params", Parameters), ")", endl, block
#    grammar = attr("typing", Type), blank, name(), "(", attr("params", Parameters), ")", endl, block


class Hoge(List):
    grammer = type(), blank, name()
#     def __new__(self,obj):
#         pass
    


if __name__ == '__main__':
    f = parse("int f(int a, long b) { do_this; do_that; }", Function, comment=comment_c)
    print("f=",f)
    print("f.name=",f.name)
    print("f.typeing=",f.type)

    for index,item in enumerate(f):
        print('[',index,']=',item)


    print("f.params=",f.params)
    for key,value in f.params.items():
        print('[',key,']=',value)

    f = parse("long a", Hoge, comment=comment_c)
    print("f=",f)


    
