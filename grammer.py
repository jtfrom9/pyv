import ply.lex as lex
import ply.yacc as yacc

from Module import Module
from Module import ParameterList

class Parser:
    # reserved words
    reserved = ('module', 'endmodule', 
                'task', 'endtask',
                'begin', 'end',
                'initial',
                'always',
                'input', 'output', 'inout',
                'reg', 'wire',
                'integer',
                'for', 'if', 
                '<=',
                '$display', '$finish'
                )

    #reserved_map = { word:word for word in reserved }
    reserved_map = {}
    for word in reserved:
        reserved_map[word] = word

    # tokens
    tokens = ('ID', 'NUM') + reserved

    # literals
    literals = "()[],.;:$=<+-"

    
    def __init__(self):
        self.lexer  = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.modules = []

    #t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = Parser.reserved_map.get(t.value,'ID')
        return t
    
    def t_NUM(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

        
    def p_module_unit(self,p):
        '''module_unit : module ID header module_body endmodule'''

    def p_task(self,p):
        '''task : task ID header task_body endtask'''

    # header
    def p_header(self,p):
        '''header : parameters ';' '''

    # parameters
    def p_parameters(self,p):
        '''parameters : '(' parameter_list ')'''

    def p_parameters_null(self,p):
        '''parameters : '('  ') 
                      |
        '''


    # parameter_list

    def p_parameter_list_recursive(self,p):
        '''parameter_list : param ',' parameter_list'''

    def p_parameter_list_id(self,p):
        '''parameter_list : param'''

    def p_parameter_list_null(self,p):
        '''parameter_list : '''

    # parameter

    def p_parameter(self,p):
        '''parameter : parameter_type ID'''

    def p_parameter_simple(self,p):
        '''parameter : ID'''

    # parameter_type

    def p_parameter_type_bits(self,p):
        '''parameter_type : direction bitwidth'''

    def p_parameter_type_bit(self,p):
        '''parameter_type : direction '''

    def p_direction(self,p):
        '''direction : input
                     | output
                     | inout'''

    def p_bitwidth(self,p):
        '''bitwidth : '[' NUM ':' NUM ']' '''


    # module_body

    def p_module_body(self,p):
        '''module_body : variables_declaration module_body
                       | module_instantiation  module_body
                       | task_declaration      module_body 
                       | initial_block         module_body 
        '''

    def p_module_body_null(self,p):
        '''module_body : '''


    # variables_declaration

    def p_variables_declaration_bits(self,p):
        '''variables_declaration : variable_type bitwidth variables ';'
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

    # task_declaration
    def p_task_declaration(self,p):
        '''task_declaration : task ID header task_body endtask
        '''

    def p_task_body(self,p):
        '''task_body : variables_declaration task_body
                     | initial_block         task_body
                     '''

    def p_task_body_null(self,p):
        '''task_body : '''

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
                      | ID '<=' ID
                      '''

    def p_task_call(self,p):
        '''task_call : system_task task_arguments ';'
                     | ID task_arguments ';'
                     '''

    def p_system_task(self,p):
        '''system_task : $display
                         $finish
        '''

    def p_task_arguments(self,p):
        '''task_arguments : '''

    def p_for_statement(self,p):
        '''for_statement : for for_constraints block'''

    def p_for_constraints(self,p):
        '''for_constraints: '(' for_init ',' for_end_cond ',' for_step ')'
        '''


    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    def parse(self, buf):
        self.parser.parse(buf)
        return self.modules


