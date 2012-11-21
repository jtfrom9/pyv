# -*- coding: utf-8 -*-
import sys
from os import path

from pyparsing import (Keyword, Literal, Regex, Regex, MatchFirst, NotAny, CharsNotIn, Suppress, 
                       Forward, Group, Optional, ZeroOrMore, OneOrMore, 
                       delimitedList, operatorPrecedence, opAssoc, oneOf,
                       ParseBaseException,
                       ParseResults)

import ast

this_mod = sys.modules[__name__]

_keywords_file = path.join(path.dirname(this_mod.__file__), "keywords.txt")
_non_terminal_symbols_file = path.join(path.dirname(this_mod.__file__), "non_terminal_symbols.txt")

with open(_keywords_file,"r") as f:
    _keywords = [line.strip() for line in f]

ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Regex(r"[a-zA-Z_][a-zA-Z0-9_$]*")("id")
LP,RP,LB,RB,LC,RC,COLON,SEMICOLON,CAMMA,PERIOD,SHARP,EQUAL,AT,ASTA,Q,PLUS,MINUS,USC,APS = map(Suppress,("()[]{}:;,.#=@*?+-_'"))

NB = Suppress(Literal("<="))
TRIG = Suppress(Literal("->"))

#LP/RP : left/right paren          ()
#LB/RB : left/right bracket        []
#LC/RC : left/right curly bracket  {}

# setup keywords
for kw in _keywords:
    setattr(this_mod, kw.swapcase(), Keyword(kw)("keyword"))

# setup non-terminal-symbols
with open(_non_terminal_symbols_file,"r") as f:
    for name in (line.strip() for line in f):
        sym = Forward()(name)
        sym.enablePackrat()
        setattr(this_mod, name, sym)


def alias(grammar, name):
    if name: 
        return Group(grammar)(name)
    else:
        return Group(grammar)

def _group(expr, err=None):
    class WrapGroup(Group):
        def __init__(self, expr):
            super(WrapGroup,self).__init__(expr)
        def parseImpl(*args):
            self = args[0]
            try:
                return super(WrapGroup,self).parseImpl(*(args[1:]))
            except ParseBaseException,pbe:
                pbe.msg = "Syntax Error: " + err
                raise
    return WrapGroup(expr)

def delim(expr, delimiter=','):
    return _group( delimitedList(expr,delimiter) - NotAny(delimiter),
                   err = "invalid ','" )

def unalias(token): return token[0]
def ungroup(token): return token[0]

# def GroupedAction(action):
#     import inspect
#     try:
#         frame = inspect.currentframe(2)
#     except ValueError as e:
#         return None
#     else:
#         filename = frame.f_code.co_filename
#         lineno   = frame.f_lineno
#     def _decorator(_s,loc,token):
#         result = None
#         try:
#             result = action(_s, loc, token)
#         except Exception as e:
#             raise ParseFatalException(_s, loc, 
#                                       "\n  File \"{filename}\", line {lineno}\n    {reason}".
#                                       format(action   = action.__name__,
#                                              filename = filename,
#                                              lineno   = lineno,
#                                              reason   = e))
#         return result
#     return _decorator

def Action(*argv,**kw):
    def deco_func(action):
        if kw.get('ungroup',False):
            new_func = lambda t: action(ungroup(t))
        else:
            new_func = action
        for grammar in argv:
            grammar.setParseAction(new_func)
        return new_func
    return deco_func

def Grammar(grammar_def_func):
    grammar_def, action = grammar_def_func()
    symbol = getattr(this_mod, grammar_def_func.__name__)
    symbol << grammar_def
    if action:
        symbol.setParseAction(action)
    return symbol

def GrammarNotImplementedYet(grammar_def_func):
    grammar_def = grammar_def_func()[0]
    def _error():
        raise Exception("Not Implemented: " + grammar_def_func.__name__)
    symbol = getattr(this_mod, grammar_def_func.__name__)
    symbol << grammar_def
    symbol.setParseAction(_error)
    return symbol

class NotImplementedCompletelyAction(Exception):
    def __init__(self, token=None):
        import inspect
        frame = inspect.currentframe(1)
        msg = "Error at {0}:{1}".format(
            frame.f_code.co_filename,
            frame.f_lineno)
        if token:
            msg += "\n    token={0}".format(ast.nodeInfo(token))
        super(Exception,self).__init__(msg)

# A.1 Source text2
# A.1.1 Library source text
# A.1.2 Configuration source text

# A.1.3 Module and primitive source text
source_text << ZeroOrMore( description )
description << Group ( module_declaration )

module_declaration << Group (  
    (MODULE + ID + Optional( module_parameter_port_list ) + Optional( list_of_ports ) + SEMICOLON +
    ZeroOrMore( module_item ) +
    ENDMODULE)
    ^
    (MODULE + ID + Optional( module_parameter_port_list ) + Optional( list_of_port_declarations ) + SEMICOLON + 
    ZeroOrMore( non_port_module_item ) +
    ENDMODULE ))
    
# A.1.4 Module parametersand ports
#module_parameter_port_list << SHARP + LP parameter
list_of_ports              << LP + delimitedList( port ) + RP
list_of_port_declarations  << Group( LP + delimitedList( port_declaration ) + RP | 
                                     LP + RP  )
                                     
port             << Group( Optional( port_expression ) | 
                           PERIOD + ID + LP + Optional( port_expression ) + RP )
port_expression  << Group( port_reference                            | 
                           LC + delimitedList( port_reference ) + RC )
port_reference   << Group( identifier                    |
                           ID + LB + constant_expression + RB |
                           ID + LB + range_expression    + RB )
port_declaration << Group ( inout_declaration | 
                            input_declaration | 
                            output_declaration )

# A.1.5 Module items
module_item                         << Group( module_or_generate_item | 
                                              port_declaration + SEMICOLON )

module_or_generate_item             << Group( module_or_generate_item_declaration |
                                              continuous_assign                   |
                                              module_instatantiation              |
                                              initial_construct                   | 
                                              always_construct  )

