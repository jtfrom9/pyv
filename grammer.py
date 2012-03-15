# -*- coding: utf-8 -*-

class Module:
    def p_module_definition(self,p):
        '''module_definition : begin_module module_body endmodule
        '''

    def p_begin_module(self,p):
        '''begin_module : module ID ports_list ';'
                        | module ID ';'
        '''

    def p_module_body(self,p):
        '''module_body : module_item module_body
                       | 
        '''


class ModuleItem:
    def p_module_item(self,p):
        '''module_item : input_declaration
                       | output_declaration
                       | inout_declaration
                       | reg_declaration
                       | net_declaration
                       | integer_declaration
                       | initial_statemnt
                       | always_statement
                       | task_definition
                       | function_definition
        '''

        
class Port:
    def p_ports_list(self,p):
        '''ports_list : '(' ports ')'
        '''

    def p_ports(self,p):
        '''ports : port ',' ports
                 | port
        '''
        
    def p_port(self,p):
        '''port : port_expression
                | 
                '''

    def p_port_specified(self,p):
        '''port : '.' ID '(' port_expression ')'
                | '.' ID '('                 ')'
        '''

    def p_port_direction(self,p):
        '''port : input_declaration
                | output_declaration
                | inout_declaration
        '''

    def p_port_expression(self,p):
        '''port_expression : port_reference
                           | '{' port_reference ',' port_references '}'
                           | '{' port_reference                     '}'
        '''

    def p_port_references(self,p):
        '''port_references : port_reference port_references
                           | port_reference
        '''
        
    def p_port_reference(self,p):
        '''port_reference : ID
                          | ID '[' constant_expression                          ']'
                          | ID '[' constant_expression ':' constant_expression  ']'
        '''

    def p_input_declaration(self,p):
        '''input_declaration : input signed_oe range_oe ids %prec INPUT_DECL
        '''
        
    def p_output_declaration(self,p):
        '''output_declaration : output signed_oe range_oe ids %prec OUTPUT_DECL
        '''
        
    def p_inout_declaration(self,p):
        '''inout_declaration : inout signed_oe range_oe ids %prec INOUT_DECL
        '''

    def p_signed_oe(self,p):
        '''signed_oe : 
        '''

    def p_range_oe(self,p):
        '''range_oe : range
                    | 
        '''


class Variables:
    def p_ids(self,p):
        '''ids : ids ',' ID %prec IDS
               | ID
        '''

    def p_var(self,p):
        '''var : ID
               | ID '[' constant_expression ':' constant_expression ']'
        '''
        
    def p_vars(self,p):
        '''vars : var ',' vars
                | var
        '''
        
    def p_reg_declaration(self,p):
        '''reg_declaration : reg range_oe vars ';'
        '''

    def p_integer_declaration(self,p):
        '''integer_declaration : integer vars ';'
        '''

    def p_net_declaration(self,p):
        '''net_declaration : nettype expandrange_oe delay_oe vars ';'
        '''

    def p_nettype(self,p):
        '''nettype : wire
        '''

    def p_expandrange_oe(self,p):
        '''expandrange_oe : expandrange
                          | 
        '''

    def p_expandrange(self,p):
        '''expandrange : range
        '''

    def p_delay_oe(self,p):
        '''delay_oe : delay
                    | 
        '''

    def p_delay(self,p):
        '''delay : '#' number
                 | '#' ID
        '''
        
class Expression:
    def p_number(self,p):
        '''number : NUM
        '''
        
    def p_constant_expression(self,p):
        '''constant_expression : expression
        '''
        
    def p_range(self,p):
        '''range : '[' constant_expression ':' constant_expression ']'
        '''

    def p_expression(self,p):
        '''expression : primary
                      | unary_expression   
                      | binary_expression
                      | STRING
        '''

    def p_binary_expression(self,p):
        '''binary_expression : expression '+' expression
                             | expression '-' expression
                             | expression '*' expression
        '''

    def p_unary_expression(self,p):
        '''unary_expression : '+' primary  %prec UNARY
                            | '-' primary  %prec UNARY
        '''

    def p_primary(self,p):
        '''primary : number
                   | ID
                   | ID '[' expression ']'
                   | ID '[' constant_expression ':' constant_expression ']'
                   | function_call
        '''

    def p_lvalue(self,p):
        '''lvalue : ID
                  | ID '[' expression ']'
                  | ID '[' constant_expression ':' constant_expression ']'
        '''
        
class Statement:
    def p_statement_oe(self,p):
        '''statement_oe : statement 
                        |              %prec NULL_STATEMENT
        '''
        
    def p_statement(self,p):
        '''statement : conditional_statement
                     | blocking_assignment
                     | nonblocking_assignment
                     | seq_block
                     | assign assignment          
                     | procedural_timing_control_statement
        '''

    def p_statements(self,p):
        '''statements : statement statements
                      | statement
        '''


