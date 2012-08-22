# -*- coding: utf-8 -*-
import sys
from pyparsing import *

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
    return Group(grammar)(name)

# A.1 Source text2
# A.1.1 Library source text
# A.1.2 Configuration source text

# A.1.3 Module and primitive source text
source_text << ZeroOrMore( description )
description << Group ( module_declaration )

module_declaration << Group (  
    (MODULE - ID + Optional( module_parameter_port_list ) + Optional( list_of_ports ) - SEMICOLON +
    ZeroOrMore( module_item ) -
    ENDMODULE)
    ^
    (MODULE - ID + Optional( module_parameter_port_list ) + Optional( list_of_port_declarations ) - SEMICOLON + 
    ZeroOrMore( non_port_module_item ) -
    ENDMODULE ))
    
# A.1.4 Module parametersand ports
#module_parameter_port_list << SHARP + LP parameter
list_of_ports              << LP + delimitedList( port ) - RP
list_of_port_declarations  << Group( LP + delimitedList( port_declaration ) + RP | 
                                     LP - RP  )
                                     
port             << Group( Optional( port_expression ) | 
                           PERIOD - ID - LP - Optional( port_expression ) - RP )
port_expression  << Group( port_reference                            | 
                           LC + delimitedList( port_reference ) - RC )
port_reference   << Group( port_identifier                    |
                           ID + LB + constant_expression - RB |
                           ID + LB + range_expression    - RB )
port_declaration << Group ( inout_declaration | 
                            input_declaration | 
                            output_declaration )

# A.1.5 Module items
module_item                         << Group( module_or_generate_item | 
                                              port_declaration - SEMICOLON )

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
event_declaration   << Group(EVENT   + list_of_event_identifiers    - SEMICOLON)
integer_declaration << Group(INTEGER + list_of_variable_identifiers - SEMICOLON)
net_declaration     << Group(
    net_type + Optional(SIGNED)                            + Optional(delay3) + list_of_net_identifiers      - SEMICOLON |
    net_type + Optional(drive_strength) + Optional(SIGNED) + Optional(delay3) + list_of_net_decl_assignments - SEMICOLON )

real_declaration     << Group(REAL                                      + list_of_real_identifiers     - SEMICOLON)
realtime_declaration << Group(REALTIME                                  + list_of_real_identifiers     - SEMICOLON)
reg_declaration      << Group(REG + Optional(SIGNED) + Optional(_range) + list_of_variable_identifiers - SEMICOLON)
time_declaration     << Group(TIME                                      + list_of_variable_identifiers - SEMICOLON)

# A.2.2 Declaration data types
# A.2.2.1 Net and variable types
net_type             << WIRE
output_variable_type << Group( INTEGER | TIME )
real_type            << Group( real_identifier + Optional( EQUAL + constant_expression ) |
                               real_identifier + dimension + ZeroOrMore ( dimension ) )
variable_type        << Group( variable_identifier + Optional( EQUAL + constant_expression ) | 
                               variable_identifier + dimension + ZeroOrMore ( dimension ) )

# A.2.2.2 Strenghths

# A.2.2.3 Delays
delay3      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value + Optional ( CAMMA + delay_value ) ) + RP )
delay2      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value ) + RP )
delay_value << Group( unsigned_number | mintypmax_expression )

# A.2.3 Declaration lists
list_of_event_identifiers        << Group(delimitedList( event_identifier + Optional( dimension + ZeroOrMore(dimension) ) ))
list_of_net_decl_assignments     << Group(delimitedList( net_decl_assignment                                              ))
list_of_net_identifiers          << Group(delimitedList( net_identifier + Optional( dimension + ZeroOrMore(dimension) )   ))
list_of_port_identifers          << Group(delimitedList( port_identifier                                                  ))
list_of_real_identifiers         << Group(delimitedList( real_type                                                        ))
list_of_variable_identifiers     << Group(delimitedList( variable_type                                                    ))
list_of_variable_port_identifers << Group(delimitedList( port_identifier + Optional( EQUAL + constant_expression )        ))

# A.2.4 Declaration assignments
net_decl_assignment << Group( net_identifier - EQUAL + expression )

# A.2.5 Declaration ranges
dimension << Group( LB + dimension_constant_expression - COLON + dimension_constant_expression - RB )
_range    << Group( LB + msb_constant_expression       - COLON + lsb_constant_expression       - RB )