module_or_generate_item_declaration << Group( net_declaration      | 
                                              reg_declaration      | 
                                              integer_declaration  |
                                              real_declaration     |
                                              time_declaration     |
                                              realtime_declaration | 
                                              event_declaration    |
                                              task_declaration     | 
                                              function_declaration )

non_port_module_item                << module_or_generate_item


# A.2   Declarations


# A.2.1 Declaration types   

# A.2.1.1 Module parameter declarations
# A.2.1.2 Port declarations
inout_declaration  << Group(
    INOUT + Optional( net_type ) + Optional( SIGNED ) + Optional ( range_ ) + list_of_port_identifers )
input_declaration  << Group(
    INPUT + Optional( net_type ) + Optional( SIGNED ) + Optional ( range_ ) + list_of_port_identifers )
output_declaration << Group( 
    OUTPUT + Optional(net_type) + Optional(SIGNED) + Optional(range_) + list_of_port_identifers          |
    OUTPUT + Optional(REG)      + Optional(SIGNED) + Optional(range_) + list_of_port_identifers          |
    OUTPUT + REG                + Optional(SIGNED) + Optional(range_) + list_of_variable_port_identifers |
    OUTPUT + Optional( output_variable_type )                         + list_of_port_identifers          |
    OUTPUT + output_variable_type                                     + list_of_variable_port_identifers )

# A.2.1.3 Type declarations
event_declaration   << Group(EVENT   + list_of_event_identifiers    + SEMICOLON)
integer_declaration << Group(INTEGER + list_of_variable_identifiers + SEMICOLON)
net_declaration     << Group(
    net_type + Optional(SIGNED)                            + Optional(delay3) + list_of_net_identifiers      + SEMICOLON |
    net_type + Optional(drive_strength) + Optional(SIGNED) + Optional(delay3) + list_of_net_decl_assignments + SEMICOLON )

real_declaration     << Group(REAL                                      + list_of_real_identifiers     + SEMICOLON)
realtime_declaration << Group(REALTIME                                  + list_of_real_identifiers     + SEMICOLON)
reg_declaration      << Group(REG + Optional(SIGNED) + Optional(range_) + list_of_variable_identifiers + SEMICOLON)
time_declaration     << Group(TIME                                      + list_of_variable_identifiers + SEMICOLON)

# A.2.2 Declaration data types
# A.2.2.1 Net and variable types
net_type             << WIRE
output_variable_type << Group( INTEGER | TIME )
real_type            << Group( identifier + Optional( EQUAL + constant_expression ) |
                               identifier + dimension + ZeroOrMore ( dimension ) )
variable_type        << Group( identifier + Optional( EQUAL + constant_expression ) | 
                               identifier + dimension + ZeroOrMore ( dimension ) )

# A.2.2.2 Strenghths

# A.2.2.3 Delays
delay3      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value + Optional ( CAMMA + delay_value ) ) + RP )
delay2      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value ) + RP )

delay_value << ( unsigned_number | mintypmax_expression )

@Action(delay_value)
def delayValueAction(token):
    if token.unsigned_number:
        return ast.NumberPrimary(ast.Int2(token.unsigned_number, 
                                          32, 
                                          ast.FixedWidthValue.Decimal,
                                          int(token.unsigned_number)))
    else:
        return token[0]

# A.2.3 Declaration listsp
list_of_event_identifiers        << Group(delimitedList( identifier + Optional( dimension + ZeroOrMore(dimension) ) ))
list_of_net_decl_assignments     << Group(delimitedList( net_decl_assignment                                        ))
list_of_net_identifiers          << Group(delimitedList( identifier + Optional( dimension + ZeroOrMore(dimension) ) ))
list_of_port_identifers          << Group(delimitedList( identifier                                                 ))
list_of_real_identifiers         << Group(delimitedList( real_type                                                  ))
list_of_variable_identifiers     << Group(delimitedList( variable_type                                              ))
list_of_variable_port_identifers << Group(delimitedList( identifier + Optional( EQUAL + constant_expression )       ))

# A.2.4 Declaration assignments
net_decl_assignment << Group( identifier + EQUAL + expression )

# A.2.5 Declaration ranges
dimension << Group( LB + dimension_constant_expression + COLON + dimension_constant_expression + RB )

@Grammar
def range_( _ = LB + msb_constant_expression + COLON + lsb_constant_expression + RB ):
    return (_, lambda t:ast.Range(t.msb_constant_expression, t.lsb_constant_expression))


# A.2.6 Function declarations
function_declaration << Group( 
    FUNCTION + 
    Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + identifier + SEMICOLON + 
    function_item_declaration + ZeroOrMore( function_item_declaration ) + 
    function_statement + 
    ENDFUNCTION
    ^
    FUNCTION + 
    Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + identifier + LP + function_port_list + RP + SEMICOLON + 
    block_item_declaration + ZeroOrMore(block_item_declaration) + 
    function_statement + 
    ENDFUNCTION
    )

function_item_declaration << Group( block_item_declaration | tf_input_declaration + SEMICOLON )
function_port_list        << Group( tf_input_declaration + ZeroOrMore( CAMMA + tf_input_declaration ) )
range_or_type             << Group( range_ | INTEGER | REAL | REALTIME | TIME )

# A.2.7 Task declarations
task_declaration << Group( 
    TASK + Optional(AUTOMATIC) + identifier + SEMICOLON + 
    ZeroOrMore( task_item_declaration ) + 
    statement + 
    ENDTASK
    ^
    TASK + Optional(AUTOMATIC) + identifier + LP + task_port_list + RP + SEMICOLON + 
    ZeroOrMore( block_item_declaration ) + 
    statement + 
    ENDTASK )

task_item_declaration << Group( block_item_declaration            | 
                                tf_input_declaration  + SEMICOLON | 
                                tf_output_declaration + SEMICOLON | 
                                tf_inout_declaration  + SEMICOLON )

