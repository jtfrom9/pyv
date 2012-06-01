from pypeg2 import *
from pypeg2.xmlast import thing2xml

class Type(Keyword):
    grammar = Enum( K("int"), K("long") )

    @staticmethod
    def attr(name="type"):
        return attr(name,Type)

class ID(Symbol):
    @staticmethod
    def attr(name="name"):
        return attr(name,ID)

def ID():
    return name()
    
class Parameter:
    grammar = Type.attr(), ID()
    
    def __repr__(self):
        return "Param{"+self.name+","+self.type+"}"

    
class Main(Namespace):
    grammar = optional(csl(Parameter))

    
if __name__ == '__main__':
    f = parse("long a", Main)
    print("f=",f)
#    print("f=",f.name)
    for index,item in enumerate(f):
        print("[",index,"]=",item)

    for value in f.values():
        print(value)
#     print(f["a"])
#     print(f["b"])

#     f = parse("hoge (long a)", Main)
#     print("f=",f)
    for key,value in f.items():
        print("key=",key,",value=",value)

    print(thing2xml(f,pretty=True))
    print(thing2xml(f,pretty=True).decode())
