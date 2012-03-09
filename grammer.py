

class Module:
    def p_module_declaration(self,p):
        '''module_declaration : begin_module module_body endmodule
        '''

    def p_beginmodule_ports(self,p):
        '''begin_module : module ID ports_list ';'
        '''

    def p_beginmodule(self,p):
        '''begin_module : module ID ';'
        '''

    def p_module_body(self,p):
        '''module_body : variables_declaration module_body
                       | module_instantiation  module_body
                       | task_declaration      module_body 
                       | initial_block         module_body 
        '''
        
    def p_module_body_empty(self,p):
        '''module_body : '''

        
class Port:
    def p_ports_list_recur(self,p):
        '''ports_list : '(' port ',' ports_list ')'
        '''

    def p_ports_list_single(self,p):
        '''ports_list : '(' port ')'
        '''
        
    def p_ports_list_empty(self,p):
        '''ports_list : '(' ')'
        '''

    def p_port(self,p):
        '''port : port_type ID
        '''

    def p_port_simple(self,p):
        '''port : ID
        '''
        
    def p_port_type_range(self,p):
        '''port_type : direction range'''

    def p_port_type(self,p):
        '''port_type : direction '''

    def p_direction(self,p):
        '''direction : input
                     | output
                     | inout'''


class Variables:
    def p_range(self,p):
        '''range : '[' NUM ':' NUM ']' '''
        

        
class Task:
    def p_task_declaration(self,p):
        '''task_declaration : begin_task task_body endtask
        '''

    def p_begin_task(self,p):
        '''begin_task : task ID ports_list ';'
        '''

    def p_task_body(self,p):
        '''task_body : variables_declaration task_body
                     | initial_block         task_body
                     '''

    def p_task_body_null(self,p):
        '''task_body : '''

    