task_port_list        << Group( delimitedList( task_port_item ) )
task_port_item        << Group( tf_inout_declaration | tf_output_declaration | tf_inout_declaration )

tf_input_declaration  << Group( 
    INPUT + Optional(REG) + Optional(SIGNED) + Optional(range_) + list_of_port_identifers  | 
    INPUT + Optional(task_port_type) + list_of_port_identifers )

tf_output_declaration << Group( 
    OUTPUT + Optional(REG) + Optional(SIGNED) + Optional(range_) + list_of_port_identifers | 
    OUTPUT + Optional(task_port_type) + list_of_port_identifers )

tf_inout_declaration  << Group( 
    INOUT + Optional(REG) + Optional(SIGNED) + Optional(range_) + list_of_port_identifers  | 
    INOUT + Optional(task_port_type) + list_of_port_identifers )

task_port_type << Group( TIME | REAL | REALTIME | INTEGER )

# A.2.8 Block item declarations
block_item_declaration << Group( 
    block_reg_declaration |
    event_declaration     | 
    integer_declaration   | 
    real_declaration      |
    realtime_declaration  |
    time_declaration )

block_reg_declaration              << Group( REG + Optional(SIGNED) + Optional(range_) + list_of_block_variable_identifiers + SEMICOLON )
list_of_block_variable_identifiers << Group( delimitedList( block_variable_type ) )
block_variable_type                << Group( identifier | identifier + dimension + ZeroOrMore(dimension) )

# A.3 Primitive instances

# A.4 Module and generated instantiation
# A.4.1 Module instantiation
module_instantiation     << Group( identifier + Optional( parameter_value_assignment ) + delimitedList( module_instance ) + SEMICOLON )
module_instance          << Group( name_of_instance + LP + Optional( list_of_port_connections ) + RP )
name_of_instance         << Group( module_instance_identifier + Optional( range_ ) )
list_of_port_connections << Group( delimitedList ( ordered_port_connection ) |
                                   delimitedList ( named_port_connection   ) )
ordered_port_connection  << Group( Optional( expression ) )
named_port_connection    << Group( PERIOD + identifier + LP + Optional( expression ) + RP )

# A.4.2 Generated instantiation

# A.5 UDP declaration and instantiation
# A.5.1 UDP declaration
# A.5.2 UDP ports
# A.5.3 UDP body
# A.5.4 UDP instantiation

# A.6 Behavioral statements
# A.6.1 Continuous assignment statements
@Grammar
def net_assignment( _ = net_lvalue + EQUAL + expression ):
    return (_, lambda t: ast.Assignment( t.net_lvalue, None, t.expression ))

@Grammar
def list_of_net_assignment( _ = delim(net_assignment)("list") ):
    return (_, lambda t: ast.NodeList([ x for x in t.list ]))

@Grammar
def continuous_assign(_ = ASSIGN + Optional( delay3 ) + list_of_net_assignment ):
    return (_, lambda t: ast.ContinuousAssignmentItems(t.keyword,t.list_of_net_assignment))


# A.6.2 Procedural blocks and assigments

initial_construct << INITIAL + statement 
always_construct  << ALWAYS  + statement

@Action(initial_construct, always_construct)
def constructAction(token):
    return ast.ConstructStatementItem(token.keyword, token.statement)

@Grammar
def blocking_assignment( _ = variable_lvalue + EQUAL + Optional( delay_or_event_control ) + expression ):
    return (_, lambda t: ast.Assignment( t.variable_lvalue,
                                         None,
                                         t.expression,
                                         blocking = True ))
@Grammar            
def nonblocking_assignment( _ = variable_lvalue + NB + Optional( delay_or_event_control ) + expression ):
    return (_, lambda t: ast.Assignment( t.variable_lvalue,
                                         None,
                                         t.expression,
                                         blocking = False ))

@Grammar
def procedural_continuous_assignments():
    _ = ( DEASSIGN + alias(variable_lvalue,"lvalue")         |
          ASSIGN   + alias(variable_assignment,"assignment") |
          FORCE    + alias(variable_assignment,"assignment") |
          FORCE    + alias(net_assignment,"assignment")      |
          RELEASE  + alias(variable_lvalue,"lvalue")         |
          RELEASE  + alias(net_lvalue,"lvalue")              )
    def action(token):
        if token.keyword in ['deassign','release']:
            return ast.ReleaseLeftValue(token.keyword, unalias(token.lvalue))
        else:
            return ast.ContinuousAssignmentItems(token.keyword, ast.NodeList([ unalias(token.assignment) ]))
    return (_,action)
    
@Grammar     
def function_blocking_assignment( _ = variable_lvalue + EQUAL + expression ):
    return (_, lambda t: ast.Assignment(t.variable_lvalue,None,t.expression))

@Grammar
def variable_assignment(         _ = variable_lvalue + EQUAL + expression ):
    return (_, lambda t: ast.Assignment(t.variable_lvalue,None,t.expression))


# A.6.3 Parallel and sequential blocks

@Grammar
def function_seq_block():
    return (( BEGIN + 
              Optional( COLON + block_identifier + ZeroOrMore(block_item_declaration)("item_delcs") ) +
              ZeroOrMore(function_statement)("statements") +
              END ),
            lambda t: ast.Block( [item for item in t.item_decls], 
                                 [stmt for stmt in t.statements] ))

@Grammar
def seq_block():
    return (( BEGIN + 
              Optional( COLON + block_identifier + ZeroOrMore(block_item_declaration)("item_decls") ) +
              ZeroOrMore(statement)("statements") +
              END ),
            lambda t: ast.Block( [item for item in t.item_decls], 
                                 [stmt for stmt in t.statements] ))

@Grammar
def par_block():
    return (( FORK + 
              Optional( COLON + block_identifier  + ZeroOrMore(block_item_declaration)("item_delcs") ) +
              ZeroOrMore(statement)("statements") +
              JOIN ),
            lambda t: ast.Block( [item for item in t.item_decls], 
                                 [stmt for stmt in t.statements], seq=False))


