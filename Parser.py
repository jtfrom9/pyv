import ply.lex as lex
import ply.yacc as yacc

import grammer

class Parser(grammer.Module, grammer.Port, grammer.Variables, grammer.Task):
    # reserved words
    reserved = ('module', 'endmodule', 
                'task', 'endtask',
                'begin', 'end',
                'initial',
                'always',
                'input', 'output', 'inout',
                'reg', 'wire',
                'integer',
                'for', 'if'
                )
    
#                'st_display', 'st_finish'

    #reserved_map = { word:word for word in reserved }
    reserved_map = {}
    for word in reserved:
        reserved_map[word] = word

    # tokens
    tokens = ('ID', 'NUM', 'NB_ASIGN', 'STASK') + reserved

    # literals
    literals = "()[],.;:$=<+-"

    
    def __init__(self):
        self.lexer  = lex.lex(module=self)
        self.parser = yacc.yacc(module=self,start='module_declaration')
        self.modules = []

    def parse(self, buf):
        self.parser.parse(buf)
        return self.modules

   
    #t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = Parser.reserved_map.get(t.value,'ID')
        return t
    
    def t_NUM(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NB_ASIGN(self,t):
        r'<='
        return t

    def t_STASK(self,t):
        r'\$[a-zA-Z]+'
        return t
    
    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        

    # variables_declaration

    def p_variables_declaration_bits(self,p):
        '''variables_declaration : variable_type range variables ';'
        '''

    def p_variables_declaration_bit(self,p):
        '''variables_declaration : variable_type variables ';'
        '''

    def p_variable_type(self,p):
        '''variable_type : reg
                         | wire
                         | integer
                         '''

    def p_variables_recur(self,p):
        '''variables : ID ',' variables'''

    def p_variables_single(self,p):
        '''variables : ID '''


    # module_instantiation

    def p_module_instantiation(self,p):
        '''module_instantiation : ID ID '(' instantiation_parameters ')' ';'
        '''

    def p_instantiation_parameters_recur(self,p):
        '''instantiation_parameters : instantiation_parameter ',' instantiation_parameters
        '''

    def p_instantiation_parameters(self,p):
        '''instantiation_parameters : instantiation_parameter
        '''
        
    def p_instantiation_parameters_null(self,p):
        '''instantiation_parameters : 
        '''
        
    # instantiation_parameter

    def p_instantiation_parameter_specify(self,p):
        '''instantiation_parameter : '.' ID '(' ID ')'
        '''

    def p_instantiation_parameter(self,p):
        '''instantiation_parameter : ID
        '''

    # initial_block
    def p_initial_block(self,p):
        '''initial_block : initial block'''

    def p_block_statement(self,p):
        '''block : statement'''

    def p_block_compound(self,p):
        '''block : begin statements end'''

    def p_statements_recur(self,p):
        '''statements : statement statements'''

    def p_statements_null(self,p):
        '''statements : '''

    def p_statement(self,p):
        '''statement : delay basic_statement'''

    def p_delay(self,p):
        '''delay : '#' NUM'''

    def p_basic_statement(self,p):
        '''basic_statement : block
                           | assignment
                           | task_call
                           | for_statement
                           '''

    def p_assignment(self,p):
        '''assignment : ID '=' ID
                      | ID NB_ASIGN ID
                      '''

    def p_task_call(self,p):
        '''task_call : system_task task_arguments ';'
                     | ID task_arguments ';'
                     '''

    def p_system_task(self,p):
        '''system_task : STASK
        '''

    def p_task_arguments(self,p):
        '''task_arguments : '''

    def p_for_statement(self,p):
        '''for_statement : for for_constraints block'''

    def p_for_constraints(self,p):
        '''for_constraints : '(' for_init_cond ',' for_end_cond ',' for_next_cond ')'
        '''
    def p_for_init_cond(self,p):
        '''for_init_cond : 
        '''

    def p_for_end_cond(self,p):
        '''for_end_cond : 
        '''

    def p_for_next_cond(self,p):
        '''for_next_cond : 
        '''

    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")



