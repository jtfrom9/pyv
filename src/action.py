# -*- coding: utf-8 -*-
import unittest
import pprint
import math
import inspect

from pyparsing import ParseFatalException, traceParseAction, ParseResults
import grammar
import ast
from test_common import *

def GroupedAction(action):
    frame    = inspect.currentframe(2)
    filename = frame.f_code.co_filename
    lineno   = frame.f_lineno

    def _decorator(_s,loc,tokens):
        result = None
        
        #print(">> enter {0}: l={1}, token={2}".format(action.__name__, loc, tokens[0]))
        try:
            result = action(_s, loc, tokens[0])
        except Exception as e:
            raise ParseFatalException(_s, loc, 
                                      "\n  File \"{filename}\", line {lineno}\n    {reason}".
                                      format(action   = action.__name__,
                                             filename = filename,
                                             lineno   = lineno,
                                             reason   = e))
        #print("<< exit  {0}: ret={1}".format(action.__name__, result))
        return result
    return _decorator

def Action(grammar):
    def _decorator(action):
        func = GroupedAction(action)
        grammar.setParseAction(func)
        return func
    return _decorator

def node(token, fail_ret=ast.null):
    if token:
        if isinstance(token,ParseResults):
            return token[0]
        else:
            return token
    else:
        return fail_ret
 
# A.2.1.2 Port declarations (0/3)
# A.2.1.3 Type declarations (0/7)
# A.2.2.1 Net and variable types (0/4)
# A.2.2.3 Delays (0/3)
# A.2.3 Declaration lists (0/7)
# A.2.4 Declaration assignments (0/1)

# A.2.5 Declaration ranges (1/2)

@Action(grammar._range)
def rangeAction(_s,loc,token):
    # print("rangeAction: s={0}, loc={1}, token={2}".format(s,loc,token))
    # print("msb_constant_expression={0}".format(token.msb_constant_expression.asXML()))
    # print("lsb_constant_expression={0}".format(token.lsb_constant_expression))
    try:
        if not token.msb_constant_expression:
            raise Exception("1")
        if not token.msb_constant_expression.constant_expression:
            raise Exception("2")
        if not token.msb_constant_expression.constant_expression[0].constant_primary:
            raise Exception("3")
        if not token.msb_constant_expression.constant_expression[0].constant_primary[0].number:
            raise Exception("4")
    except Exception as msg:
        print("_range Not Implemented completely: {0}".format(msg))
        assert False
    return ast.Range(token.msb_constant_expression.constant_expression[0].constant_primary[0].number,
                     token.lsb_constant_expression.constant_expression[0].constant_primary[0].number)

# A.2.6 Function declarations (0/4)
# A.2.7 Task declarations (0/8)
# A.2.8 Block item declarations (0/4)

# A.4.1 Module instantiation (0/6)

# A.6.1 Continuous assignment statements (1/3)
@Action(grammar.net_assignment)
def netAssignmentAction(_s,l,token):
    return ast.Assignment( node(token.net_lvalue), None, node(token.expression) )

                           
# A.6.2 Procedural blocks and assignments (3/7)
@Action(grammar.nonblocking_assignment)
def nonBlockingAssignmentAction(_s,l,token):
    return ast.Assignment( node( token.variable_lvalue ),
                           node( token.delay_or_event_control ),
                           node( token.expression ),
                           blocking = False )

@Action(grammar.blocking_assignment)
def blockingAssignmentAction(_s,l,token):
    return ast.Assignment( node( token.variable_lvalue ),
                           node( token.delay_or_event_control ),
                           node( token.Expression ),
                           blocking = True )

@Action(grammar.procedural_continuous_assignments)
def proceduralContinuousAssignmentAction(_s,l,token):
    if token.variable_assignment:
        return ast.ContinuousAssignment(token.keyword, node(token.variable_assignment))
    elif token.net_assignment:
        return ast.ContinuousAssignment(token.keyword, node(token.net_assignment))
    elif token.variable_lvalue:
        return ast.ContinuousAssignment(token.keyword, node(token.variable_lvalue))
    elif token.net_lvalue:
        return ast.ContinuousAssignment(token.keyword, node(token.net_lvalue))
         
# A.6.3 Parallel and sequential blocks (1/4)
@Action(grammar.variable_assignment)
def variableAssignmentAction(_s,l,token):
    return ast.Assignment( node( token.variable_lvalue ),
                           None,
                           node( token.expression ) )