# A.6.4 Statements
@Grammar
def statement():
    return ((case_statement                                |
             conditional_statement                         |
             disable_statement                             |
             event_trigger                                 |
             loop_statement                                |
             par_block                                     |
             procedural_timing_control_statement           |
             seq_block                                     |
             system_task_enable                            |
             task_enable                                   |
             wait_statement                                |
             nonblocking_assignment            - SEMICOLON |
             blocking_assignment               - SEMICOLON |
             procedural_continuous_assignments - SEMICOLON ),
            lambda t: t)

@Grammar
def function_statement():
    return (( function_blocking_assignment + SEMICOLON |
              function_case_statement                  |
              function_conditional_statement           |
              function_loop_statement                  |
              function_seq_block                       |
              disable_statement                        |
              system_task_enable                       ),
            lambda t:t )

@Grammar
def statement_or_null( _ = SEMICOLON | statement ):
    return (_, lambda t: t.statement if t.statement else ast.null)

@Grammar
def function_statement_or_null( _ = SEMICOLON | function_statement ):
    return (_, lambda t: t.function_statement if t.function_statement else ast.null)


# A.6.5 Timing control statements
@Grammar
def delay_control():
    _ = ( SHARP + delay_value | 
          SHARP + LP + mintypmax_expression + RP )
    def action(token):
        v = token.delay_value if token.delay_value else token.mintypmax_expression
        return ast.DelayControl(v)
    return (_,action)
            
@Grammar
def delay_or_event_control():
    _ = ( delay_control | 
          event_control |
          REPEAT + LP + expression + RP + event_control )
    def action(token):
        if not token.expression: return token[0]
        else: raise NotImplementedCompletelyAction(token)
    return (_,action)

@GrammarNotImplementedYet
def disable_statement():
    return (( DISABLE + hierarchical_identifier  + SEMICOLON ), )

@Grammar
def event_control():
    _ = (AT + identifier                 |
         AT + LP + event_expression + RP |
         AT + ASTA                       |
         AT + LP + ASTA + RP             )
    def action(token):
        if token.identifier:
            return ast.EventControl(ast.WaitTypeId, token.identifier)
        elif token.event_expression:
            return ast.EventControl(ast.WaitTypeExpr, token.event_expression)
        else:
            return ast.EventControl(ast.WaitTypeAny, None)
    return (_,action)

@Grammar
def event_trigger( _ = TRIG + hierarchical_identifier + SEMICOLON ):
    return (_, lambda t: ast.Trigger(t.hierarchical_identifier) )

@Grammar
def event_expression():
    ev_base_expr = ( POSEDGE + expression    |
                     NEGEDGE + expression    |
                     hierarchical_identifier |
                     expression              )
    @Action(ev_base_expr)
    def ev_base_expr_action(token):
        if token.keyword:
            return ast.EdgeExpression(token.keyword, token.expression)
        elif token.hierarchical_identifier:
            return ast.IdPrimary(token.hierarchical_identifier)
        else:
            return token.expression

    _ = operatorPrecedence( ev_base_expr, [ (OR,                      2, opAssoc.LEFT),
                                            (Literal(",")("keyword"), 2, opAssoc.LEFT) ] )
    def action(s,l,_token):
        token = ungroup(_token)
        if isinstance(token, ast.Expression): 
            return token
        elif token.keyword:
            return ast.BinaryExpression(token.keyword,
                                        [t for t in token[0::2]])
        else:
            raise NotImplementedCompletelyAction(token)
    return (_, action)

@Grammar
def procedural_timing_control_statement():
    return ((delay_or_event_control + statement_or_null),
            lambda t: ast.TimingControlStatement(t.delay_or_event_control, t.statement_or_null))
        
@Grammar
def wait_statement():
    return (( WAIT + LP + expression + RP + statement_or_null ),
            lambda t: ast.Wait(t.expression, t.statement_or_null if t.statement_or_null else ast.null))


# A.6.6 Conditional statements

conditional_statement << ( 
    alias(if_else_if_statement,"if_else_stmt")
    |
    IF + LP + expression + RP + alias(statement_or_null,"stmt")          + Optional( ELSE + alias(statement_or_null,"else_stmt") ) )

function_conditional_statement << ( 
    alias(function_if_else_if_statement,"if_else_stmt")
    |
    IF + LP + expression + RP + alias(function_statement_or_null,"stmt") + Optional( ELSE + alias(function_statement_or_null,"else_stmt" ) ) )

@Action(conditional_statement, function_conditional_statement)
def conditionalStatementAction(token):
    if token.if_else_stmt:
        return unalias(token.if_else_stmt)
    else:
        return ast.ConditionalStatement( [(token.expression, unalias(token.stmt))], 
                                         unalias(token.else_stmt) if token.else_stmt else None )


if_else_if_statement << ( 
    IF + LP + expression + RP + alias(statement_or_null,"stmt") + 
    ZeroOrMore( Group(ELSE + IF + LP + expression + RP + alias(statement_or_null,"stmt")) )("elseif_blocks") +
    Optional( ELSE + alias(statement_or_null, "else_stmt") ) )

function_if_else_if_statement << (
    IF + LP + expression + RP + alias(function_statement_or_null,"stmt") +
    ZeroOrMore( Group(ELSE + IF + LP + expression + RP + alias(function_statement_or_null,"stmt")) )("elseif_blocks") +
    Optional( ELSE + alias(function_statement_or_null,"else_stmt") ) )


@Action(if_else_if_statement, function_if_else_if_statement)
def ifElseifStatementAction(token):
    return ast.ConditionalStatement( [ (token.expression, unalias(token.stmt)) ] +
                                     [ (elseif.expression, unalias(elseif.stmt)) for elseif in token.elseif_blocks ],
                                     unalias(token.else_stmt) if token.else_stmt else None )


# A.6.7 Case statements
case_statement << Group( CASE  + LP + expression + RP + OneOrMore( case_item ) + ENDCASE |
                         CASEZ + LP + expression + RP + OneOrMore( case_item ) + ENDCASE |
                         CASEX + LP + expression + RP + OneOrMore( case_item ) + ENDCASE )
