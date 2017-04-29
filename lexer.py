import ply.lex as lex

reserved = (
    "CROSSOVER",
    "MUTATION",
    "POPSIZE",
    "GENERATIONS",
    "OPERATORS",
    "EVAL",
    "IF",
    "ELSE",
    "FOR",
    "WHILE",
    "RETURN",
    "TRUE",
    "FALSE",
    "FILE",
    "INT",
    "FLOAT"
)

tokens = reserved + (
        # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

        # Assignment (=)
    'EQUALS',

        # Literals (identifier, integer constant, float constant, string constant)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST',

        # Delimeters ( ) { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON'
)

# token regular definition
t_ignore = ' \t\r'

t_SCONST   = '".*"'

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LNOT = r'!'


t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='


# Assignment operators

t_EQUALS = r'='

# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'


# Identifiers and reserved words
reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_FCONST(t):
    r'[-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_ICONST(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # Check for reserved words
    t.type = reserved_map.get(t.value,"ID")
    return t

def t_error(t):
    print "Lexical Error in: "
    print  t.value[0], " in pos ", t.lexer.lineno
    exit(-1)
    t.lexer.skip(1)

lexer = lex.lex()
