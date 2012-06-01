from pypeg2 import *

class Type(Keyword):
    grammar = Enum( K("int"), K("long") )

class Parameter:
    grammar = attr("type",Type), name()

    def __repr__(self):
        return "Param{"+self.name+","+self.type+"}"

class Main(List):
#    grammar = "(", optional(csl(Parameter)), ")"
    grammar = "(", optional(csl(Type, Symbol)), ")"

    
if __name__ == '__main__':
    f = parse("(int a, int b)", Main)
    print("f=",f)
#    print("f=",f.name)
    for index,item in enumerate(f):
        print("[",index,"]=",item)

        
#     for value in f.values():
#         print(value)
#     print(f["a"])
#     print(f["b"])

#     f = parse("hoge (long a)", Main)
#     print("f=",f)
#     for key,value in f.items():
#         print("key=",key,",value=",value)


    