# A.2.6 Function declarations
function_declaration << Group( 
    FUNCTION + 
    Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + function_identifier + SEMICOLON + 
    function_item_declaration + ZeroOrMore( function_item_declaration ) + 
    function_statement + 
    ENDFUNCTION
    ^
    FUNCTION + 
    Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + function_identifier + LP + function_port_list + RP + SEMICOLON + 
    block_item_declaration + ZeroOrMore(block_item_declaration) + 
    function_statement + 
    ENDFUNCTION
    )

function_item_declaration << Group( block_item_declaration | tf_input_declaration + SEMICOLON )
function_port_list        << Group( tf_input_declaration + ZeroOrMore( CAMMA + tf_input_declaration ) )
range_or_type             << Group( _range | INTEGER | REAL | REALTIME | TIME )

# A.2.7 Task declarations
task_declaration << Group( 
    TASK + Optional(AUTOMATIC) + task_identifier + SEMICOLON + 
    ZeroOrMore( task_item_declaration ) + 
    statement + 
    ENDTASK
    ^
    TASK + Optional(AUTOMATIC) + task_identifier + LP + task_port_list + RP + SEMICOLON + 
    ZeroOrMore( block_item_declaration ) + 
    statement + 
    ENDTASK )

task_item_declaration << Group( block_item_declaration            | 
                                tf_input_declaration  - SEMICOLON | 
                                tf_output_declaration - SEMICOLON | 
                                tf_inout_declaration  - SEMICOLON )

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
block_variable_type                << Group( variable_identifier | variable_identifier + dimension + ZeroOrMore(dimension) )

# A.3 Primitive instances

# A.4 Module and generated instantiation
# A.4.1 Module instantiation
module_instantiation     << Group( module_identifier + Optional( parameter_value_assignment ) + delimitedList( module_instance ) - SEMICOLON )
module_instance          << Group( name_of_instance - LP + Optional( list_of_port_connections ) - RP )
name_of_instance         << Group( module_instance_identifier + Optional( _range ) )
list_of_port_connections << Group( delimitedList ( ordered_port_connection ) |
                                   delimitedList ( named_port_connection   ) )
ordered_port_connection  << Group( Optional( expression ) )
named_port_connection    << Group( PERIOD - port_identifier - LP + Optional( expression ) - RP )

# A.4.2 Generated instantiation

# A.5 UDP declaration and instantiation
# A.5.1 UDP declaration
# A.5.2 UDP ports
# A.5.3 UDP body
# A.5.4 UDP instantiation

# A.6 Behavioral statements
# A.6.1 Continuous assignment statements
continuous_assign      << Group( ASSIGN + Optional( delay3 ) + list_of_net_assignment )
list_of_net_assignment << Group( delimitedList( net_assignment ) )
net_assignment         << Group( net_lvalue - EQUAL + expression )

# A.6.2 Procedural blocks and assigments
initial_construct      << Group( INITIAL + statement )
always_construct       << Group( ALWAYS  + statement )
blocking_assignment    << Group( variable_lvalue + EQUAL + Optional( delay_or_event_control ) + expression )
nonblocking_assignment << Group( variable_lvalue + NB    + Optional( delay_or_event_control ) + expression )

procedural_continuous_assignments << Group( ASSIGN   + variable_assignment |
                                            DEASSIGN + variable_lvalue     |
                                            FORCE    + variable_assignment |
                                            FORCE    + net_assignment      |
                                            RELEASE  + variable_lvalue     |
                                            RELEASE  + net_lvalue          )

function_blocking_assignment << Group( variable_lvalue - EQUAL + expression )
function_statement_or_null   << Group( function_statement | SEMICOLON )

# A.6.3 Parallel and sequential blocks
function_seq_block  << Group( BEGIN + Optional( COLON + block_identifier + ZeroOrMore( block_item_declaration ) ) +
                              ZeroOrMore( function_statement ) -
                              END )
variable_assignment << Group( variable_lvalue - EQUAL + expression )
par_block           << Group( FORK + Optional( COLON + block_identifier  + ZeroOrMore( block_item_declaration ) ) +
                              ZeroOrMore( statement ) -
                              JOIN )
seq_block           << Group( BEGIN + 
                              Optional( COLON + block_identifier + Group(ZeroOrMore( block_item_declaration ))("item_decls") ) +
                              alias(ZeroOrMore( statement ),"statements") -
                              END )

