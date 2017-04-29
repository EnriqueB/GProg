import parser
import logging

def test(code):
    log = logging.getLogger()
    parser.parser.parse(code, tracking=True)

#print "Simplest type of program"
#s = 'file:"asdasd"%%%%'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"


#print "Program with descriptors"
#s = 'crossover: 0.3 mutation:0.2 popsize:100 generations:100 file:"asdasdas"%%%%'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

#print "Program with descriptors, wrong type"
#s = 'crossover: 10 mutation:0.2 popsize:100 generations:100 file:"asdasdas"%%%%'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

#print "Program with function with an if"
#s = 'file:"asdasd"%% max(float a, float b){if(a<b){b = a+b;} return b;}%%'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

#print "Program with eval function"
#s = 'file:"c://a.txt"%% %%eval(float a, float b){int t = 5; return b;}'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

#print "Program with multiple functions and eval"
#s = 'file:"c://a.txt"%% maxx(float a, float b){int c = 3; if(a<b){b=a;} return b;} mult(float a, float b){while(b > 2){a = a + a; b = b - 1;} return a;} %%eval(float a, float b){int t_val = 5; return b/p_val;}'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

#print "Program with function with an if"
#s = 'file:"asdasd"%% maxxx(float a, float b){if(a<b){b = a;} return b;} min(float a, float b){if(a>b){b = a;} return b;}%%'
#test(s)
#print "Original: \n{0}".format(s)
#print "\n"

print "test"
s = 'file:"values.txt"%% sumThree(float a){int b = 0; float c = a; while(b<3){a = a + c; b = b+1; if(a>1){b = 4;}} return a;}'
test(s)