case_item      << Group( delimitedList( expression ) + COLON + statement_or_null |
                         DEFAULT + Optional( COLON ) + statement_or_null         )

function_case_statement << Group( CASE  + LP + expression + RP + OneOrMore (function_case_item ) + ENDCASE |
                                  CASEZ + LP + expression + RP + OneOrMore (function_case_item ) + ENDCASE |
                                  CASEX + LP + expression + RP + OneOrMore (function_case_item ) + ENDCASE )
function_case_item      << Group( delimitedList( expression ) + COLON + function_statement_or_null |
                                  DEFAULT + Optional( COLON ) + function_statement_or_null         )


@Action(case_statement)
def caseStatementAction(token):
    pass


# A.6.8 Loop statements
function_loop_statement << Group( 
    FOREVER + function_statement                       |
    REPEAT + LP + expression + RP + function_statement |
    WHILE  + LP + expression + RP + function_statement 
    |
    FOR + LP + variable_assignment + SEMICOLON + expression + SEMICOLON + variable_assignment + RP +
    function_statement )

loop_statement << Group(
    FOREVER + statement                       |
    REPEAT + LP + expression + RP + statement |
    WHILE  + LP + expression + RP + statement 
    |
    FOR + LP + variable_assignment("init") + SEMICOLON + expression + SEMICOLON + variable_assignment("next") + RP +
    statement )

@Action(loop_statement)
def loopStatementAction(token):
    print("loopStatementAction: {0}".format(token.keyword))
    if token.keyword != 'for':
        pass
    else:
        print("init={0}".format(token.init))
        print("exp={0}".format(token.expression))
        print("next={0}".format(token.next))
                            
        
# A.6.9 Task enable statements
system_task_enable << Group( 
    system_task_identifier + Optional( LP + delimitedList( expression ) + LP ) + SEMICOLON )

task_enable << Group(
    hierarchical_identifier + Optional( LP + delimitedList( expression ) + LP ) + SEMICOLON )

# A.7 Specify section
# A.7.1 Specify block declaration
# A.7.2 Specify path declaration
# A.7.3 Specify block terminals
# A.7.4 Specify path delays

# A.7.5 System timing checks
# A.7.5.1 System timing check commands
# A.7.5.2 System timing check command arguments
# A.7.5.3 System timing check event definitions


# A.8 Expressions
# A.8.1 Concatenations
@Grammar
def concatenation( _ = LC + delim(expression)("exps") + RC ):
    return (_, lambda token: ast.Concatenation([e for e in token.exps]))

@Grammar
def constant_concatenation( _ = LC + delim(constant_expression)("exps") + RC ):
    return (_, lambda token: ast.Concatenation([e for e in token.exps]))

@GrammarNotImplementedYet
def constant_multiple_concatenation( _ = LC + constant_expression + constant_concatenation + RC ):
    return (_,)

@GrammarNotImplementedYet
def module_path_concatenation():
    return ( LC + delimitedList( module_path_expression ) + RC, )

@GrammarNotImplementedYet
def module_path_multiple_concatenation():
    return (LC + constant_expression + module_path_concatenation + RC, )

@GrammarNotImplementedYet
def multiple_concatenation():
    return ( LC + constant_expression + concatenation + RC, )


net_concatenation << LC + delim(net_concatenation_value)("con_values") + RC 
net_concatenation_value << ( 
    hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps") + LB + range_expression + RB |
    hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps")                              |
    hierarchical_identifier +                                                  LB + range_expression + RB |
    hierarchical_identifier                                                                               |
    net_concatenation )

variable_concatenation <<  LC + delim(variable_concatenation_value)("con_values") + RC 
variable_concatenation_value << (
    hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps") + LB + range_expression + RB |
    hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps")                              |
    hierarchical_identifier +                                                  LB + range_expression + RB |
    hierarchical_identifier                                                                               |
    variable_concatenation )

@Action(net_concatenation, variable_concatenation)
def _NetVariableConcatenationAction(token):
    vlist = [e for e in token.con_values]
    if len(vlist)==1: 
        return vlist[0]
    else:
        return ast.Concatenation(vlist)

@Action(net_concatenation_value, variable_concatenation_value)
def _NetVariableConcatenationValueAction(token):
    if token.net_concatenation:
        return token.net_concatenation
    elif token.variable_concatenation:
        return token.variable_concatenation
    else:
        return ast.IdPrimary(token.hierarchical_identifier,
                             [ e.expression for e in token.exps ],
                             token.range_expression if token.range_expression else None )


# A.8.2 Function calls
@Grammar
def constant_function_call( _ = identifier + LP + Optional(delim(constant_expression)("args")) + RP ):
    return (_, lambda token: ast.FunctionCall(token.identifier, [arg for arg in token.args]))

@Grammar
def function_call( _ = hierarchical_identifier + LP + Optional(delim(expression)("args")) + RP ):
    return (_, lambda token: ast.FunctionCall(token.hierarchical_identifier, [arg for arg in token.args]))

@Grammar
def system_function_call( _ = system_task_identifier + Optional( LP + Optional(delim(expression)("args")) + RP ) ):
    return (_, lambda token: ast.FunctionCall(token.system_task_identifier, [arg for arg in token.args]))


# A.8.3 Expressions
@Grammar
def constant_base_expression(): 
    return (constant_expression, lambda t: t[0])