#     def p_conditional_statement(self,p):
#         '''conditional_statement : if '(' expression ')' wo_if_statement 
#                                  | if '(' expression ')' conditional_statement
#                                  | if '(' expression ')' wo_if_statement else statement
#                                  | if '(' expression ')' conditional_statement     else statement
#         '''
        
#     def p_conditional_statement(self,p):
#         '''conditional_statement : conditional_statement_if
#                                  | conditional_statement_ifelse
#         '''
#     def p_conditional_statement_if(self,p):
#         '''conditional_statement_if : if '(' expression ')' statement
#         '''
        
#     def p_conditional_statement_ifelse(self,p):
#         '''conditional_statement_ifelse : if '(' expression ')' wo_if_statement else statement
#         '''


    def p_conditional_statement(self,p):
        '''conditional_statement : if '(' expression ')' wo_if_statement else statement
                                 | if '(' expression ')' statement
        '''
        
    def p_wo_if_statement(self,p):
        '''wo_if_statement : blocking_assignment
                           | nonblocking_assignment
                           | seq_block
                           | assign assignment
        '''
        # この方が正確。 if-elseはshift/reduce conflictが発生しても仕方ない
#     def p_conditional_statement(self,p):
#         '''conditional_statement : if '(' expression ')' statement else statement
#                                  | if '(' expression ')' statement
#         '''
        
    def p_assignment(self,p):
        '''assignment : lvalue '=' expression
        '''
    
    def p_blocking_assignment(self,p):
        '''blocking_assignment : lvalue '=' expression
        '''
    
    def p_nonblocking_assignment(self,p):
        '''nonblocking_assignment : lvalue NB_ASIGN expression
        '''
    def p_seq_block(self,p):
        '''seq_block : begin statements end
        '''
    def p_initial_statement(self,p):
        '''initial_statemnt : initial statement
        '''

    def p_always_statement(self,p):
        '''always_statement : always statement
        '''

    def p_procedural_timing_control_statement(self,p):
        '''procedural_timing_control_statement : procedural_timing_control statement_oe
        '''

    def p_procedural_timing_control(self,p):
        '''procedural_timing_control : delay_control
                                     | event_control
                                     '''

    def p_event_control(self,p):
        '''event_control : '@' ID
                         | '@' '(' event_expression ')'
                         | AT_ASTA
                         | '@' '(' '*' ')'
                         '''

    def p_delay_control(self,p):
        '''delay_control : '#' delay_value
        '''

    def p_delay_value(self,p):
        '''delay_value : NUM '''

    def p_event_expression(self,p):
        '''event_expression : expression
                            | posedge expression
                            | negedge expression
                            | event_expression or event_expression
                            | event_expression ',' event_expression
                            '''

class TaskAndFunction:
    def p_function_definition(self,p):
        '''function_definition : begin_function statement endfunction
        '''
        pass

    def p_begin_function(self,p):
        '''begin_function : function range_oe ID ports_list ';'
                          | function range_oe ID            ';' tf_declarations
        '''
        
    def p_tf_declarations(self,p):
        '''tf_declarations : tf_declaration tf_declarations
                           | tf_declaration
        '''

    def p_tf_declarations_oe(self,p):
        '''tf_declarations_oe : tf_declarations
                              | 
        '''

    def p_tf_declaration(self,p):
        '''tf_declaration : input_declaration
                          | reg_declaration
                          | integer_declaration
        '''
        
    def p_task_definition(self,p):
        '''task_definition : begin_task statement_oe endtask
        '''

    def p_begin_task(self,p):
        '''begin_task : task ID ports_list ';'
                      | task ID            ';' tf_declarations_oe
        '''
    
    # まだmoduleのインスタンス化を書いてないので一旦おいておく
    def p_function_call(self,p):
        '''function_call : ID '(' ')'
        '''
        pass




       
    
# class ModuleInstance:
#     def p_module_instantiation(self,p):
#         '''module_instantiation : ID parameter_value_assignment ID port_connections ';'
#         '''

#     def p_parameter_value_assignment(self,p):
#         '''parameter_value_assignment : '''

#     def p_instantiation_parameters_recur(self,p):
#         '''instantiation_parameters : instantiation_parameter ',' instantiation_parameters
#         '''

#     def p_instantiation_parameters(self,p):
#         '''instantiation_parameters : instantiation_parameter
#         '''
        
#     def p_instantiation_parameters_null(self,p):
#         '''instantiation_parameters : 
#         '''
