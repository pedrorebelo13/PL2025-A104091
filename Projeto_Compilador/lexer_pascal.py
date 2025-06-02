import ply.lex as lex

# Lista de tokens
tokens = [
    # Palavras reservadas
    'PROGRAM', 'BEGIN', 'END', 'VAR', 'INTEGER', 'BOOLEAN', 'IF', 'THEN', 'ELSE',
    'WHILE', 'DO', 'FOR', 'TO', 'FUNCTION', 'PROCEDURE', 'READLN', 'WRITELN', 'WRITE',
    # Operadores e símbolos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'DIV', 'MOD', 'AND', 'OR', 'NOT',
    'EQUAL', 'NEQUAL', 'LT', 'LE', 'GT', 'GE',
    'ASSIGN', 'LPAREN', 'RPAREN', 'SEMI', 'COLON', 'DOT', 'COMMA',
    # Tipos
    'ID', 'NUMBER', 'STRING' , 'LBRACKET', 'RBRACKET',
]

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_EQUAL = r'='
t_NEQUAL = r'<>'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_DOT = r'\.'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# AGORA TODAS SERÃO TRATADAS NA FUNÇÃO t_ID

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifica se é uma palavra-chave (case-insensitive)
    keyword_value = t.value.lower()
    if keyword_value == 'program': 
        t.type = 'PROGRAM'
    elif keyword_value == 'begin': 
        t.type = 'BEGIN'
    elif keyword_value == 'end': 
        t.type = 'END'
    elif keyword_value == 'var': 
        t.type = 'VAR'
    elif keyword_value == 'integer': 
        t.type = 'INTEGER'
    elif keyword_value == 'boolean': 
        t.type = 'BOOLEAN'
    elif keyword_value == 'if': 
        t.type = 'IF'
    elif keyword_value == 'then': 
        t.type = 'THEN'
    elif keyword_value == 'else': 
        t.type = 'ELSE'
    elif keyword_value == 'while': 
        t.type = 'WHILE'
    elif keyword_value == 'do': 
        t.type = 'DO'
    elif keyword_value == 'for': 
        t.type = 'FOR'
    elif keyword_value == 'to': 
        t.type = 'TO'
    elif keyword_value == 'function': 
        t.type = 'FUNCTION'
    elif keyword_value == 'procedure': 
        t.type = 'PROCEDURE'
    elif keyword_value == 'readln': 
        t.type = 'READLN'
    elif keyword_value == 'writeln': 
        t.type = 'WRITELN'
    elif keyword_value == 'div': 
        t.type = 'DIV'
    elif keyword_value == 'mod': 
        t.type = 'MOD'
    elif keyword_value == 'and': 
        t.type = 'AND'
    elif keyword_value == 'or': 
        t.type = 'OR'
    elif keyword_value == 'not': 
        t.type = 'NOT'
    elif keyword_value == 'write': 
        t.type = 'WRITE'
    return t

def t_STRING(t):
    r"'[^']*'"  # Esta regex captura strings entre aspas simples
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\{[^}]*\}'
    pass  # Ignorar comentários

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()