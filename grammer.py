# -*- coding: utf-8 -*-

class Module:
    #A.1.3 Module and primitive source text
    def p_soruce_text(self,p):
        '''source_text : description source_text
                       | description
                       |
        '''
        
    def p_description(self,p):
        '''description : module_declaration
                       | interface_declaration
                       | program_declaration
                       | package_declaration
        '''

    def p_module_ansi_header(self,p):
        '''module_ansi_header : module ID opt_parameter_port_list list_of_port_declarations ';'
                              | module ID opt_parameter_port_list ';'
        '''
        print 'ID=',p[2], ' port_decls=',p[4]

    def p_module_declaration(self,p):
        '''module_declaration : module_ansi_header             non_port_module_items endmodule
        '''
        pass
    
#                              | module ID '(' DOTASTA ')' ';'  module_items          endmodule  

    def p_interface_declaration(self,p):
        '''interface_declaration : NOTDEFINED'''
        pass

    def p_program_declaration(self,p):
        '''program_declaration : NOTDEFINED'''
        pass

    def p_package_declaration(self,p):
        '''package_declaration : NOTDEFINED'''
        pass


    #A.1.4 Module parameters and ports
    def p_opt_parameter_port_list(self,p):
        '''opt_parameter_port_list : parameter_port_list
                                   |
                                   '''
        pass

    def p_parameter_port_list(self,p):
        '''parameter_port_list : NOTDEFINED'''
        pass


    def p_list_of_ports(self,p):
        '''list_of_ports : '(' port opt_ports ')'
        '''
        pass

    def p_opt_ports(self,p):
        '''opt_ports : ',' port opt_ports
                     | ',' port 
        '''
    
    def p_list_of_port_declarations(self,p):
        '''list_of_port_declarations : '(' ansi_port_declaration opt_ansi_port_declarations ')'
        '''
        #p[0] = p[2] + p[3]
        print "# ", p[2],' #',p[3]
        p[0] = [p[2]] + p[3]
    
    
    def p_port_declaration(self,p):
        '''port_declaration : inout_declaration
                            | input_declaration
                            | output_declaration
                            | ref_declaration
                            | interface_port_declaration
                            '''
        pass


    def p_port(self,p):
        '''port : port_expression
                | '.' ID '(' port_expression ')'
        '''
        pass

    def p_port_expression(self,p):
        '''port_expression : port_reference
                           | port_reference ',' port_expression
                           |
        '''
        pass

    def p_port_reference(self,p):
        '''port_reference : ID constant_select'''
        pass
    
    def p_port_direction(self,p):
        '''port_direction : input
                          | output
                          | inout
                          | ref
                          '''
        pass
    
    def p_net_port_header(self,p):
        '''net_port_header : port_direction port_type
                           |                port_type
        '''
        pass

    def p_variable_port_header(self,p):
        '''variable_port_header : port_direction data_type
                                |                data_type
        '''
        pass

    def p_interface_port_header(self,p):
        '''interface_port_header : NOTDEFINED'''
        pass

    def p_opt_ansi_port_declarations(self,p):
        '''opt_ansi_port_declarations : ',' ansi_port_declaration opt_ansi_port_declarations
                                      | ',' ansi_port_declaration
                                      '''
        #p[0] = p[2] + p[3]
        print 'len(p)=',len(p)
        if len(p)==4:
            print 'p[2]=',p[2],', p[3]=',p[3]
            p[0] = [p[2]] + p[3]
        else:
            print 'p[2]=',p[2]
            p[0] = [ p[2] ]

    def p_ansi_port_declaration(self,p):
        '''ansi_port_declaration : net_port_header       ID opt_unpacked_dimensions
                                 | interface_port_header ID opt_unpacked_dimensions
                                 |                       ID opt_unpacked_dimensions
                                 | variable_port_header  ID variable_dimension opt_default_constant_expression
                                 |                       ID variable_dimension opt_default_constant_expression
                                 | net_port_header      '.' ID '(' opt_expression ')'
                                 | variable_port_header '.' ID '(' opt_expression ')'
                                 |                      '.' ID '(' opt_expression ')'
        '''
        p[0] = p[1]

    def p_opt_default_constant_expression(self,p):
        '''opt_default_constant_expression : '=' constant_expression
                                           |
        '''
        pass


