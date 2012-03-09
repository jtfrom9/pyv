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
                       | empty
        '''

    def p_module_body_empty(self,p):
        '''module_body : '''


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
                | empty
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
        '''input_declaration : input signed_oe range_oe ids
        '''
        
    def p_output_declaration(self,p):
        '''output_declaration : output signed_oe range_oe ids
        '''
        
    def p_inout_declaration(self,p):
        '''inout_declaration : output signed_oe range_oe ids
        '''

    def p_signed_oe(self,p):
        '''signed_oe : empty
        '''

    def p_range_oe(self,p):
        '''range_oe : range
                          | empty
        '''


class Variables:
    def p_ids(self,p):
        '''ids : ID ',' ids
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
        '''reg_declaration : reg range_oe vars 
        '''

    def p_integer_declaration(self,p):
        '''integer_declaration : integer vars
        '''

    def p_net_declaration(self,p):
        '''net_declaration : nettype expandrange_oe delay_oe vars
        '''

    def p_nettype(self,p):
        '''nettype : wire
        '''

    def p_expandrange_oe(self,p):
        '''expandrange_oe : expandrange
                                | empty
        '''

    def p_expandrange(self,p):
        '''expandrange : range
        '''

    def p_delay_oe(self,p):
        '''delay_oe : delay
                    | empty
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
                      | unary_operator primary
                      | expression binary_operator expression
                      | STRING
        '''

    def p_unary_operator(self,p):
        '''unary_operator : '+'
                          | '-'
        '''

    def p_binary_operator(self,p):
        '''binary_operator : '+'
                           | '-'
                           | '*'
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
                        | empty
        '''
        
    def p_statement(self,p):
        '''statement : blocking_assignment
                     | nonblocking_assignment
                     | if '(' expression ')' statement_oe
                     | seq_block
                     | assign assignment
        '''

    def p_statements(self,p):
        '''statements : statement statements
                      | statement
        '''
        
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
                              | empty
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
        '''function_call : ID 
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
