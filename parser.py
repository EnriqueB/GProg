import lexer
import sys
import ply.yacc as yacc
from procDirectory import procedureDirectory, Var
from quadGen import quadGen
from semanticC import getResultingType

tokens = lexer.tokens

functionList = []
operators = {}

directoryTable = {}
geneticOperators = {}

seenType = None

q = quadGen()

start = 'program'

#first rule
def p_program(p):
    '''program : program2 file  MOD MOD program3'''
    global directoryTable, functionList, q, geneticOperators, operators
    #parameter and function files need to be generated
    #so the virtual machine may use them
    file = open("parameters.gp", "a")
    file.write(str(len(functionList))+"\n")
    for k, v in geneticOperators.iteritems():
        file.write(str(k)+" "+str(v)+"\n")

    file = open("functions.gp", "w")
    for k in operators:
        file.write(k+" 2\n")
    if not bool(operators):
        file.write("+ 2\n- 2\n* 2\n/ 2")
    
    file.close()

def p_program2(p):
    '''program2 : descriptors program2
                | empty '''

def p_program3(p):
    '''program3 : functions program3
                | empty '''

def p_descriptors(p):
    '''descriptors : CROSSOVER COLON FCONST 
                    | MUTATION COLON FCONST
                    | POPSIZE COLON ICONST
                    | GENERATIONS COLON ICONST
                    | OPERATORS COLON ops '''
    global geneticOperators
    if not p[1] == "operators":
        if p[1] in geneticOperators:
            print "ERROR: multiple definitions of genetic operators"
            sys.exit()
        else:
            geneticOperators[p[1]] = p[3]
        

def p_ops(p):
    '''ops : PLUS ops2
            | MINUS ops2
            | TIMES ops2
            | DIVIDE ops2 '''
    global operators
    if p[1] in operators:
        print "ERROR: operator already declared"
        sys.exit()
    else:
        operators[p[1]] = 1

def p_ops2(p):
    '''ops2 : COMMA ops
            | empty '''

def p_file(p):
    '''file : FILE COLON SCONST'''
    file = open("parameters.gp", "w")
    file.write(p[3]+"\n")

def p_type(p):
    '''type : INT
            | FLOAT'''

    global seenType
    if p[1] == 'int':
        seenType = int
    elif p[1] == 'float':
        seenType = float
    else:
        #error
        print "ERROR: Type error"
        sys.exit()

def p_var_declarator(p):
    '''var_declarator : type var_declaration SEMI'''

def p_var_declaration(p):
    '''var_declaration : ID var_seen var_declaration2'''

def p_var_seen(p):
    '''var_seen :'''
    #when the ID of a variable has been found. 
    global seenType, directoryTable, functionList
    func = directoryTable[functionList[-1]]
    func.add_var(p[-1], seenType)

def p_var_declaration2(p):
    '''var_declaration2 : EQUALS expression
                        | empty'''
    global q, directoryTable
    if p[1]:
        #get var
        var = p[-2]
        var = directoryTable[functionList[-1]].get_var(var)
        op1 = q.popOperandStack()
        operator = p[1]
        #check type
        varType = getResultingType(var.Type, op1.Type, operator)
        if varType == None:
            print "ERROR: wrong type"
            sys.exit()
        else: 
            q.generateQuad(operator, op1, None, var)

def p_var_value(p):
    '''var_value : ID saw_id EQUALS expression SEMI'''
    global q, directoryTable
    op1 = q.popOperandStack()
    var = q.popOperandStack()
    operator = '='
    #check type
    varType = getResultingType(var.Type, op1.Type, operator)
    if varType == None:
        print "ERROR: wrong type"
        sys.exit()
    else: 
        q.generateQuad(operator, op1, None, var)

def p_saw_id(p):
    '''saw_id :'''
    global q, directoryTable
    var = directoryTable[functionList[-1]].get_var(p[-1])
    q.pushOperandStack(var)

def p_expression(p):
    '''expression : num_expression expression2'''

def p_expression2(p):
    '''expression2 : comp num_expression seen_comp
                    | empty'''
    
def p_seen_comp(p):
    '''seen_comp : '''
    global q, directoryTable, functionList
    op2 = q.popOperandStack()
    op1 = q.popOperandStack()
    operator = q.popOperatorStack()
    #check type
    varType = getResultingType(op1.Type, op2.Type, operator)
    if varType == None:
        print "ERROR: invalid type in comparison"
        sys.exit()
    else:
        res = directoryTable[functionList[-1]].add_temp(varType)
        q.generateQuad(operator, op1, op2, res)
        q.pushOperandStack(res)

def p_comp(p):
    '''comp : EQ
            | GT
            | LT
            | GE
            | LE
            | NE'''
    global q
    q.pushOperatorStack(p[1])

def p_num_expression(p):
    '''num_expression : term num_exp_q num_expression2'''

def p_num_exp_q(p):
    '''num_exp_q :'''
    global q
    if (q.topOperatorEquals('+') or q.topOperatorEquals('-')):
        op2 = q.popOperandStack()
        op1 = q.popOperandStack()
        operator = q.popOperatorStack()
        #check type
        varType = getResultingType(op1.Type, op2.Type, operator)
        if varType == None:
            print "ERROR: invalid type"
            sys.exit()
        else:
            res = directoryTable[functionList[-1]].add_temp(varType)  
            q.generateQuad(operator, op1, op2, res)
            q.pushOperandStack(res)

def p_num_expression2(p):
    '''num_expression2 : PLUS num_exp_op num_expression
                        | MINUS num_exp_op num_expression
                        | empty'''

def p_num_exp_op(p):
    '''num_exp_op :'''
    global q
    q.pushOperatorStack(p[-1])

def p_term(p):
    '''term : factor term_q term2'''

