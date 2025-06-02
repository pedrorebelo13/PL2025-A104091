import ply.yacc as yacc
from lexer_pascal import tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('right', 'UMINUS')
)


def p_programa(p):
    """programa : PROGRAM ID SEMI bloco DOT"""
    p[0] = ('programa', p[2], p[4])

def p_bloco(p):
    """bloco : declaracoes BEGIN comandos END"""
    p[0] = ('bloco', p[1], p[3])

def p_declaracoes(p):
    """declaracoes : VAR declaracao_vars
                  | """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_declaracao_vars(p):
    """declaracao_vars : declaracao_var
                      | declaracao_vars declaracao_var"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao_var(p):
    """declaracao_var : lista_ids COLON tipo SEMI"""
    p[0] = ('declaracao_vars', p[1], p[3])

def p_lista_ids(p):
    """lista_ids : ID
                | lista_ids COMMA ID"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_tipo(p):
    """tipo : INTEGER
           | BOOLEAN"""
    p[0] = p[1]

def p_comandos(p):
    """comandos : comando
                | comandos SEMI comando"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_comando(p):
    """comando : atribuicao
               | comando_if
               | comando_while
               | comando_for
               | """
    if len(p) > 1:
        p[0] = p[1]

def p_atribuicao(p):
    """atribuicao : ID ASSIGN expr_bool"""
    p[0] = ('atribuicao', p[1], p[3])

def p_comando_if(p):
    """comando_if : IF expr_bool THEN comando
                  | IF expr_bool THEN comando ELSE comando"""
    if len(p) == 5:
        p[0] = ('if', p[2], p[4], None)
    else:
        p[0] = ('if', p[2], p[4], p[6])

def p_comando_while(p):
    """comando_while : WHILE expr_bool DO comando
                     | WHILE expr_bool DO BEGIN comandos END"""
    if len(p) == 5:
        p[0] = ('while', p[2], p[4])  # Corpo é um único comando
    else:
        p[0] = ('while', p[2], ('bloco', [], p[5]))  # Corpo é um bloco de comandos

def p_comando_for(p):
    """comando_for : FOR ID ASSIGN expr_bool TO expr_bool DO comando"""
    p[0] = ('for', p[2], p[4], p[6], p[8])

def p_comando_readwrite(p):
    """comando : READLN LPAREN ID RPAREN
              | WRITE LPAREN args_write RPAREN
              | WRITELN LPAREN args_write RPAREN"""
    if p[1].lower() == 'readln':
        p[0] = ('readln', p[3])
    elif p[1].lower() == 'write':
        p[0] = ('write', p[3])
    else:  # writeln
        p[0] = ('writeln', p[3])

def p_args_write(p):
    """args_write : STRING
                 | expr_bool
                 | args_write COMMA STRING
                 | args_write COMMA expr_bool"""
    if len(p) == 2:
        if isinstance(p[1], str):  # Se for STRING
            p[0] = [('valor', p[1])]
        else:  # Se for expr_bool
            p[0] = [p[1]]
    else:  # Com vírgula
        if isinstance(p[3], str):  # Se for STRING
            p[0] = p[1] + [('valor', p[3])]
        else:  # Se for expr_bool
            p[0] = p[1] + [p[3]]

    
def p_expr_bool_rel(p):
    """expr_bool : expr
                 | expr oprel expr"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('rel', p[2], p[1], p[3])

def p_oprel(p):
    """oprel : EQUAL
             | NEQUAL
             | LT
             | LE
             | GT
             | GE"""
    p[0] = p[1]

def p_expr_binop(p):
    """expr : expr opad termo
            | termo"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_opad(p):
    """opad : PLUS
            | MINUS
            | OR"""
    p[0] = p[1]

def p_termo_binop(p):
    """termo : termo opmul fator
              | fator"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_opmul(p):
    """opmul : TIMES
             | DIVIDE
             | DIV
             | MOD
             | AND"""
    p[0] = p[1]

def p_fator(p):
    """fator : NUMBER
              | STRING
              | ID
              | ID LBRACKET expr RBRACKET
              | ID LPAREN args RPAREN
              | LPAREN expr_bool RPAREN
              | MINUS fator %prec UMINUS
              | NOT fator"""
    if len(p) == 2:
        p[0] = ('valor', p[1])
    elif len(p) == 4 and p[2] == '(':
        p[0] = ('call', p[1], p[3])
    elif len(p) == 4 and p[2] == '[':
        p[0] = ('index', p[1], p[3])
    elif len(p) == 3 and p[1] == '-':
        p[0] = ('uminus', p[2])
    elif len(p) == 3 and p[1] == 'not':
        p[0] = ('not', p[2])
    else:
        p[0] = p[2]

def p_args(p):
    """args : expr_bool
            | args COMMA expr_bool"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]



def p_error(p):
    if p:
        print(f"Erro de sintaxe na linha {p.lineno}: token '{p.value}'")
    else:
        print("Erro de sintaxe no fim do input")

parser = yacc.yacc()