@Grammar
def constant_expression():
    basic_primary = _group( unary_operator + constant_primary |
                            constant_primary                  |
                            string                            ,
                            "basic_primary")

    @Action(basic_primary, ungroup=True)
    def basicPrimaryAction(token):
        if token.unary_operator:
            return ast.UnaryExpression(token.unary_operator, token.constant_primary)
        elif token.constant_primary:
            return token.constant_primary
        else:
            raise NotImplementedCompletelyAction(token)
    
    basic_expr = Forward()

    cond_expr = ( alias(basic_expr,"exp_cond") + Q + 
                  alias(constant_expression,"exp_if") + COLON + alias(constant_expression,"exp_else") )
    cond_expr.setParseAction(lambda t: 
                             ast.ConditionalExpression(unalias(t.exp_cond), unalias(t.exp_if), unalias(t.exp_else)))

    expr = cond_expr | basic_primary 
    expr.setParseAction(lambda t: t[0])

    basic_expr           << operatorPrecedence( basic_primary, [ (binary_operator, 2, opAssoc.LEFT) ] )
    _constant_expression  = operatorPrecedence( expr,          [ (binary_operator, 2, opAssoc.LEFT) ] )

    @Action(basic_expr, ungroup=True)
    def action(token):
        if isinstance(token, ast.Expression):
            return token
        elif token.binary_operator:
            return ast.BinaryExpression(token.binary_operator, 
                                        [t for t in token[0::2]])
        else:
            raise NotImplementedCompletelyAction(token)

    return (_constant_expression, action)


@Grammar
def constant_mintypmax_expression():
    _ = ( alias(constant_expression,"exp") |
          constant_expression + COLON + constant_expression + COLON + constant_expression )
    def action(token):
        if token.exp:
            return token.exp
        else:
            raise NotImplementedCompletelyAction(token)
    return (_,action)

@Grammar
def constant_range_expression():
    _ = ( msb_constant_expression + COLON + lsb_constant_expression   |
          constant_expression                                         )
# constant_base_expression + alias(PLUS, "sign") + COLON + width_constant_expression |
# constant_base_expression + alias(MINUS,"sign") + COLON + width_constant_expression |

    def action(token):
        if token.msb_constant_expression or token.lsb_constant_expression:
            return ast.Range(token.msb_constant_expression, token.lsb_constant_expression)
        else:
            return token.constant_expression
    return (_, action)

@Grammar
def dimension_constant_expression( _ = constant_expression ):
    return (_, lambda t: t)


basic_expr = Forward()

@Grammar
def conditional_expression():
    return ( alias(basic_expr,"exp_cond") + Q + alias(expression,"exp_if") + COLON + alias(expression,"exp_else"),
             lambda token: ast.ConditionalExpression( unalias(token.exp_cond),
                                                      unalias(token.exp_if),
                                                      unalias(token.exp_else) ))

@Grammar
def expression():
    basic_primary = unary_operator + primary | primary | string 

    @Action(basic_primary)
    def basicPrimaryAction(token):
        if token.unary_operator:
            return ast.UnaryExpression(token.unary_operator, token.primary)
        elif token.primary:
            return token.primary
        else:
            raise NotImplementedCompletelyAction(token)

    term = conditional_expression | basic_primary
    term.setParseAction(lambda t: t)

    basic_expr << operatorPrecedence( basic_primary,  [ (binary_operator, 2, opAssoc.LEFT) ])
    _expression = operatorPrecedence( term,           [ (binary_operator, 2, opAssoc.LEFT) ])

    @Action(basic_expr, ungroup=True)
    def action(token):
        if isinstance(token, ast.Expression):
            return token
        elif token.binary_operator:
            return ast.BinaryExpression(token.binary_operator, 
                                        [t for t in token[0::2]])
        else:
            raise NotImplementedCompletelyAction(token)
    return (_expression, action)

@Grammar
def lsb_constant_expression(): return (constant_expression, lambda t: t)

@Grammar
def msb_constant_expression(): return (constant_expression, lambda t: t)

@Grammar
def mintypmax_expression():
    _ = ( alias(expression, "exp") | 
          expression + COLON + expression + COLON + expression )
    def action(token):
        if token.exp: return unalias(token.exp)
        else: raise NotImplementedCompletelyAction(token)
    return (_,action)

@GrammarNotImplementedYet
def module_path_conditional_expression():
    return (module_path_expression + Q + module_path_expression + COLON + module_path_expression, )

@GrammarNotImplementedYet
def module_path_expression():
    return (( module_path_primary                                                           |
              unary_module_path_operator + module_path_primary                              |
              module_path_expression + binary_module_path_operator + module_path_expression |
              module_path_conditional_expression                                            ), )

@GrammarNotImplementedYet
def module_path_mintypmax_expression():
    return (( module_path_expression | 
              module_path_expression + COLON + module_path_expression + COLON + module_path_expression ), )

@Grammar
def range_expression():
    _ = ( msb_constant_expression + COLON + lsb_constant_expression |
          expression                                                )
#                           expression + alias(PLUS, "sign") + COLON + width_constant_expression ^
#                           expression + alias(MINUS,"sign") + COLON + width_constant_expression |
    def action(token):
        if token.expression:
            return token.expression
        elif token.expression:
            if token.sign=="+":
                return ast.Range( token.base_expression, token.width_constant_expression )
            else:
                raise NotImplementedCompletelyAction(token)
        else:
            return ast.Range(token.msb_constant_expression, token.lsb_constant_expression)
    return (_,action)

@GrammarNotImplementedYet
def width_constant_expression(): 
    return (constant_expression, )


# A.8.4 Primaries

@Grammar
def primary():
    _ = _group( number                                                                                                |
                function_call                                                                                         |
                constant_function_call                                                                                |
                system_function_call                                                                                  |
                hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps") + LB + range_expression + RB |
                hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps")                              |
                hierarchical_identifier                                           + LB + range_expression + RB        |
                hierarchical_identifier                                                                               |
                concatenation                                                                                         |
                multiple_concatenation                                                                                |
                LP + mintypmax_expression + RP                                                                        ,
                err = "primary")
    @Action(ungroup=True)
    def action(token):
        if token.number:
            return ast.NumberPrimary( token.number )
        elif token.hierarchical_identifier:
            return ast.IdPrimary( token.hierarchical_identifier,
                                  [ e.expression for e in token.exps ],
                                  token.range_expression if token.range_expression else None )
        elif (token.concatenation or token.function_call or 
              token.system_function_call or token.constant_function_call or
              token.mintypmax_expression):
            return token[0]
        else:
            raise NotImplementedCompletelyAction(token)
    return (_,action)