@Action(grammar.seq_block)
def sequencialBlockAction(_s,l,token):
    return ast.SequencialBlock( node(token.item_decls, []),
                                node(token.statements, []) )


# A.6.4 Statements (2/3)

@Action(grammar.statement)
def statementAction(_s,l,token):
    if (token.nonblocking_assignment              or 
        token.blocking_assignment                 or
        token.case_statement                      or 
        token.conditional_statement               or
        token.loop_statement                      or
        token.event_trigger                       or
        token.wait_statement                      or
        token.procedural_casontinuous_assignments or
        token.procedural_timing_control_statement or
        token.seq_block ):
        return node(token)
    else:
        raise Exception("Not implemented completely statementAction")

@Action(grammar.statement_or_null)
def statementOrNullAction(_s,l,token):
    #print("Action: statement_or_null token={0}".format(token))
    return node(token.statement)

# A.6.5 Timing control statements (2/8)
@Action(grammar.event_trigger)
def eventTriggerAction(_s,l,token):
    pass

@Action(grammar.procedural_timing_control_statement)
def proceduralTimingControlStatementAction(_s,l,token):
    pass
    

# A.6.6 Conditional statements (0/4)
@Action(grammar.conditional_statement)
def conditionalStatementAction(_s,l,token):
    if not token.if_else_if_statement:
        return ast.Conditional( [(node(token.condition), node(token.statement_if))], node(token.statement_else) )
    else:
        return node( token )
                        
@Action(grammar.if_else_if_statement)
def ifElseIfStatementAction(_s,l,token):
#     print("token={0}".format(token))
#     print("token.elseif_blocks={0}".format(token.elseif_blocks))
#     print("token.elseif_blocks={0}".format(dir(token.elseif_blocks)))
#     for block in token.elseif_blocks:
#         print("block={0}".format(block))
#         print("block.cond_elseif={0}".format(block.condition_elseif))
#         print("block.cond_elseif={0}".format(block.condition_elseif))
    return ast.Conditional( [ (node(token.condition), node(token.statement_if)) ] +
                            [ (node(block.condition_elseif), node(block.statement_elseif)) for block in token.elseif_blocks ],
                            node(token.statement_else) )

# A.6.7 Case statements  (0/4)
@Action(grammar.case_statement)
def caseStatementAction(_s,l,token):
    pass

# A.6.8 Loop statements (0/2)
@Action(grammar.loop_statement)
def loopStatementAction(_s,l,token):
    pass

# A.6.9 Task enable statements (0/2)



# A.8.1 Concatenations (0/10)
# A.8.2 Function calls (0/3)

# A.8.3 Expressions (0/16)

@Action(grammar.expression)
def expressionAction(_s,l,token):
    if token.unary_operator:
        return ast.UnaryExpression(token.unary_operator, token.primary)
    elif token.binary_operator:
        return ast.BinaryExpression(token.binary_operator, token[0], token[2])
    elif token.primary:
        return token
    else:
        raise Exception("Not Implemented completely expressionAction: token={0}".format(token))
    
# A.8.4 Primaries (1/3)

@Action(grammar.primary)
def primaryAction(_s,l,token):
    if token.number:
        return ast.Primary( node(token.number) )
    elif token.hierarchical_identifier:
        return ast.Primary(( node(token.hierarchical_identifier), 
                             node(token.expression), 
                             node(token.range_expression) ))
    elif token.function_call:
        pass
    else:
        raise Exception("Not Implemented completely primaryAction: token={0}".format(token))


# A.8.5 Expression left-side value (2/2)

@Action(grammar.net_lvalue)
def netLvalueAction(s,l,token):
    if token.net_concatenation:
        raise Exception("Not Implemented. net_concatenation")
    else:
        return ast.LeftSideValue( node(token.hierarchical_identifier),
                                  [ node(e.constant_expression) for e in token.exps ],
                                  node(token.constant_range_expression) )
        
@Action(grammar.variable_lvalue)
def variableLvalueAction(s,l,token):
    if token.variable_concatenation:
        raise Exception("Not Implemented. variable_concatenation")
    else:
        return ast.LeftSideValue( node(token.hierarchical_identifier),
                                  [ node(e.expression) for e in token.exps ],
                                  node(token.range_expression) )