class ModuleItem:
    def p_module_items(self,p):
        '''module_items : module_item module_items
                        | module_item
        '''
        pass
    
    def p_module_common_item(self,p):
        '''module_common_item : module_or_generate_item_declaration
                              | interface_instantiation
                              | program_instantiation
                              | concurrent_assertion_item
                              | bind_directive
                              | continuous_assign
                              | net_alias
                              | initial_construct
                              | final_construct
                              | always_construct
        '''
    
    def p_module_item(self,p):
        '''module_item : port_declaration ';'
                       | non_port_module_item
                       '''
        pass

    def p_module_or_generate_item(self,p):
        '''module_or_generate_item : parameter_override
                                   | module_instantiation
                                   | module_common_item
                                   '''
        pass

    def p_module_or_generate_item_declaration(self,p):
        '''module_or_generate_item_declaration : package_or_generate_item_declaration
                                               '''
        pass

    def p_non_port_module_items(self,p):
        '''non_port_module_items : non_port_module_item non_port_module_items
                                 | non_port_module_item
                                 |
        '''
        
    def p_non_port_module_item(self,p):
        '''non_port_module_item : module_or_generate_item
        '''
        pass

    def p_program_instantiation(self,p):
        '''program_instantiation : NOTDEFINED'''
        pass

    def p_concurrent_assertion_item(self,p):
        '''concurrent_assertion_item : NOTDEFINED'''
        pass

    def p_bind_directive(self,p):
        '''bind_directive : NOTDEFINED'''
        pass

    def p_net_alias(self,p):
        '''net_alias : NOTDEFINED'''
        pass

    def p_final_construct(self,p):
        '''final_construct : NOTDEFINED'''
        pass

    def p_interface_instantiation(self,p):
        '''interface_instantiation : NOTDEFINED'''
        pass
    
    def p_parameter_override(self,p):
        '''parameter_override : NOTDEFINED'''
        pass

    def p_continuous_assign(self,p):
        '''continuous_assign : NOTDEFINED'''
        pass


    def p_package_or_generate_item_declaration(self,p):
        '''package_or_generate_item_declaration : net_declaration
                                                | data_declaration
                                                | task_declaration
                                                | function_declaration
         '''
        pass

    
class ModuleInstance:
    def p_module_instantiation(self,p):
        '''module_instantiation : ID opt_parameter_value_assignment hierarchical_instances
        '''
        pass

    def p_opt_parameter_value_assignment(self,p):
        '''opt_parameter_value_assignment : parameter_value_assignment
                                          |
        '''
        pass

    def p_parameter_value_assignment(self,p):
        '''parameter_value_assignment : '''
        pass
    
    def p_hierarchical_instances(self,p):
        '''hierarchical_instances : hierarchical_instance ',' hierarchical_instances
                                  | hierarchical_instance
        '''
        pass

    def p_hierarchical_instance(self,p):
        '''hierarchical_instance : name_of_instance '(' list_of_port_connections ')'
                                 | name_of_instance '('                          ')'
        '''
        pass

    def p_name_of_instance(self,p):
        '''name_of_instance : ID opt_unpacked_dimensions
        '''
        pass


    def p_list_of_port_connections(self,p):
        '''list_of_port_connections : ordered_port_connections
                                    | named_port_connections
        '''
        pass

    def p_ordered_port_connections(self,p):
        '''ordered_port_connections : ordered_port_connection ',' ordered_port_connections
                                    | ordered_port_connection
        '''
        pass

    def p_ordered_port_connection(self,p):
        '''ordered_port_connection : expression
        '''
        pass
    
    def p_named_port_connections(self,p):
        '''named_port_connections : named_port_connection ',' named_port_connections
                                  | named_port_connection
                                  '''
        pass

    def p_named_port_connection(self,p):
        '''named_port_connection : '.' ID '(' expression ')'
                                 | '.' ID
                                 | DOTASTA
        '''
        pass

        