@Grammar
def constant_primary():
    _ = _group( number                                  |
                constant_concatenation                  |
                constant_multiple_concatenation         |
                constant_function_call                  |
                LP + constant_mintypmax_expression + RP ,
                err = "constant_primary" )
    @Action(ungroup=True)
    def action(token):
        if token.number:
            return ast.NumberPrimary( token.number )
        elif (token.constant_concatenation or 
              token.constant_multiple_concatenation or 
              token.constant_function_call or 
              token.constant_mintypmax_expression):
            return token[0]
        else:
            raise NotImplementedCompletelyAction(token)
    return (_,action)

@GrammarNotImplementedYet
def module_path_primary():
    return (( number                                     |
              identifier                                 |
              module_path_concatenation                  |
              module_path_multiple_concatenation         |
              function_call                              |
              system_function_call                       |
              constant_function_call                     |
              LP + module_path_mintypmax_expression + RP ), )


# A.8.5 Expression left-side value

@Grammar
def net_lvalue():
    _ = ( hierarchical_identifier + OneOrMore(Group(LB + constant_expression + RB))("exps") + LB + constant_range_expression + RB |
          hierarchical_identifier + OneOrMore(Group(LB + constant_expression + RB))("exps")                                       |
          hierarchical_identifier                                                           + LB + constant_range_expression + RB |
          net_concatenation                                                                                                       |
          hierarchical_identifier                                                                                                 )
    def action(token):
        if token.net_concatenation:
            return token.net_concatenation
        else:
            return ast.IdPrimary( token.hierarchical_identifier,
                                  [ e.constant_expression for e in token.exps ],
                                  token.constant_range_expression )
    return (_,action)

@Grammar
def variable_lvalue(): 
    _ = ( hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps") + LB + range_expression + RB |
          hierarchical_identifier + OneOrMore(Group(LB + expression + RB))("exps")                              |
          hierarchical_identifier                                                  + LB + range_expression + RB |
          variable_concatenation                                                                                |
          hierarchical_identifier                                                                               )
    def action(token):
        if token.variable_concatenation:
            return token.variable_concatenation
        else:
            return ast.IdPrimary( token.hierarchical_identifier,
                                  [ e.expression for e in token.exps ],
                                  token.range_expression )
    return (_,action)

# A.8.6 Operators
unary_operator              << oneOf("+ - ! ~ & ~& | ~| ^ ~^ ^~                                            ")
binary_operator             << oneOf("+ - * / % == != === !== && || ** < <= > >= & | ^ ^~ ~^ >> << >>> <<< ")
unary_module_path_operator  << oneOf("! ~ & ~& | ~| ^ ~^ ^~                                                ")
binary_module_path_operator << oneOf("== != && || & | ^ ^~ ~^                                              ")

# A.8.7 Numbers

@Grammar
def number( _ = decimal_number ^ octal_number ^ binary_number ^ hex_number ^ real_number ):
    return (_, lambda t: t[0])

@Grammar
def real_number():
    _integral_part     = Group( unsigned_number )("integral_part")
    _decimal_part      = Group( unsigned_number )("decimal_part")
    _expornential_part = Group( unsigned_number )("expornential_part")

    @Action(_integral_part, _decimal_part, _expornential_part, ungroup=True)
    def realNumberPartAction(token): 
        return token.unsigned_number

    _ = ( _integral_part + Optional( PERIOD + _decimal_part ) + exp + Optional( sign ) + _expornential_part |
          _integral_part +           PERIOD + _decimal_part                                                 )
    def action(token):
        if not token.exp:
            return ast.Float( token.integral_part + "." + token.decimal_part)
        else:
            return ast.Float( token.integral_part + "." + token.decimal_part + 
                              token.exp + 
                              (token.sign if token.sign else "") + 
                              token.expornential_part )
    return (_,action)

@Grammar
def decimal_number():
    _ = ( Optional( size ) + decimal_base + x_digit + ZeroOrMore( USC ) |
          Optional( size ) + decimal_base + z_digit + ZeroOrMore( USC ) |
          Optional( size ) + decimal_base + unsigned_number             |
          unsigned_number                                               )
    def action(token):
        def dval(vstr): 
            return int(vstr, ast.FixedWidthValue.Decimal)
        def i2val(width):
            val = int(token.unsigned_number)
            if val >= pow(2,width):
                print("Warning: constant {0} is truncate to {1} bit value: {2}".format(
                        token.unsigned_number, width, pow(2,width)-1))
            return ast.Int2(token.unsigned_number,width,ast.FixedWidthValue.Decimal, val)
        def i4val(width,v):
            return ast.Int4(v,width,ast.FixedWidthValue.Decimal, v*width)

        if len(token)==1:
            return i2val(32)
        else:
            width = token.size if token.size else 32
            if token.x_digit:
                return i4val(width,token.x_digit)
            if token.z_digit:
                return i4val(width,token.z_digit)
            if token.unsigned_number:
                return i2val(width)
            return (_,action)
    return (_,action)

binary_number  << Optional( size ) + binary_base + binary_value 
octal_number   << Optional( size ) + octal_base  + octal_value 
hex_number     << Optional( size ) + hex_base    + hex_value 

def valueActions(name,vtype):
    def action(token):
        width = token.size if token.size else 32
        vstr = getattr(token,name)
        trans = vstr.translate(None,'xXzZ?')
        if trans==vstr:
            return ast.Int2(vstr,width,vtype,int(vstr,vtype))
        else:
            return ast.Int4(vstr,width,vtype,vstr)
    return action

binary_number.setParseAction(valueActions('binary_value' , ast.FixedWidthValue.Binary))
octal_number.setParseAction (valueActions('octal_value'  , ast.FixedWidthValue.Octal))
hex_number.setParseAction   (valueActions('hex_value'    , ast.FixedWidthValue.Hex))

