import lexer
#s = 'crossover: 1.5 file:"asdasdasd"%% sum(float val1, float val_2){return 0.1}%%'
s = 'int p_val = 3;'
lexer.lexer.input(s)


for token in lexer.lexer:
    print token