class Declaration:
    #A.2.1.1 Module parameter declarations
    
    #A.2.1.2 Port declarations
    def p_inout_declaration(self,p):
        '''inout_declaration : inout port_type list_of_port_identifiers'''
        pass

    def p_input_declaration(self,p):
        '''input_declaration : input port_type list_of_port_identifiers
                             | input data_type list_of_variable_identifiers
                             '''
        pass

    def p_output_declaration(self,p):
        '''output_declaration : output port_type list_of_port_identifiers
                              | output data_type list_of_variable_identifiers
        '''
        pass

    def p_interface_port_declaration(self,p):
        '''interface_port_declaration : ID        list_of_interface_identifiers
                                      | ID '.' ID list_of_interface_identifiers
        '''
        pass

    def p_ref_declaration(self,p):
        '''ref_declaration : ref data_type list_of_port_identifiers
        '''
        pass

    #A.2.1.3 Type declarations
    def p_data_declaration(self,p):
        '''data_declaration : NOTDEFINED'''
        pass

    def p_net_declaration(self,p):
        '''net_declaration : NOTDEFINED'''
        pass

    #A.2.2.1 Net and variable types
    def p_data_type(self,p):
        '''data_type : NOTDEFINED'''
        pass
        
    def p_net_type(self,p):
        '''net_type : wire'''
        pass
    
    def p_port_type(self,p):
        '''port_type : net_type_or_trireg opt_signing opt_packed_dimensions'''
        pass

    def p_net_type_or_trireg(self,p):
        '''net_type_or_trireg : net_type
        '''
        pass
    
    def p_opt_signing(self,p):
        '''opt_signing : signing
                       |'''
        pass

    def p_signing(self,p):
        '''signing : signed
                   | unsigned
        '''
        pass

    
    #A.2.3 Declaration lists
    def p_list_of_interface_identifiers(self,p):
        '''list_of_interface_identifiers : ID opt_unpacked_dimensions ',' list_of_interface_identifiers
                                         | ID opt_unpacked_dimensions 
        '''
        pass
    
    def p_list_of_net_identifiers(self,p):
        '''list_of_net_identifiers : ID opt_unpacked_dimensions ',' list_of_net_identifiers
                                   | ID opt_unpacked_dimensions 
        '''
        pass
    
    def p_list_of_port_identifiers(self,p):
        '''list_of_port_identifiers : ID opt_unpacked_dimensions ',' list_of_port_identifiers
                                    | ID opt_unpacked_dimensions
        '''
        pass

    def p_list_of_variable_identifiers(self,p):
        '''list_of_variable_identifiers : ID variable_dimension ',' list_of_variable_identifiers
                                        | ID variable_dimension 
        '''
        pass
    
    #A.2.4 Declaration assignments
    def p_variable_dimension(self,p):
        '''variable_dimension : NOTDEFINED'''
        pass
    
    #A.2.5 Declaration ranges
    def p_opt_unpacked_dimensions(self,p):
        '''opt_unpacked_dimensions : unpacked_dimension opt_unpacked_dimensions
                                   |
        '''
        pass
    
    def p_unpacked_dimension(self,p):
        '''unpacked_dimension : '[' constant_range ']'
                              | '[' constant_expression ']'
        '''
        pass

    def p_packed_dimension(self,p):
        '''packed_dimension : '[' constant_range ']'
        '''
        pass

    def p_opt_packed_dimensions(self,p):
        '''opt_packed_dimensions : packed_dimension opt_packed_dimensions
                                 |
        '''
        pass
    
    #A.2.6 Function declarations
    def p_function_declaration(self,p):
        '''function_declaration : NOTDEFINED'''
        pass

    #A.2.7 Task declarations
    def p_task_declaration(self,p):
        '''task_declaration : NOTDEFINED'''
        pass



    
class BehavioralStatement:
    def p_initial_construct(self,p):
        '''initial_construct : NOTDEFINED'''
        pass

    def p_always_construct(self,p):
        '''always_construct : NOTDEFINED'''
        pass

    
class Expression:
    #A.8.3 Expressions
    def p_constant_expression(self,p):
        '''constant_expression : constant_primary
                               | unary_operator constant_primary
                               | constant_expression binary_operator constant_expression
                               | constant_expression '?' constant_expression ':' constant_expression
                               '''
        pass

    def p_constant_range(self,p):
        '''constant_range : constant_expression ':' constant_expression'''
        pass

    def p_opt_expression(self,p):
        '''opt_expression : expression
                          |
        '''
        pass
    
    def p_expression(self,p):
        '''expression : NOTDEFINED'''
        pass

    #A.8.4 Primaries
    def p_constant_primary(self,p):
        '''constant_primary : NOTDEFINED'''
        pass

    def p_constant_select(self,p):
        '''constant_select : NOTDEFINED
        '''

    #A.8.5 Expression left-side values
    #A.8.6 Operators
    def p_unary_operator(self,p):
        '''unary_operator : NOTDEFINED'''
        pass
    
    def p_binary_operator(self,p):
        '''binary_operator : NOTDEFINED'''
        pass

        
