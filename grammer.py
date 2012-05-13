# -*- coding: utf-8 -*-

class Top:
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

    def p_interface_declaration(self,p):
        '''interface_declaration : NOTDEFINED'''
        pass

    def p_program_declaration(self,p):
        '''program_declaration : NOTDEFINED'''
        pass

    def p_package_declaration(self,p):
        '''package_declaration : NOTDEFINED'''
        pass

    
class Module:
    def p_module_ansi_header(self,p):
        '''module_ansi_header : module ID opt_parameter_port_list opt_list_of_port_declarations ';'
        '''
        pass

    def p_module_declaration(self,p):
        '''module_declaration : module_ansi_header             non_port_module_items endmodule
                              | module ID '(' DOTASTA ')' ';'  module_items          endmodule  
        '''
        pass
    
    def p_opt_parameter_port_list(self,p):
        '''opt_parameter_port_list : parameter_port_list
                                   |
                                   '''
        pass

    def p_parameter_port_list(self,p):
        '''parameter_port_list : NOTDEFINED'''
        pass

    def p_opt_list_of_port_declarations(self,p):
        '''opt_list_of_port_declarations : NOTDEFINED'''
        pass

    def p_port_declaration(self,p):
        '''port_declaration : NOTDEFINED'''
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
    def p_net_declaration(self,p):
        '''net_declaration : NOTDEFINED'''
        pass
    
    def p_task_declaration(self,p):
        '''task_declaration : NOTDEFINED'''
        pass

    def p_function_declaration(self,p):
        '''function_declaration : NOTDEFINED'''
        pass

    def p_data_declaration(self,p):
        '''data_declaration : NOTDEFINED'''
        pass

    def p_opt_unpacked_dimensions(self,p):
        '''opt_unpacked_dimensions : unpacked_dimension
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

    
class BehavioralStatement:
    def p_initial_construct(self,p):
        '''initial_construct : NOTDEFINED'''
        pass

    def p_always_construct(self,p):
        '''always_construct : NOTDEFINED'''
        pass
    
class Expression:
    def p_expression(self,p):
        '''expression : NOTDEFINED'''
        pass

    def p_constant_range(self,p):
        '''constant_range : constant_expression ':' constant_expression'''
        pass

    def p_constant_expression(self,p):
        '''constant_expression : constant_primary
                               | unary_operator constant_primary
                               | constant_expression binary_operator constant_expression
                               | constant_expression '?' constant_expression ':' constant_expression
                               '''
        pass

    def p_constant_primary(self,p):
        '''constant_primary : NOTDEFINED'''
        pass


    def p_binary_operator(self,p):
        '''binary_operator : NOTDEFINED'''
        pass

    def p_unary_operator(self,p):
        '''unary_operator : NOTDEFINED'''
        pass
        
    
