# -*- coding: utf-8 -*-
import sys
from pyparsing import *

self = sys.modules[__name__]

with open("keywords.txt","r") as f:
    _keywords = [line.strip() for line in f]

ID = ~MatchFirst([Keyword(w) for w in _keywords]) + Word(alphas, alphanums+'_')("id")
LP,RP,LB,RB,LC,RC,COLON,SEMICOLON,CAMMA,PERIOD,SHARP,EQUAL = map(Suppress,("()[]{}:;,.#="))

#LP/RP : left/right paren          ()
#LB/RB : left/right bracket        []
#LC/RC : left/right curly bracket  {}

for kw in _keywords:
    setattr(self, kw.swapcase(), Keyword(kw)("keyword"))

with open("non_terminal_symbols.txt","r") as f:
    for sym in (line.strip() for line in f):
        setattr(self, sym, Forward()(sym))

# A.1 Source text
# A.1.1 Library source text
# A.1.2 Configuration source text

# A.1.3 Module and primitive source text
source_text << ZeroOrMore( description )
description << Group ( module_declaration )

module_declaration << Group (  
    MODULE + ID + Optional( module_parameter_port_list ) + Optional( list_of_ports ) + SEMICOLON + 
    ZeroOrMore( module_item ) + 
    ENDMODULE
    | 
    MODULE + ID + Optional( module_parameter_port_list ) + Optional( list_of_port_declarations) + SEMICOLON + 
    ZeroOrMore( non_port_module_item ) + 
    ENDMODULE )
    
# A.1.4 Module parametersand ports
#module_parameter_port_list << SHARP + LP parameter
list_of_ports              << LP + delimitedList( port ) + RP
list_of_port_declarations  << Group( LP + delimitedList( port_declaration ) + RP | 
                                     LP + RP  )
                                     
port             << Group( Optional( port_expression ) | 
                           PERIOD + ID + LP + Optional( port_expression ) + RP )
port_expression  << Group( port_reference | LC + delimitedList( port_reference ) + RC )
port_reference   << Group( ID                                 |
                           ID + LB + constant_expression + RB |
                           ID + LB + range_expression +  RB   )
port_declaration << Group ( inout_declaration | 
                            input_declaration | 
                            output_declaration )

# A.1.5 Module items
module_item                         << Group( module_or_generate_item | 
                                              port_declaration  )

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

non_port_module_item                << Group( module_or_generate_item )
 

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
real_type            << Group( ID + Optional( EQUAL + constant_expression ) |
                               ID + dimension + ZeroOrMore ( dimension ) )
variable_type        << Group( ID + Optional( EQUAL + constant_expression ) | 
                               ID + dimension + ZeroOrMore ( dimension ) )

# A.2.2.2 Strenghths

# A.2.2.3 Delays
delay3      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value + Optional ( CAMMA + delay_value ) ) + RP )
delay2      << Group( SHARP + delay_value | 
                      SHARP + LP + delay_value + Optional( CAMMA + delay_value ) + RP )
delay_value << Group( unsigned_number | mintypmax_expression )

# A.2.3 Declaration lists
list_of_event_identifiers        << Group(delimitedList( ID + Optional( dimension + ZeroOrMore(dimension) ) ))
list_of_net_decl_assignments     << Group(delimitedList( net_decl_assignment                                ))
list_of_net_identifiers          << Group(delimitedList( ID + Optional( dimension + ZeroOrMore(dimension) ) ))
list_of_port_identifers          << Group(delimitedList( ID                                                 ))
list_of_real_identifiers         << Group(delimitedList( real_type                                          ))
list_of_variable_identifiers     << Group(delimitedList( variable_type                                      ))
list_of_variable_port_identifers << Group(delimitedList( ID + Optional( EQUAL + constant_expression )       ))

# A.2.4 Declaration assignments
net_decl_assignment << Group( ID + EQUAL + expression )

# A.2.5 Declaration ranges
dimension << LB + dimension_constant_expression + COLON + dimension_constant_expression + RB
_range    << LB + msb_constant_expression       + COLON + lsb_constant_expression       + RB

# A.2.6 Function declarations
function_declaration << Group( 
    FUNCTION + Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + ID + SEMICOLON + 
    function_item_declaration + ZeroOrMore( function_item_declaration ) + 
    function_statement + 
    ENDFUNCTION
    |
    FUNCTION + Optional(AUTOMATIC) + Optional(SIGNED) + Optional(range_or_type) + ID + LP + function_port_list + RP + SEMICOLON + 
    block_item_declaration + ZeroOrMore(block_item_declaration) + 
    function_statement + 
    ENDFUNCTION
    )

function_item_declaration << Group( block_item_declaration | tf_input_declaration + SEMICOLON )
function_port_list        << Group( tf_input_declaration + ZeroOrMore( CAMMA + tf_input_declaration ) )
range_or_type             << Group( _range | INTEGER | REAL | REALTIME | TIME )

# A.2.7 Task declarations
task_declaration << Group( 
    TASK + Optional(AUTOMATIC) + ID + SEMICOLON + 
    ZeroOrMore( task_item_declaration ) + 
    statement + 
    ENDTASK
    |
    TASK + Optional(AUTOMATIC) + ID + LP + task_port_list + RP + SEMICOLON + 
    ZeroOrMore( block_item_declaration ) + 
    statement + 
    ENDTASK )

task_item_declaration << Group( block_item_declaration | tf_input_declaration | tf_output_declaration | tf_inout_declaration )
task_port_list        << Group( delimitedList( task_port_item ) )
task_port_item        << Group( tf_inout_declaration | tf_output_declaration | tf_inout_declaration )

tf_input_declaration <<  Group( 
    INPUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers | 
    INPUT + Optional(task_port_type) + list_of_port_identifers )

tf_output_declaration <<  Group( 
    OUTPUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers | 
    OUTPUT + Optional(task_port_type) + list_of_port_identifers )

tf_inout_declaration <<  Group( 
    INOUT + Optional(REG) + Optional(SIGNED) + Optional(_range) + list_of_port_identifers | 
    INOUT + Optional(task_port_type) + list_of_port_identifers )

task_port_type << Group( TIME | INTEGER )

#A.2.8 Block item declarations
block_item_declaration << Group( 
    block_reg_declaration |
    event_declaration     | 
    integer_declaration   | 
    real_declaration      |
    realtime_declaration  |
    time_declaration )

block_reg_declaration              << Group( REG + Optional(SIGNED) + Optional(_range) + list_of_block_variable_identifiers + SEMICOLON )
list_of_block_variable_identifiers << Group( delimitedList( block_variable_type ) )
block_variable_type                << Group( ID | ID + dimension + ZeroOrMore(dimension) )

# A.3 Primitive instances
# A.4 Module and generated instantiation

#A.6.4 Statements

#A.8.7 Numbers

# temp
constant_expression << ID("constant_expression")
range_expression    << ID("range_expression")
statement           << Group( delimitedList(ID) )("statement")


file = '''
module hoge ( a,b, c, d  , e );
wire a,b;
wire x,y;
integer A;
reg foo;

task foo;
a
endtask

endmodule
'''

def main():
    result = source_text.parseString(file)
    if result:
        print(result.asXML())
    else:
        print("error")

if __name__=='__main__':
    main()
