import re, fileinput
import pyPEG
from pyPEG import parse
from pyPEG import keyword, _and, _not, ignore
from xml.sax.saxutils import escape
from pyPEG import Symbol

def source_text():
    return -1, descriptrion

def descriptrion():
    return module_declaration

reserved = ("endmodule", "module")

def ID():
    return tuple(_not(x) for x in reserved) + (re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),)
    

def module_declaration():
    return keyword("module"), ID, list_of_port_declarations, ";", -1, non_port_module_item, keyword("endmodule")

def non_port_module_item():
    return ID

def list_of_port_declarations():
    return "(", ansi_port_declaration, -1, (",", ansi_port_declaration), ")"

def ansi_port_declaration():
    return ID


def pyAST2XML(pyAST):
    if isinstance(pyAST, unicode) or isinstance(pyAST, str):
        return escape(pyAST)
    if type(pyAST) is Symbol:
#         if pyAST[1][0] is not Symbol:
#             print "****",pyAST[1], type(pyAST[1])
#             print "****",pyAST[1][0], type(pyAST[1][0])
#             result = u"<" + pyAST[0].replace("_","-") + "=" + pyAST[1][0] + u"/>"
#         else:
#         if pyAST[0]=="ID":
#             print "---"
#             print type(pyAST)
#             print type(pyAST[0])
#             print type(pyAST[1])
#             print type(pyAST[1][0])
#             print len(pyAST[1])
#             print pyAST

#         if len(pyAST[1])==1:
#             print "---", pyAST[0],"=", pyAST[1], "   ", type(pyAST[1][0])
            
#         if len(pyAST[1])==1 and type(pyAST[1][0]) is unicode:
#             print "---", pyAST[0],"=", pyAST[1]


        if type(pyAST[1][0]) is not Symbol:
            result = u"<" + pyAST[0].replace("_","-") + "=" + pyAST[1][0] + u"/>"
        else:
            result = u"<" + pyAST[0].replace("_", "-") + u">"
            for e in pyAST[1:]:
                result += pyAST2XML(e)
            result += u"</" + pyAST[0].replace("_", "-") + u">"
    else:
        result = u""
        for e in pyAST:
            result += pyAST2XML(e)
    return result


pyPEG.print_trace = True

files = fileinput.input()
result = parse((source_text,), files, True)
#print result
xml=pyAST2XML(result)

print xml