def p_term_q(p):
    '''term_q :'''
    global q
    if (q.topOperatorEquals('*') or q.topOperatorEquals('/')):
        op2 = q.popOperandStack()
        op1 = q.popOperandStack()
        operator = q.popOperatorStack()
        varType = getResultingType(op1.Type, op2.Type, operator)
        if varType == None:
            print "ERROR: invalid type"
            sys.exit()
        else:
            res = directoryTable[functionList[-1]].add_temp(varType)
            q.generateQuad(operator, op1, op2, res)
            q.pushOperandStack(res)

def p_term2(p):
    '''term2 : DIVIDE term_operator term
                | TIMES term_operator term
                | empty'''

def p_term_operator(p):
    '''term_operator :'''
    global q
    q.pushOperatorStack(p[-1])

def p_factor(p):
    '''factor : LPAREN found_paren expression RPAREN
                | cst_expression'''
    global q
    if p[1] == "(":
        while not q.topOperatorEquals("("):
            op2 = q.popOperandStack()
            op1 = q.popOperandStack()
            operator = q.popOperatorStack()
            varType = getResultingType(op1.Type, op2.Type, operator)
            if varType == None:
                print "ERROR: invalid type"
                sys.exit()
            else:
                res = directoryTable[functionList[-1]].add_temp(varType)
                q.generateQuad(operator, op1, op2, res)
                q.pushOperandStack(res)
        q.popOperatorStack()

def p_found_paren(p):
    '''found_paren :'''
    global q
    q.pushOperatorStack("(")

def p_cst_expression(p):
    '''cst_expression : ICONST
                        | FCONST
                        | ID'''
    #check if its an ID or a number
    global q, directoryTable, functionList
    if type(p[1]) is float:
        #float
        q.pushOperandStack(directoryTable[functionList[-1]].add_const(float, float(p[1])))
    elif type(p[1]) is int:
        #int
        q.pushOperandStack(directoryTable[functionList[-1]].add_const(int, int(p[1])))
    else:
        q.pushOperandStack(directoryTable[functionList[-1]].get_var(p[1]))

def p_functions(p):
    '''functions : function'''

def p_function(p):
    '''function : ID seen_function LPAREN func_parameters RPAREN func'''

def p_seen_function(p):
    '''seen_function :'''
    #excuted when ID of a function is found
    global functionList
    global directoryTable
    functionID = p[-1]
    if functionID in functionList:
        print "ERROR: Function '{}' already declared.".format(str(functionID))
        sys.exit()
    if len(functionID) < 2:
        print "ERROR: Function name must be longer than one character"
        sys.exit()
    else:
        functionList.append(functionID)
        p = procedureDirectory(functionID)
        directoryTable[functionID] = p

def p_func(p):
    '''func : LBRACE func2 func3 RETURN expression SEMI RBRACE'''
    #when the definition of a function terminates
    #the relevant information about it must be printed
    #to file along with the quads.
    global q, functionList, directoryTable
    q.generateQuad("ret", None, None, q.popOperandStack())
    fileName = str(len(functionList))+".gp"
    file = open(fileName, 'w')
    file.write(functionList[-1].lower()+"\n")
    file.close()
    directoryTable[functionList[-1]].print_to_file(fileName)
    q.printQuadsFile(fileName)
    q.quads = []

def p_func2(p):
    '''func2 : var_declarator func2
            | empty'''

def p_func3(p):
    '''func3 : statement func3
            | empty'''

def p_func_parameters(p):
    '''func_parameters : type ID seen_func_parameter func_parameters2
                        | empty'''

def p_seen_func_parameter(p):
    '''seen_func_parameter :'''
    global seenType, directoryTable, functionList
    func = directoryTable[functionList[-1]]
    func.add_parameter(p[-1], seenType)

def p_func_parameters2(p):
    '''func_parameters2 : COMMA func_parameters
                        | empty'''

def p_block_statement(p):
    '''block_statement : LBRACE block_statement2 RBRACE'''

def p_block_statement2(p):
    '''block_statement2 : statement block_statement2
                        | empty'''

def p_statement(p):
    '''statement : var_value
                | if_statement
                | while_statement'''

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN found_if block_statement if_statement2'''
    global q
    q.fill(q.popJumpStack())

def p_found_if(p):
    '''found_if : '''
    global q
    q.generateQuad("gotof", q.popOperandStack(), None, None)
    q.pushJumpStack(q.progCounter-1)

def p_if_statement2(p):
    '''if_statement2 : ELSE found_else block_statement
                    | empty'''

def p_found_else(p):
    '''found_else :'''
    global q
    q.generateQuad("goto", None, None, None)
    cont = q.popJumpStack()
    q.fill(cont)
    q.pushJumpStack(q.progCounter-1)

def p_while_statement(p):
    '''while_statement : WHILE LPAREN found_while expression while_expression RPAREN block_statement'''
    global q
    pc = q.popJumpStack()
    q.generateQuad("goto", None, None, q.popJumpStack())
    q.fill(pc)

def p_found_while(p):
    '''found_while :'''
    global q
    q.pushJumpStack(q.progCounter)

def p_while_expression(p):
    '''while_expression :'''
    global q
    q.generateQuad("gotof", q.popOperandStack(), None, None)
    q.pushJumpStack(q.progCounter-1)

def p_empty(p):
    '''empty :'''
    pass
    
def p_error(p):
    print "ERROR: Syntax error in token: ", p.type
    print "in position: {0} ".format(p.lexpos)

import profile

# Build the grammar
parser = yacc.yacc()

if len(sys.argv) == 2:
    #parse from file
    file = open(sys.argv[1],'r')
    s = file.read()
    parser.parse(s)

else:
    print "Usage: python ", sys.argv[0], " filename"