# A.8.7 Numbers

@Action(grammar.number)
def numberAction(_s,l,token): 
    return token

@Action(grammar.real_number)
def realNumberAction(_s,l,token):
    if not token.exp:
        return ast.Float( node(token.integral_part) + "." + node(token.decimal_part))
    else:
        return ast.Float( node(token.integral_part) + "." + node(token.decimal_part) + token.exp + node(token.sign,"") + node(token.expornential_part) )

@Action(grammar.decimal_number)
def decimalNumberAction(_s, loc, token):
    def dval(vstr): 
        return int(vstr, ast.FixedWidthValue.Decimal)
    def s2val(width):
        val = int(token.unsigned_number)
        if val >= pow(2,width):
            print("Warning: constant {0} is truncate to {1} bit value: {2}".format(
                    token.unsigned_number, width, pow(2,width)-1))
        return ast.State2Value(token.unsigned_number,width,ast.FixedWidthValue.Decimal, val)
    def s4val(width,v):
        return ast.State4Value(v,width,ast.FixedWidthValue.Decimal, v*width)

    if len(token)==1:
        return s2val(32)
    else:
        width = token.size if token.size else 32
        if token.x_digit:
            return s4val(width,token.x_digit)
        if token.z_digit:
             return s4val(width,token.z_digit)
        if token.unsigned_number:
            return s2val(width)

def valueActions(name,vtype):
    @GroupedAction
    def _action(_s,loc,token):
        width = token.size if token.size else 32
        vstr = getattr(token,name)
        trans = vstr.translate(None,'xXzZ?')
        if trans==vstr:
            return ast.State2Value(vstr,width,vtype,int(vstr,vtype))
        else:
            return ast.State4Value(vstr,width,vtype,vstr)
    return _action

grammar.binary_number.setParseAction (valueActions('binary_value' , ast.FixedWidthValue.Binary))
grammar.octal_number.setParseAction  (valueActions('octal_value'  , ast.FixedWidthValue.Octal))
grammar.hex_number.setParseAction    (valueActions('hex_value'    , ast.FixedWidthValue.Hex))

grammar.size.setParseAction                    (lambda t: int(t[0]))
grammar.non_zero_unsigned_number.setParseAction(lambda t: t[0])
grammar.unsigned_number.setParseAction         (lambda t: t[0])
grammar.binary_value.setParseAction            (lambda t: t[0])
grammar.octal_value.setParseAction             (lambda t: t[0])
grammar.hex_value.setParseAction               (lambda t: t[0])


# A.9.3 Identifiers
@Action(grammar.simple_identifier)
def simpleIdentifierAction(_s,loc,token):
    return ast.BasicId(token)

@Action(grammar.identifier)
def identifierAction(_s,loc,token):
    if token.simple_identifier:
        return token.simple_identifier
    elif token.escaped_identifier:
        return token.escaped_identifier
    else:
        assert False

@Action(grammar.simple_arrayed_identifier)
def simpleArrayedIdentifierAction(_s,loc,token):
    print(token.simple_identifier)
    if token._range:
        return ast.RangedId(token.simple_identifier.shortName(), token._range)
    else:
        return ast.BasicId(token.simple_identifier.shortName())

@Action(grammar.arrayed_identifier)
def arrayedIdentifierAction(_s,loc,token):
    if token.simple_arrayed_identifier:
        return token.simple_arrayed_identifier
    elif token.escaped_arrayed_identifier:
        return token.escaped_arrayed_identifier
    else:
        assert False
    
@Action(grammar.simple_hierarchical_branch)
def simpleHierarchicalBranchAction(_s,loc,token):
    index = None
    if token.index:
        index = int(token.index)
    ids=[]
    for id in token.ids:
        if id.index:
            ids.append(ast.IndexedId( node(id.name), int(id.index) ))
        else:
            ids.append(ast.BasicId( node(id.name) ))
    return ast.HierarchicalId(token.simple_identifier, index, ids)
    #return ast.HierarchicalId(token.name, index, ids)

@Action(grammar.simple_hierarchical_identifier)
def simpleHierarchicalIdnetifierAction(_s,loc,token):
    if not token.escaped_identifier:
        return token
    else:
        assert isinstance(token, HierarchicalId)
        token.addId(ast.BasicId(token.escaped_identifier))
        
