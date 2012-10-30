# -*- coding: utf-8 -*-
import sys
from pyparsing import *
import ast

self = sys.modules[__name__]

with open("keywords.txt","r") as f:
    _keywords = [line.strip() for line in f]

#ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Word(alphas+'_', alphanums+'_')("id")
ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Regex(r"[a-zA-Z_][a-zA-Z0-9_$]*")("id")
LP,RP,LB,RB,LC,RC,COLON,SEMICOLON,CAMMA,PERIOD,SHARP,EQUAL,AT,ASTA,Q,PLUS,MINUS,USC,APS = map(Suppress,("()[]{}:;,.#=@*?+-_'"))

NB = Suppress(Literal("<="))
TRIG = Suppress(Literal("->"))

#LP/RP : left/right paren          ()
#LB/RB : left/right bracket        []
#LC/RC : left/right curly bracket  {}

for kw in _keywords:
    setattr(self, kw.swapcase(), Keyword(kw)("keyword"))

with open("non_terminal_symbols.txt","r") as f:
    for sym in (line.strip() for line in f):
        #result_name = sym if not sym.endswith("identifier") else "id"
        result_name = sym
        setattr(self, sym, Forward()(result_name))

def alias(grammar, name):
    if name: 
        return Group(grammar)(name)
    else:
        return Group(grammar)

def emsg(msg):
    sym = NoMatch()
    sym.setName(msg)
    return sym

def _group(expr, err):
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

def oneOrMore(expr,name,err=""):
    return alias(OneOrMore(expr),name)

def zeroOrMore(expr,name,err=""):
    return alias(ZeroOrMore(expr),name)

def delim(expr,name=None,delimiter=','):
    def _action(token):
        return token[0]
    expr_ext = _group( delimitedList(expr,delimiter) - NotAny(delimiter),
                       err = "invalid ','" ).setParseAction(_action)
    return alias(expr_ext,name)

def node(token, fail_ret=ast.null):
    if token:
        if isinstance(token,ParseResults):
            return token[0]
        else:
            return token
    else:
        return fail_ret

def GroupedAction(action):
    import inspect
    try:
        frame = inspect.currentframe(2)
    except ValueError as e:
        return None
    else:
        filename = frame.f_code.co_filename
        lineno   = frame.f_lineno

    def _decorator(_s,loc,tokens):
        result = None
        
        #print(">> enter {0}: l={1}, token={2}".format(action.__name__, loc, tokens[0]))
        try:
            result = action(_s, loc, node(tokens))
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

def Action(*argv):
    def _decorator(action):
        func = GroupedAction(action)
        for grammar in argv:
            grammar.setParseAction(func)
        return func
    return _decorator

@GroupedAction
def OneOfAction(s,l,token):
    return node(token)

def NotImplemented(func):
    def _decorator(s,l,t):
        raise Exception("Not Implemented: " + func.__name__)
    return _decorator


    
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
    INOUT + Optional( net_type ) + Optional( SIGNED ) + Optional ( _range ) + list_of_port_identifers )
input_declaration  << Group(
    INPUT + Optional( net_type ) + Optional( SIGNED ) + Optional ( _range ) + list_of_port_identifers )
output_declaration << Group( 
    OUTPUT + Optional(net_type) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers          |
    OUTPUT + Optional(REG)      + Optional(SIGNED) + Optional(_range) + list_of_port_identifers          |
    OUTPUT + REG                + Optional(SIGNED) + Optional(_range) + list_of_variable_port_identifers |
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
reg_declaration      << Group(REG + Optional(SIGNED) + Optional(_range) + list_of_variable_identifiers + SEMICOLON)
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
delay_value << Group( unsigned_number | mintypmax_expression )

# A.2.3 Declaration lists
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
_range    << Group( LB + msb_constant_expression       + COLON + lsb_constant_expression       + RB )

@Action(_range)
def rangeAction(_s,loc,token):
    return ast.Range(token.msb_constant_expression, token.lsb_constant_expression)


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
range_or_type             << Group( _range | INTEGER | REAL | REALTIME | TIME )

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
    INPUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers  | 
    INPUT + Optional(task_port_type) + list_of_port_identifers )

tf_output_declaration << Group( 
    OUTPUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers | 
    OUTPUT + Optional(task_port_type) + list_of_port_identifers )