# A.6.4 Statements
statement << Group( nonblocking_assignment            + SEMICOLON |
                    blocking_assignment               + SEMICOLON |
                    case_statement                                |
                    conditional_statement                         |
                    disable_statement                             |
                    event_trigger                                 |
                    loop_statement                                |
                    par_block                                     |
                    procedural_continuous_assignments - SEMICOLON |
                    procedural_timing_control_statement           |
                    seq_block                                     |
                    system_task_enable                            |
                    task_enable                                   |
                    wait_statement                                )

statement_or_null  << Group(  SEMICOLON | statement  )
function_statement << Group( function_blocking_assignment - SEMICOLON |
                             function_case_statement                  |
                             function_conditional_statement           |
                             function_loop_statement                  |
                             function_seq_block                       |
                             disable_statement                        |
                             system_task_enable                       )

# A.6.5 Timing control statements
delay_control          << Group( SHARP + delay_value | 
                                 SHARP - LP + mintypmax_expression - RP )
delay_or_event_control << Group( delay_control | 
                                 event_control |
                                 REPEAT - LP + expression - RP + event_control )
disable_statement      << Group( DISABLE + hierarchical_task_identifier  - SEMICOLON |
                                 DISABLE + hierarchical_block_identifier - SEMICOLON )
event_control          << Group( AT + event_identifier           |
                                 AT + LP + event_expression - RP |
                                 AT + ASTA                       |
                                 AT + LP - ASTA - RP             )
event_trigger          << Group( TRIG + hierarchical_event_identifier - SEMICOLON )
event_expression       << Group( expression                               |
                                 hierarchical_identifier                  |
                                 POSEDGE + expression                     |
                                 NEGEDGE + expression                     |
                                 event_expression + OR + event_expression |
                                 event_expression + CAMMA + event_expression )

procedural_timing_control_statement << Group( delay_or_event_control + statement_or_null      )
wait_statement                      << Group( WAIT - LP + expression - RP + statement_or_null )

# A.6.6 Conditional statements
conditional_statement << Group( 
    if_else_if_statement
    |
    IF + LP + alias(expression, "condition") + RP + alias(statement_or_null, "statement_if") + 
    Optional( ELSE + alias(statement_or_null,"statement_else") ) )

_else_if_part = Group( ELSE + IF + LP + alias(expression,"condition_elseif") - RP + alias(statement_or_null,"statement_elseif") )
if_else_if_statement << Group( 
    IF + LP + alias(expression,"condition") + RP + alias(statement_or_null,"statement_if") + 
    alias(ZeroOrMore( _else_if_part ), "elseif_blocks") +
    Optional( ELSE + alias(statement_or_null,"statement_else") ) )

function_conditional_statement << Group(
    IF + LP + expression - RP + function_statement_or_null +
    Optional( ELSE + function_statement_or_null )
    |
    function_if_else_if_statement )

function_if_else_if_statement << Group(
    IF + LP + expression - RP + function_statement_or_null +
    ZeroOrMore ( ELSE - IF - LP + expression - RP + function_statement_or_null ) +
    Optional   ( ELSE + function_statement_or_null ) )

# A.6.7 Case statements
case_statement << Group( CASE  - LP + expression - RP + OneOrMore( case_item ) + ENDCASE |
                         CASEZ - LP + expression - RP + OneOrMore( case_item ) + ENDCASE |
                         CASEX - LP + expression - RP + OneOrMore( case_item ) + ENDCASE )
case_item      << Group( delimitedList( expression ) - COLON + statement_or_null |
                         DEFAULT + Optional( COLON ) + statement_or_null         )

function_case_statement << Group( CASE  - LP + expression - RP + OneOrMore (function_case_item ) + ENDCASE |
                                  CASEZ - LP + expression - RP + OneOrMore (function_case_item ) + ENDCASE |
                                  CASEX - LP + expression - RP + OneOrMore (function_case_item ) + ENDCASE )
function_case_item      << Group( delimitedList( expression ) - COLON + function_statement_or_null |
                                  DEFAULT + Optional( COLON ) + function_statement_or_null         )


# A.6.8 Loop statements
function_loop_statement << Group( 
    FOREVER + function_statement                       |
    REPEAT - LP + expression - RP + function_statement |
    WHILE  - LP + expression - RP + function_statement 
    |
    FOR - LP + variable_assignment - SEMICOLON + expression - SEMICOLON + variable_assignment - RP +
    function_statement )

loop_statement << Group(
    FOREVER + statement                       |
    REPEAT - LP + expression - RP + statement |
    WHILE  - LP + expression - RP + statement 
    |
    FOR - LP + alias(variable_assignment,"init") - SEMICOLON + expression - SEMICOLON + alias(variable_assignment,"next") - RP +
    statement )