exp  << oneOf("e E")
sign << oneOf("+ -")
# non_zero_unsigned_number << non_zero_decimal_digit + ZeroOrMore( USC | decimal_digit )
# unsigned_number          << decimal_digit + ZeroOrMore( USC | decimal_digit ) 
# binary_value             << binary_digit  + ZeroOrMore( USC | binary_digit )
# octal_value              << octal_digit   + ZeroOrMore( USC | octal_digit )
# hex_value                << hex_digit     + ZeroOrMore( USC | hex_digit )
# decimal_base             << APS + Optional( oneOf("s S") ) + oneOf("d D")
# binary_base              << APS + Optional( oneOf("s S") ) + oneOf("b B")
# octal_base               << APS + Optional( oneOf("s S") ) + oneOf("o O")
# hex_base                 << APS + Optional( oneOf("s S") ) + oneOf("h H")
# non_zero_decimal_digit   << oneOf("  1 2 3 4 5 6 7 8 9")
# decimal_digit            << oneOf("0 1 2 3 4 5 6 7 8 9")
# binary_digit             << Group( x_digit | z_digit | Suppress("0") | Suppress("1") )
# octal_digit              << Group( x_digit | z_digit | oneOf("0 1 2 3 4 5 6 7") )
# hex_digit                << Group( x_digit | z_digit | oneOf("0 1 2 3 4 5 6 7 8 9 a b c d ef A B C D E F") )
x_digit      << oneOf("x X")
z_digit      << oneOf("z Z ?")
decimal_base << Regex(r"'[sS]?[dD]")
binary_base  << Regex(r"'[sS]?[bB]")
octal_base   << Regex(r"'[sS]?[oO]")
hex_base     << Regex(r"'[sS]?[hH]")


non_zero_unsigned_number << Regex(r"[1-9][_0-9]*")
unsigned_number          << Regex(r"[0-9][_0-9]*")
binary_value             << Regex(r"[01xXzZ\?][_01xXzZ\?]*")
octal_value              << Regex(r"[0-7xXzZ\?][_0-7xXzZ\?]*")
hex_value                << Regex(r"[0-9a-fA-FxXzZ\?][_0-9a-fA-FxXzZ\?]*")
@Action(non_zero_unsigned_number, unsigned_number, binary_value, octal_value, hex_value, ungroup=True)
def valueAction(t): return t

@Grammar
def size(): return (non_zero_unsigned_number, lambda t: int(t[0]))


# A.8.8 Strings
string << Suppress("\"") + ZeroOrMore( CharsNotIn("\"\n") ) + Suppress("\"")

# A.9 General
# A.9.1 Attributes
# A.9.2 Comments

# A.9.3 Identifiers

# [ a-zA-Z_ ] { [ a-zA-Z0-9_$ ] }
@Grammar
def simple_identifier():
    return (ID, lambda t: ast.BasicId(t[0]))

@Grammar
def simple_arrayed_identifier( _ = simple_identifier + Optional( range_ ) ):
    def action(token):
        if token.range_:
            return ast.RangedId(str(token.simple_identifier), token.range_)
        else:
            return ast.BasicId(str(token.simple_identifier))
    return (_, action)


# \ {Any_ASCII_character_except_white_space} white_space

@GrammarNotImplementedYet
def escaped_identifier(): 
    return (simple_identifier, )#temp

@GrammarNotImplementedYet
def escaped_arrayed_identifier():
    return (( escaped_identifier + Optional( range_ ) ), )

@Grammar
def identifier():
    return (( simple_identifier | escaped_identifier ), lambda t: t[0])

@Grammar
def arrayed_identifier():
    return (( simple_arrayed_identifier | escaped_arrayed_identifier ), lambda t: t[0])

@Grammar
def module_instance_identifier():
    return (arrayed_identifier , lambda t: t)

@Grammar
def hierarchical_identifier():
    return (( simple_hierarchical_identifier | escaped_hierarchical_identifier ), lambda t: t[0])

@Grammar
def simple_hierarchical_identifier():
    _ = simple_hierarchical_branch + Optional( PERIOD + escaped_identifier ) 
    def action(token):
        ret = token.simple_hierarchical_branch
        if token.escaped_identifier:
            ret.addId(ast.BasicId(token.escaped_identifier))
        return ret
    return (_,action)

@GrammarNotImplementedYet
def escaped_hierarchical_identifier():
    return ((escaped_hierarchical_branch + ZeroOrMore( PERIOD + simple_hierarchical_branch |
                                                       PERIOD + escaped_hierarchical_branch ) ), )
@Grammar
def simple_hierarchical_branch():
    index = unsigned_number("index")
    index.setParseAction(lambda t: t[0])

    _ = ( simple_identifier + 
          Optional( LB + index + RB ) +
          ZeroOrMore( Group(PERIOD + simple_identifier + Optional( LB + index + RB )))("part_list") )
          
    def action(token):
        if token.index:
            headId = ast.IndexedId(str(token.simple_identifier), int(token.index))
        else:
            headId = token.simple_identifier
        ids = [ headId ]
        if token.part_list:
            #print("part_list={0}".format(token.part_list))
            for part in token.part_list: 
                # print("part={0}".format(ast.nodeInfo(part)))
                # print("has index = {0}".format(part.index))
                if part.index:
                    ids.append(ast.IndexedId(str(part.simple_identifier), int(part.index)))
                else:
                    ids.append(part.simple_identifier)
        if len(ids)==1:
            return ids[0]
        else:
            return ast.HierarchicalId(ids)
    return (_,action)

@GrammarNotImplementedYet
def escaped_hierarchical_branch():
    return (( escaped_identifier + Optional( LB + unsigned_number + RB ) + Optional(
                ZeroOrMore( PERIOD + escaped_identifier + Optional( LB + unsigned_number + RB ) ) ) ), )

@Grammar
def system_task_identifier():
    return (Regex(r"\$[a-zA-Z0-9_$][a-zA-Z0-9_$]*"),
            lambda t: ast.BasicId(t[0]))

