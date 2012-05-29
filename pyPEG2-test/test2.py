from pypeg2 import *

class Type(Keyword):
    grammar = Enum( K("int"), K("long") )

class Parameter:
    grammar = attr("type",Type), name()

    def __repr__(self):
        return "Param{"+self.name+","+self.type+"}"

# class Parameters(Namespace):
#     grammar = optional(csl(Parameter))
    
class Main(Namespace):
#     grammar = name(), "(", Parameters, ")"
    grammar = name(), "(", optional(csl(Parameter)), ")"
    
if __name__ == '__main__':
    f = parse("hoge (int a, int b)", Main)
    print("f=",f)
    print("f=",f.name)
    for index,item in enumerate(f):
        print("[",index,"]=",item)
    for value in f.values():
        print(value)
    print(f["a"])
    print(f["b"])
    
#     f = parse("hoge (long a)", Main)
#     print("f=",f)
#     for key,value in f.items():
#         print("key=",key,",value=",value)


    