# A.6.9 Task enable statements
system_task_enable << Group( 
    system_task_identifier + Optional( LP + delimitedList( expression ) - LP ) - SEMICOLON )

task_enable << Group(
    hierarchical_identifier + Optional( LP + delimitedList( expression ) - LP ) - SEMICOLON )

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
concatenation                   << Group( LC + delimitedList( expression )                  - RC )
constant_concatenation          << Group( LC + delimitedList( constant_expression )         - RC )
constant_multiple_concatenation << Group( LC + constant_expression + constant_concatenation - RC )

module_path_concatenation          << Group( LC + delimitedList( module_path_expression )         - RC )
module_path_multiple_concatenation << Group( LC + constant_expression + module_path_concatenation - RC )
multiple_concatenation             << Group( LC + constant_expression + concatenation             - RC )

net_concatenation << Group( LC + delimitedList( net_concatenation_value ) - RC )
net_concatenation_value << Group( 
    hierarchical_net_identifier                                                                  |
    hierarchical_net_identifier + OneOrMore( LB + expression - RB )                              |
    hierarchical_net_identifier + OneOrMore( LB + expression - RB ) + LB + range_expression - RB |
    hierarchical_net_identifier + LB + range_expression - RB                                     |
    net_concatenation )

variable_concatenation << Group( LC + delimitedList( variable_concatenation_value ) - RC )
variable_concatenation_value << Group(
    hierarchical_variable_identifier                                                                  |
    hierarchical_variable_identifier + OneOrMore( LB + expression - RB )                              |
    hierarchical_variable_identifier + OneOrMore( LB + expression - RB ) + LB + range_expression - RB |
    hierarchical_variable_identifier + LB + range_expression - RB                                     |
    variable_concatenation )

# A.8.2 Function calls
constant_function_call << Group( function_identifier - LP + delimitedList( constant_expression )     - RP )
function_call          << Group( hierarchical_function_identifier - LP + delimitedList( expression ) - RP )
system_function_call   << Group( system_task_identifier + Optional( LP + delimitedList( expression ) - RP ) )

# A.8.3 Expressions
base_expression          << expression
conditional_expression   << Group( expression + Q + expression - COLON + expression )
constant_base_expression << constant_expression
constant_expression      << Group( constant_primary                                                            |
                                   unary_operator + constant_primary                                           |
                                   constant_expression + binary_operator + constant_expression                 |
                                   constant_expression + Q + constant_expression - COLON + constant_expression |
                                   string )

constant_mintypmax_expression << Group( 
    constant_expression |
    constant_expression + COLON + constant_expression + COLON + constant_expression )

constant_range_expression     << Group( constant_base_expression + PLUS  + COLON + width_constant_expression |
                                        constant_base_expression + MINUS + COLON + width_constant_expression |
                                        msb_constant_expression + COLON + lsb_constant_expression            |
                                        constant_expression                                                  )

dimension_constant_expression << constant_expression
_expression                    = Group( primary                                   |
                                        string                                    |
                                        unary_operator + primary                  |
                                        conditional_expression                    )
#                                        expression + binary_operator + expression )
expression << operatorPrecedence( _expression, [ (binary_operator, 2, opAssoc.RIGHT) ])

lsb_constant_expression            << constant_expression
msb_constant_expression            << constant_expression
mintypmax_expression               << Group( expression | expression + COLON + expression + COLON + expression )
module_path_conditional_expression << module_path_expression + Q + module_path_expression + COLON + module_path_expression

module_path_expression << Group( module_path_primary                                                           |
                                 unary_module_path_operator + module_path_primary                              |
                                 module_path_expression + binary_module_path_operator + module_path_expression |
                                 module_path_conditional_expression                                            )

module_path_mintypmax_expression << Group( 
    module_path_expression | 
    module_path_expression + COLON + module_path_expression + COLON + module_path_expression )

range_expression << Group( expression                                                  |
                           msb_constant_expression + COLON + lsb_constant_expression   |
                           base_expression + PLUS  + COLON + width_constant_expression |
                           base_expression + MINUS + COLON + width_constant_expression )

width_constant_expression << constant_expression

# A.8.4 Primaries
constant_primary << Group( constant_concatenation                  |
                           constant_function_call                  |
                           LP - constant_mintypmax_expression - RP |
                           constant_multiple_concatenation         |
                           number )

