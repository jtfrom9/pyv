from pyparsing import *

def test(grammer, text, xml=False):
    try:
        print("=== " + grammer.resultsName + " <- \"" + text + "\" ===")
        result = (grammer + pp.stringEnd).parseString(text)
        if result:
            if xml:
                print(result.asXML())
            else:
                print(result)
    except pp.ParseException,pfe:
        print("*** Error detect.")
        print("line={0}".format(pfe.line))
        print("msg={0}".format(pfe.msg))
        print(pfe)
        print(pfe.line);
    except pp.ParseSyntaxException,pfe:
        print("Error detect.")
        print("line={0}".format(pfe.line))
        print("msg={0}".format(pfe.msg))
        print(pfe)
        print(pfe.line);