tf_inout_declaration  << Group( 
    INOUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers  | 
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

block_reg_declaration              << Group( REG + Optional(SIGNED) + Optional(_range) + list_of_block_variable_identifiers + SEMICOLON )
list_of_block_variable_identifiers << Group( delimitedList( block_variable_type ) )
block_variable_type                << Group( identifier | identifier + dimension + ZeroOrMore(dimension) )

# A.3 Primitive instances

# A.4 Module and generated instantiation
# A.4.1 Module instantiation
module_instantiation     << Group( identifier + Optional( parameter_value_assignment ) + delimitedList( module_instance ) + SEMICOLON )
module_instance          << Group( name_of_instance + LP + Optional( list_of_port_connections ) + RP )
name_of_instance         << Group( module_instance_identifier + Optional( _range ) )
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
continuous_assign      << Group( ASSIGN + Optional( delay3 ) + list_of_net_assignment )
list_of_net_assignment << delim( net_assignment )
net_assignment         << Group( net_lvalue + EQUAL + expression )

@Action(continuous_assign)
def continuousAsignmentAction(_s,l,token):
    for asgn in node(token.list_of_net_assignment):
        asgn.setContinuous(token.keyword)
    return [ asgn for asgn in token.list_of_net_assignment ]
                           
@Action(net_assignment)
def netAssignmentAction(_s,l,token):
    return ast.Assignment( node(token.net_lvalue), None, node(token.expression) )
                           

# A.6.2 Procedural blocks and assigments
initial_construct      << Group( INITIAL + statement )
always_construct       << Group( ALWAYS  + statement )

@Action(initial_construct, always_construct)
def initialConstructAction(_s,l,token):
    return ast.Construct(token.keyword, token.statement)

blocking_assignment    << Group( variable_lvalue + EQUAL + Optional( delay_or_event_control ) + expression )
nonblocking_assignment << Group( variable_lvalue + NB    + Optional( delay_or_event_control ) + expression )

@Action(blocking_assignment)
def blockingAssignmentAction(_s,l,token):
    return ast.Assignment( token.variable_lvalue,
                           None,
                           token.expression,
                           blocking = True )

@Action(nonblocking_assignment)
def nonBlockingAssignmentAction(_s,l,token):
    return ast.Assignment( token.variable_lvalue,
                           None,
                           token.expression,
                           blocking = False )

procedural_continuous_assignments << Group( DEASSIGN + alias(variable_lvalue,"lvalue")         |
                                            ASSIGN   + alias(variable_assignment,"assignment") |
                                            FORCE    + alias(variable_assignment,"assignment") |
                                            FORCE    + alias(net_assignment,"assignment")      |
                                            RELEASE  + alias(variable_lvalue,"lvalue")         |
                                            RELEASE  + alias(net_lvalue,"lvalue")              )

@Action(procedural_continuous_assignments)
def proceduralContinuousAssignmentAction(_s,l,token):
    if token.keyword in ['deassign','release']:
        return ast.ReleaseLeftValue(token.keyword,node(token.lvalue))
    else:
        return node(token.assignment)
    
     
function_blocking_assignment << Group( variable_lvalue + EQUAL + expression )
variable_assignment          << Group( variable_lvalue + EQUAL + expression )

@Action(function_blocking_assignment, variable_assignment)
def functionBlockingAssignmentAction(_s,l,token):
    return ast.Assignment(token.variable_lvalue,None,token.expression)


# A.6.3 Parallel and sequential blocks
function_seq_block  << Group( BEGIN + 
                              Optional( COLON + block_identifier + zeroOrMore( block_item_declaration, "item_delcs" ) ) +
                              zeroOrMore( function_statement, "statements" ) +
                              END )
par_block           << Group( FORK + 
                              Optional( COLON + block_identifier  + zeroOrMore( block_item_declaration, "item_delcs" ) ) +
                              zeroOrMore( statement, "statements" ) +
                              JOIN )
seq_block           << Group( BEGIN + 
                              Optional( COLON + block_identifier + zeroOrMore( block_item_declaration, "item_decls") ) +
                              zeroOrMore( statement, "statements" ) +
                              END )

@Action(function_seq_block, seq_block)
def sequencialBlockAction(_s,l,token):
    # print(token)
    # print(ast.nodeInfo(token))
    # print(token.statements)
    # print(ast.nodeInfo(token.statements))
    return ast.Block( [item for item in token.item_decls], 
                      [stmt for stmt in token.statements] )

@Action(par_block)
def parallelBlockAction(_s,l,token):
    return ast.Block( node(token.item_decls, []), node(token.statements, []), seq=False)


# A.6.4 Statements
statement << Group( nonblocking_assignment            + SEMICOLON |
                    blocking_assignment               + SEMICOLON |
                    case_statement                                |
                    conditional_statement                         |
                    disable_statement                             |
                    event_trigger                                 |
                    loop_statement                                |
                    par_block                                     |
                    procedural_continuous_assignments + SEMICOLON |
                    procedural_timing_control_statement           |
                    seq_block                                     |
                    system_task_enable                            |
                    task_enable                                   |
                    wait_statement                                )
statement.setParseAction(OneOfAction)

function_statement << Group( function_blocking_assignment + SEMICOLON |
                             function_case_statement                  |
                             function_conditional_statement           |
                             function_loop_statement                  |
                             function_seq_block                       |
                             disable_statement                        |
                             system_task_enable                       )
function_statement.setParseAction(OneOfAction)

statement_or_null          << Group( SEMICOLON | alias(statement,"stmt")  )
function_statement_or_null << Group( SEMICOLON | alias(function_statement,"stmt") )

@Action(statement_or_null, function_statement_or_null)
def statementOrNullAction(_s,l,token):
    return node(token.stmt) if token.stmt else ast.null



# A.6.5 Timing control statements
delay_control          << Group( SHARP + delay_value | 
                                 SHARP + LP + mintypmax_expression + RP )
delay_or_event_control << Group( delay_control | 
                                 event_control |
                                 REPEAT + LP + expression + RP + event_control )
disable_statement      << Group( DISABLE + hierarchical_identifier  + SEMICOLON )
event_control          << Group( AT + identifier                 |
                                 AT + LP + event_expression + RP |
                                 AT + ASTA                       |
                                 AT + LP + ASTA + RP             )
event_trigger          << Group( TRIG + hierarchical_identifier + SEMICOLON )
event_expression       << Group( expression                               |
                                 hierarchical_identifier                  |
                                 POSEDGE + expression                     |
                                 NEGEDGE + expression                     |
                                 event_expression + OR + event_expression |
                                 event_expression + CAMMA + event_expression )

procedural_timing_control_statement << Group( delay_or_event_control + statement_or_null      )
wait_statement                      << Group( WAIT + LP + expression + RP + statement_or_null )

@Action(event_trigger)
def eventTriggerAction(_s,l,token):
    pass

@Action(procedural_timing_control_statement)
def proceduralTimingControlStatementAction(_s,l,token):
    pass
    

# A.6.6 Conditional statements
conditional_statement << Group( 
    if_else_if_statement
    |
    IF + LP + alias(expression,"condition") + RP + alias(statement_or_null,"statement_if") + 
    Optional( ELSE + alias(statement_or_null,"statement_else") ) )

_else_if_part = Group( ELSE + IF + LP + expression("condition_elseif") + RP + statement_or_null("statement_elseif") )
if_else_if_statement << Group( 
    IF + LP + expression("condition") + RP + statement_or_null("statement_if") + 
    zeroOrMore(_else_if_part,"elseif_blocks") +
    Optional( ELSE + statement_or_null("statement_else") ) )

function_conditional_statement << Group(
    IF + LP + expression + RP + function_statement_or_null +
    Optional( ELSE + function_statement_or_null )
    |
    function_if_else_if_statement )

function_if_else_if_statement << Group(
    IF + LP + expression + RP + function_statement_or_null +
    ZeroOrMore ( ELSE + IF + LP + expression + RP + function_statement_or_null ) +
    Optional   ( ELSE + function_statement_or_null ) )

@Action(conditional_statement)
def conditionalStatementAction(_s,l,token):
    if not token.if_else_if_statement:
        print("<1>")
        print(token.statement_if)
        return ast.Conditional( [(node(token.condition), node(token.statement_if))], node(token.statement_else) )
    else:
        print("<2>")
        return node( token )
                        
@Action(if_else_if_statement)
def ifElseIfStatementAction(_s,l,token):
    # print("condi:{0}".format(dir(token)))
    # print("condi:{0}".format(token.condition))
    return ast.Conditional( [ (node(token.condition), node(token.statement_if)) ] +
                            [ (node(block.condition_elseif), node(block.statement_elseif)) for block in token.elseif_blocks ],
                            node(token.statement_else) )


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
def caseStatementAction(_s,l,token):
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
def loopStatementAction(_s,l,token):
    print("loopStatementAction: {0}".format(token.keyword))
    if token.keyword != 'for':
        #return ast.Loop( node(token.expression),node(token.statement) )
        pass
    else:
        print("init={0}".format(token.init))
        print("exp={0}".format(token.expression))
        print("next={0}".format(token.next))
        #return ast.ForLoop( node(token.init), node(token.expression), node(token.next) )
                            
        
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
concatenation                   << Group( LC + delim(expression,"exps")          + RC )
constant_concatenation          << Group( LC + delim(constant_expression,"exps") + RC )
constant_multiple_concatenation << Group( LC + constant_expression + constant_concatenation + RC )

@Action(concatenation)
def concatenationAction(s,l,token):
    return ast.Concatenation([e for e in token.exps])

@Action(constant_concatenation)
def constantConcatenationAction(s,l,token):
    return ast.Concatenation([e for e in token.exps])

@Action(constant_multiple_concatenation)
@NotImplemented
def constantMultipleConcatenationAction(s,l,token):
    pass

module_path_concatenation          << Group( LC + delimitedList( module_path_expression )         + RC )
module_path_multiple_concatenation << Group( LC + constant_expression + module_path_concatenation + RC )
multiple_concatenation             << Group( LC + constant_expression + concatenation             + RC )

@Action(module_path_concatenation)
@NotImplemented
def modulePathConcatenationAction(s,l,token):
    pass


@Action(module_path_multiple_concatenation)
@NotImplemented
def modulePathMultipleConcatenationAction(s,l,token):
    pass


@Action(multiple_concatenation)
@NotImplemented
def multipleConcatenationAction(s,l,token):
    pass


net_concatenation << Group( LC + delim(net_concatenation_value,"exps") + RC )
net_concatenation_value << Group( 
    hierarchical_identifier + oneOrMore( LB + expression + RB, "exps") + LB + range_expression + RB |
    hierarchical_identifier + oneOrMore( LB + expression + RB, "exps")                              |
    hierarchical_identifier +                                            LB + range_expression + RB |
    hierarchical_identifier                                                                         |
    net_concatenation )

variable_concatenation << Group( LC + delim(variable_concatenation_value,"exps") + RC )
variable_concatenation_value << Group(
    hierarchical_identifier + oneOrMore( LB + expression + RB,"exps" ) + LB + range_expression + RB |
    hierarchical_identifier + oneOrMore( LB + expression + RB,"exps" )                              |
    hierarchical_identifier +                                            LB + range_expression + RB |
    hierarchical_identifier                                                                         |
    variable_concatenation )

@Action(net_concatenation, variable_concatenation)
def _NetVariableConcatenationAction(s,l,token):
    el = [e for e in token.exps]
    return el[0] if len(el)==1 else ast.Concatenation(el)
    

@Action(net_concatenation_value, variable_concatenation_value)
def _NetVariableConcatenationValueAction(s,l,token):
    if token.net_concatenation:
        return node(token.net_concatenation)
    elif token.variable_concatenation:
        return node(token.variable_concatenation)
    else:
        return ast.IdPrimary(token.hierarchical_identifier,
                             [ node(e) for e in token.exps ],
                             node(token.range_expression) if token.range_expression else None )


# A.8.2 Function calls
constant_function_call << Group( identifier              + LP + Optional(delim(constant_expression ,"args")) + RP )
function_call          << Group( hierarchical_identifier + LP + Optional(delim(expression          ,"args")) + RP )
system_function_call   << Group( system_task_identifier  + Optional( LP + Optional(delim(expression,"args")) + RP ) )


@Action(constant_function_call)
def constantFunctionCallAction(s,l,token):
    return ast.FunctionCall(token.identifier, 
                            [arg for arg in token.args])

@Action(function_call)
def functionCallAction(s,l,token):
    return ast.FunctionCall(token.hierarchical_identifier, 
                            [arg for arg in token.args])

@Action(system_function_call)
def systemFunctionCallAction(s,l,token):
    return ast.FunctionCall(token.system_task_identifier,
                            [arg for arg in token.args])


# A.8.3 Expressions
constant_base_expression << constant_expression
constant_base_expression.setParseAction(lambda t: node(t))


_constant_expr  = Forward()
_constant_expr_ = _group( unary_operator + constant_primary |
                          constant_primary                  |
                          string                            ,
                          "_constant_expr_")("_constant_expr_")

_constant_conditional_expression = alias( 
    alias(_constant_expr,"exp_cond") + Q + alias(constant_expression,"exp_if") + COLON + alias(constant_expression,"exp_else"),
    "_constant_conditional_expression")
_constant_expression  = Group( _constant_conditional_expression | _constant_expr_ )

_constant_expr      << operatorPrecedence( _constant_expr_,      [ (binary_operator, 2, opAssoc.LEFT) ] )
constant_expression << operatorPrecedence( _constant_expression, [ (binary_operator, 2, opAssoc.LEFT) ] )

@Action(_constant_conditional_expression)
def _constantConditionalExpressionAction(s,l,token):
    return ast.ConditionalExpression( node(token.exp_cond),
                                      node(token.exp_if),
                                      node(token.exp_else) )

@Action(_constant_expr_)
def _constantExpr_Action(s,l,token):
    if token.unary_operator:
        return ast.UnaryExpression(token.unary_operator, token.constant_primary)
    elif token.constant_primary:
        return token.constant_primary
    else:
        raise Exception("Not Implemented completely _constant_expr_Action: token={0}".format(ast.nodeInfo(token)))
    
@Action(_constant_expression)
def _constantExpressionAction(s,l,token):
    if token._constant_conditional_expression:
        return token._constant_conditional_expression
    elif token._constant_expr_:
        return token._constant_expr_
    else:
        raise Exception("Not Implemented completely _constantExpressionAction: token={0}".format(ast.nodeInfo(token)))

@Action(constant_expression)
def constantExpressionAction(s,l,token):
    if isinstance(token, ast.Expression):
        return token
    elif token.binary_operator:
        return ast.BinaryExpression(token.binary_operator, 
                                    [node(t) for t in token[0::2]])
    else:
        raise Exception("Not Implemented completely constantExpressionAction: token={0}".format(token))
_constant_expr.setParseAction(constantExpressionAction)



constant_mintypmax_expression << Group( alias(constant_expression,"exp") |
                                        constant_expression + COLON + constant_expression + COLON + constant_expression )

constant_range_expression << Group( msb_constant_expression + COLON + lsb_constant_expression   |
                                    constant_expression                                         )
# constant_base_expression + alias(PLUS, "sign") + COLON + width_constant_expression |
# constant_base_expression + alias(MINUS,"sign") + COLON + width_constant_expression |

dimension_constant_expression << constant_expression

@Action(constant_mintypmax_expression)
def constantMintypmaxExpressionAction(s,l,token):
    if token.exp:
        return token.exp
    else:
        raise Exception("Not Implemented completely constantMintypmaxExpressionAction: token={0}".format(token))

@Action(constant_range_expression)
def constantRangeExpressionAction(s,l,token):
    if token.constant_expression:
        return node(token.constant_expression)
    else:
        return ast.Range(node(token.msb_constant_expression),
                         node(token.lsb_constant_expression))

dimension_constant_expression.setParseAction(lambda t: node(t))


_expr  = Forward()
_expr_ = Group( unary_operator + primary | primary | string )("_expr_")

conditional_expression << Group( alias(_expr,"exp_cond") + Q + alias(expression,"exp_if") + COLON + alias(expression,"exp_else") )
_expression = Group( conditional_expression | _expr_ )

_expr      << operatorPrecedence( _expr_,      [ (binary_operator, 2, opAssoc.LEFT) ])
expression << operatorPrecedence( _expression, [ (binary_operator, 2, opAssoc.LEFT) ])


@Action(conditional_expression)
def conditionalExpressionAction(s,l,token):
    return ast.ConditionalExpression( node(token.exp_cond),
                                      node(token.exp_if),
                                      node(token.exp_else) )

@Action(_expr_)
def _expr_Action(_s,l,token):
    if token.unary_operator:
        return ast.UnaryExpression(token.unary_operator, token.primary)
    elif token.primary:
        return token.primary
    else:
        raise Exception("Not Implemented completely _expWithoutCondAction: token={0}".format(token))

@Action(_expression)
def _expressionAction(_s,l,token):
    if token.conditional_expression:
        return token.conditional_expression
    elif token._expr_:
        return token._expr_
    else:
        raise Exception("Not Implemented completely _expressionAction: token={0}".format(token))

@Action(expression, _expr)
def expressionAction(_s,l,token):
    if isinstance(token, ast.Expression):
        return token
    elif token.binary_operator:
        return ast.BinaryExpression(token.binary_operator, 
                                    [node(t) for t in token[0::2]])
    else:
        raise Exception("Not Implemented completely expressionAction: token={0}".format(token))
    

lsb_constant_expression << constant_expression
msb_constant_expression << constant_expression

lsb_constant_expression.setParseAction(lambda t: node(t))
msb_constant_expression.setParseAction(lambda t: node(t))

mintypmax_expression    << Group( expression("exp") | 
                                  expression + COLON + expression + COLON + expression )

module_path_conditional_expression << module_path_expression + Q + module_path_expression + COLON + module_path_expression

module_path_expression << Group( module_path_primary                                                           |
                                 unary_module_path_operator + module_path_primary                              |
                                 module_path_expression + binary_module_path_operator + module_path_expression |
                                 module_path_conditional_expression                                            )

module_path_mintypmax_expression << Group( 
    module_path_expression | 
    module_path_expression + COLON + module_path_expression + COLON + module_path_expression )

range_expression << Group( msb_constant_expression + COLON + lsb_constant_expression |
                           expression                                                )
#                           expression + alias(PLUS, "sign") + COLON + width_constant_expression ^
#                           expression + alias(MINUS,"sign") + COLON + width_constant_expression |

width_constant_expression << constant_expression

@Action(mintypmax_expression)
def mintypmaxExpressionAction(s,l,token):
    if token.exp: return token.exp
    else: raise Exception("Not Implemented completely mintypmaxExpressionAction: token={0}".format(token))

@Action(module_path_conditional_expression)
@NotImplemented
def modulePathConditionalExpressionAction(s,l,token):
    pass

@Action(module_path_expression)
@NotImplemented
def modulePathExpressionAction(s,l,token):
    pass

@Action(module_path_mintypmax_expression)
@NotImplemented
def modulePathMintypmaxExpressionAction(s,l,token):
    pass

@Action(range_expression)
def rangeExpressionAction(s,l,token):
    if token.expression:
        return node(token.expression)
    elif token.expression:
        if token.sign=="+":
            return ast.Range(node(token.base_expression),
                             ndoe(token.width_constant_expression))
        else:
            raise Exception("Not Implemented completely rangeExpressionAction: token={0}".format(token))
    else:
        return ast.Range(node(token.msb_constant_expression),
                         node(token.lsb_constant_expression))

@Action(width_constant_expression)
@NotImplemented
def widthConstantExpressionAction(s,l,token):
    pass


    

# A.8.4 Primaries
constant_primary << _group( number                                  |
                            constant_concatenation                  |
                            constant_multiple_concatenation         |
                            constant_function_call                  |
                            LP + constant_mintypmax_expression + RP ,
                            err = "constant_primary" )

module_path_primary << Group( number                                     |
                              identifier                                 |
                              module_path_concatenation                  |
                              module_path_multiple_concatenation         |
                              function_call                              |
                              system_function_call                       |
                              constant_function_call                     |
                              LP + module_path_mintypmax_expression + RP )

primary << _group( number                                                                                           |
                   function_call                                                                                    |
                   constant_function_call                                                                           |
                   system_function_call                                                                             |
                   hierarchical_identifier + oneOrMore( LB + expression + RB, "exps" ) + LB + range_expression + RB |
                   hierarchical_identifier + oneOrMore( LB + expression + RB, "exps" )                              |
                   hierarchical_identifier                                             + LB + range_expression + RB |
                   hierarchical_identifier                                                                          |
                   concatenation                                                                                    |
                   multiple_concatenation                                                                           |
                   LP + mintypmax_expression + RP                                                                   ,
                   err = "primary")



@Action(constant_primary)
def constantPrimaryAction(s,l,token):
    if token.number:
        return ast.NumberPrimary( token.number )
    elif token.constant_function_call:
        return token.constant_function_call
    elif token.constant_concatenation:
        return token.constant_concatenation
    elif token.constant_mintypmax_expression:
        return token.constant_mintypmax_expression
    else:
        raise Exception("Not Implemented completely constantPrimaryAction: token={0}".format(token))

@Action(module_path_primary)
@NotImplemented
def modulePathPrimaryAction(s,l,token):
    pass


@Action(primary)
def primaryAction(_s,l,token):
    if token.number:
        return ast.NumberPrimary( token.number )
    elif token.hierarchical_identifier:
        return ast.IdPrimary( token.hierarchical_identifier,
                              [ node(exp) for exp in token.exps ],
                              node(token.range_expression) if token.range_expression else None )
    elif token.concatenation:
        return token.concatenation
    elif token.function_call:
        return token.function_call
    elif token.system_function_call:
        return token.system_function_call
    elif token.constant_function_call:
        return token.constant_function_call
    elif token.mintypmax_expression:
        return token.mintypmax_expression
    else:
        raise Exception("Not Implemented completely primaryAction: token={0}".format(token))


# A.8.5 Expression left-side value
net_lvalue << Group( hierarchical_identifier + oneOrMore( LB + constant_expression + RB, "exps" ) + LB + constant_range_expression + RB  |
                     hierarchical_identifier + oneOrMore( LB + constant_expression + RB, "exps" )                                        |
                     hierarchical_identifier                                                      + LB + constant_range_expression + RB  |
                     net_concatenation                                                                                                   |
                     hierarchical_identifier                                                                                             )

variable_lvalue << Group( hierarchical_identifier + oneOrMore( LB + expression + RB, "exps") + LB + range_expression + RB  |
                          hierarchical_identifier + oneOrMore( LB + expression + RB, "exps")                               |
                          hierarchical_identifier                                            + LB + range_expression + RB  |
                          variable_concatenation                                                                           |
                          hierarchical_identifier                                                                          )

@Action(net_lvalue)
def netLvalueAction(s,l,token):
    if token.net_concatenation:
        return token.net_concatenation
    else:
        return ast.LeftSideValue( token.hierarchical_identifier,
                                  token.exps,
                                  token.constant_range_expression )
        
@Action(variable_lvalue)
def variableLvalueAction(s,l,token):
    if token.variable_concatenation:
        return token.variable_concatenation
    else:
        return ast.LeftSideValue( token.hierarchical_identifier,
                                  token.exps,
                                  token.range_expression )

# A.8.6 Operators
unary_operator              << oneOf("+ - ! ~ & ~& | ~| ^ ~^ ^~                                            ")("unary_operator")
binary_operator             << oneOf("+ - * / % == != === !== && || ** < <= > >= & | ^ ^~ ~^ >> << >>> <<< ")("binary_operator")
unary_module_path_operator  << oneOf("! ~ & ~& | ~| ^ ~^ ^~                                                ")("unary_module_path_operator")
binary_module_path_operator << oneOf("== != && || & | ^ ^~ ~^                                              ")("binary_module_path_operator")

# A.8.7 Numbers
number         << Group( decimal_number ^ 
                         octal_number   ^ 
                         binary_number  ^ 
                         hex_number     ^ 
                         real_number    )

_integral_part = Group(unsigned_number)("integral_part")
_decimal_part  = Group(unsigned_number)("decimal_part")
_expornential_part = Group(unsigned_number)("expornential_part")
real_number    << Group( 
    _integral_part + Optional( PERIOD + _decimal_part ) + exp + Optional( sign ) + _expornential_part |
    _integral_part +           PERIOD + _decimal_part )

exp            << oneOf("e E")
decimal_number << Group( Optional( size ) + decimal_base + x_digit + ZeroOrMore( USC ) |
                         Optional( size ) + decimal_base + z_digit + ZeroOrMore( USC ) |
                         Optional( size ) + decimal_base + unsigned_number             |
                         unsigned_number                                               )
binary_number  << Group( Optional( size ) + binary_base + binary_value )
octal_number   << Group( Optional( size ) + octal_base  + octal_value  )
hex_number     << Group( Optional( size ) + hex_base    + hex_value    )

sign                     << oneOf("+ -")
size                     << non_zero_unsigned_number
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
x_digit                  << oneOf("x X")
z_digit                  << oneOf("z Z ?")

non_zero_unsigned_number << Regex(r"[1-9][_0-9]*")
unsigned_number          << Regex(r"[0-9][_0-9]*")
binary_value             << Regex(r"[01xXzZ\?][_01xXzZ\?]*")
octal_value              << Regex(r"[0-7xXzZ\?][_0-7xXzZ\?]*")
hex_value                << Regex(r"[0-9a-fA-FxXzZ\?][_0-9a-fA-FxXzZ\?]*")
decimal_base             << Regex(r"'[sS]?[dD]")
binary_base              << Regex(r"'[sS]?[bB]")
octal_base               << Regex(r"'[sS]?[oO]")
hex_base                 << Regex(r"'[sS]?[hH]")

number.setParseAction(OneOfAction)

@Action(real_number)
def realNumberAction(_s,l,token):
    if not token.exp:
        return ast.Float( node(token.integral_part) + "." + node(token.decimal_part))
    else:
        return ast.Float( node(token.integral_part) + "." + node(token.decimal_part) + token.exp + node(token.sign,"") + node(token.expornential_part) )

@Action(decimal_number)
def decimalNumberAction(_s, loc, token):
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

def valueActions(name,vtype):
    @GroupedAction
    def _action(_s,loc,token):
        width = token.size if token.size else 32
        vstr = getattr(token,name)
        trans = vstr.translate(None,'xXzZ?')
        if trans==vstr:
            return ast.Int2(vstr,width,vtype,int(vstr,vtype))
        else:
            return ast.Int4(vstr,width,vtype,vstr)
    return _action

binary_number.setParseAction (valueActions('binary_value' , ast.FixedWidthValue.Binary))
octal_number.setParseAction  (valueActions('octal_value'  , ast.FixedWidthValue.Octal))
hex_number.setParseAction    (valueActions('hex_value'    , ast.FixedWidthValue.Hex))

size.setParseAction                    (lambda t: int(t[0]))
non_zero_unsigned_number.setParseAction(lambda t: t[0])
unsigned_number.setParseAction         (lambda t: t[0])
binary_value.setParseAction            (lambda t: t[0])
octal_value.setParseAction             (lambda t: t[0])
hex_value.setParseAction               (lambda t: t[0])



# A.8.8 Strings
string << Suppress("\"") + ZeroOrMore( CharsNotIn("\"\n") ) + Suppress("\"")

# A.9 General
# A.9.1 Attributes
# A.9.2 Comments

# A.9.3 Identifiers

# [ a-zA-Z_ ] { [ a-zA-Z0-9_$ ] }
simple_identifier         << ID  
simple_arrayed_identifier << Group( simple_identifier + Optional( _range ) )

@Action(simple_identifier)
def simpleIdentifierAction(_s,loc,token):
    return ast.BasicId(token)

@Action(simple_arrayed_identifier)
def simpleArrayedIdentifierAction(_s,loc,token):
    print(token.simple_identifier)
    if token._range:
        return ast.RangedId(token.simple_identifier.shortName(), token._range)
    else:
        return ast.BasicId(token.simple_identifier.shortName())


# \ {Any_ASCII_character_except_white_space} white_space
escaped_identifier         << simple_identifier # temp
escaped_arrayed_identifier << Group( escaped_identifier + Optional( _range ) )

@Action(escaped_identifier)
@NotImplemented
def escapedIdentifierAction(_s,loc,token):
    pass

@Action(escaped_arrayed_identifier)
@NotImplemented
def escapedArrayedIdentifierAction(_s,loc,token):
    pass


identifier                 << Group( simple_identifier         | escaped_identifier         )
arrayed_identifier         << Group( simple_arrayed_identifier | escaped_arrayed_identifier ) 

identifier.setParseAction         (OneOfAction)
arrayed_identifier.setParseAction (OneOfAction)

module_instance_identifier << arrayed_identifier 
module_instance_identifier.setParseAction (lambda t: node(t))

hierarchical_identifier         << Group( simple_hierarchical_identifier | escaped_hierarchical_identifier )
simple_hierarchical_identifier  << Group( simple_hierarchical_branch + Optional( PERIOD + escaped_identifier ) )

escaped_hierarchical_identifier << Group( escaped_hierarchical_branch + ZeroOrMore( PERIOD + simple_hierarchical_branch |
                                                                                    PERIOD + escaped_hierarchical_branch ) )

    
_simple_hierarchical_branch_part = Group( PERIOD + simple_identifier + Optional( LB + unsigned_number("index") + RB ) )
simple_hierarchical_branch  << Group(
    simple_identifier
    + Optional( LB + unsigned_number("index") + RB )
    + Group( Optional( ZeroOrMore( _simple_hierarchical_branch_part ) ) ) ("ids")
    )

escaped_hierarchical_branch << Group(
    escaped_identifier + Optional( LB + unsigned_number + RB ) + Optional(
        ZeroOrMore( PERIOD + escaped_identifier + Optional( LB + unsigned_number + RB ) ) ) )

system_task_identifier << Regex(r"\$[a-zA-Z0-9_$][a-zA-Z0-9_$]*")

hierarchical_identifier.setParseAction(OneOfAction)

@Action(simple_hierarchical_identifier)
def simpleHierarchicalIdnetifierAction(_s,loc,token):
    ret = token.simple_hierarchical_branch
    if token.escaped_identifier:
        assert isinstance(ret, HierarchicalId)
        ret.addId(ast.BasicId(token.escaped_identifier))
    return ret
        
@Action(escaped_hierarchical_identifier)
@NotImplemented
def escapedHierarchicalIdentifier(_s,loc,token):
    pass

@Action(simple_hierarchical_branch)
def simpleHierarchicalBranchAction(_s,loc,token):
    if token.index:
        headId = ast.IndexedId(token.simple_identifier.string, int(token.index))
    else:
        headId = token.simple_identifier
    ids = [ headId ]
    for id in token.ids: 
        if id.index:
            ids.append(ast.IndexedId(id.simple_identifier.string, int(id.index)))
        else:
            ids.append(id.simple_identifier)
    if len(ids)==1:
        return ids[0]
    else:
        return ast.HierarchicalId(ids)


@Action(escaped_hierarchical_branch)
@NotImplemented
def escapedHierarchicalBranchAction(_s,loc,token):
    pass

@Action(system_task_identifier)
def systemTaskIdentifierAction(s,l,token):
    return ast.BasicId(token)