module_path_primary << Group( number                                     |
                              identifier                                 |
                              module_path_concatenation                  |
                              module_path_multiple_concatenation         |
                              function_call                              |
                              system_function_call                       |
                              constant_function_call                     |
                              LP + module_path_mintypmax_expression - RP )

primary << Group( number                                                                                           ^
                  hierarchical_identifier                                                                          ^
                  hierarchical_identifier + OneOrMore( LB + expression + RB )("exps")                              ^
                  hierarchical_identifier + OneOrMore( LB + expression + RB )("exps") + LB + range_expression + LB ^
                  hierarchical_identifier + LB + range_expression - RB                                             ^
                  concatenation                                                                                    ^
                  multiple_concatenation                                                                           ^
                  function_call                                                                                    ^
                  system_function_call                                                                             ^
                  constant_function_call                                                                           ^
                  LP + mintypmax_expression - RP                                                                   )

# A.8.5 Expression left-side value
net_lvalue << Group( hierarchical_net_identifier + alias(OneOrMore( LB + constant_expression + RB ),"exps") + LB + constant_range_expression + RB  |
                     hierarchical_net_identifier + alias(OneOrMore( LB + constant_expression + RB ),"exps")                                        |
                     hierarchical_net_identifier                                                            + LB + constant_range_expression + RB  |
                     net_concatenation                                                                                                             |
                     hierarchical_net_identifier                                                                                                   )

variable_lvalue << Group( hierarchical_variable_identifier + alias(OneOrMore( LB + expression - RB ),"exps") + LB + range_expression - RB  |
                          hierarchical_variable_identifier + alias(OneOrMore( LB + expression - RB ),"exps")                               |
                          hierarchical_variable_identifier                                                    + LB + range_expression - RB |
                          variable_concatenation                                                                                           |
                          hierarchical_variable_identifier                                                                                 )

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

# A.8.8 Strings
string << Suppress("\"") + ZeroOrMore( CharsNotIn("\"\n") ) + Suppress("\"")

# A.9 General
# A.9.1 Attributes
# A.9.2 Comments

# A.9.3 Identifiers

# [ a-zA-Z_ ] { [ a-zA-Z0-9_$ ] }
simple_identifier         << ID  
simple_arrayed_identifier << Group( simple_identifier + Optional( _range ) )

# \ {Any_ASCII_character_except_white_space} white_space
escaped_identifier         << simple_identifier # temp
escaped_arrayed_identifier << Group( escaped_identifier + Optional( _range ) )

identifier                 << Group( simple_identifier         | escaped_identifier         )
arrayed_identifier         << Group( simple_arrayed_identifier | escaped_arrayed_identifier ) 

event_identifier           << identifier
function_identifier        << identifier
module_identifier          << identifier
module_instance_identifier << arrayed_identifier 
net_identifier             << identifier
port_identifier            << identifier
real_identifier            << identifier
task_identifier            << identifier
variable_identifier        << identifier

hierarchical_identifier         << Group( simple_hierarchical_identifier | escaped_hierarchical_identifier )
simple_hierarchical_identifier  << Group( simple_hierarchical_branch + Optional( PERIOD + escaped_identifier ) )

escaped_hierarchical_identifier << Group( 
    escaped_hierarchical_branch + ZeroOrMore( 
        PERIOD + simple_hierarchical_branch ^ PERIOD + escaped_hierarchical_branch ) )

    
_simple_hierarchical_branch_part = Group( PERIOD + simple_identifier("name") + Optional( LB + unsigned_number("index") + RB ) )
simple_hierarchical_branch  << Group(
    simple_identifier
    + Optional( LB + unsigned_number("index") + RB )
    + Group( Optional( ZeroOrMore( _simple_hierarchical_branch_part ) ) ) ("ids")
    )

escaped_hierarchical_branch << Group(
    escaped_identifier + Optional( LB + unsigned_number + RB ) + Optional(
        ZeroOrMore( PERIOD + escaped_identifier + Optional( LB + unsigned_number + RB ) ) ) )

hierarchical_block_identifier    << hierarchical_identifier
hierarchical_event_identifier    << hierarchical_identifier
hierarchical_function_identifier << hierarchical_identifier
hierarchical_net_identifier      << hierarchical_identifier
hierarchical_variable_identifier << hierarchical_identifier
hierarchical_task_identifier     << hierarchical_identifier

system_task_identifier << Regex(r"$[a-zA-Z0-9_$][a-zA-Z0-9_$]*")

