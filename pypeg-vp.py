import re, fileinput
import pyPEG
from pyPEG import parse
from pyPEG import keyword, _and, _not, ignore

def source_text():
    return -1, descriptrion

def descriptrion():
    return module_declaration


def ID():
    return _not("endmodule"), _not("module"), re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
    

def module_declaration():
    return keyword("module"), ID, list_of_port_declarations, ";", -1, non_port_module_item, keyword("endmodule")

def non_port_module_item():
    return ID

def list_of_port_declarations():
    return "(", ansi_port_declaration, -1, (",", ansi_port_declaration), ")"

def ansi_port_declaration():
    return ID


pyPEG.print_trace = True

files = fileinput.input()
result = parse(source_text, files, True)
print result
