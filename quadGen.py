class quad:
    def __init__(self, operator = '', op1 = '', op2='', result = ''):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.result = result

class quadGen:
    def __init__(self):
        self.quads = [] 
        self.jumpStack = []
        self.operandStack = []
        self.operatorStack = []
        self.typeStack = []
        self.progCounter = 0

    def pushJumpStack(self, index):
        self.jumpStack.append(index)
    
    def popJumpStack(self):
        return self.jumpStack.pop()

    def pushOperandStack(self, operand):
        self.operandStack.append(operand)
    
    def popOperandStack(self):
        return self.operandStack.pop()

    def pushOperatorStack(self, operator):
        self.operatorStack.append(operator)
    
    def popOperatorStack(self):
        return self.operatorStack.pop()
    
    def topOperatorEquals(self, op):
        index = len(self.operatorStack)-1
        if index >= 0:
            return self.operatorStack[index]==op
        else:
            return False
    
    def pushTypeStack(self, type):
        self.typeStack.append(type)
    
    def popTypeStack(self):
        return typeStack.pop()

    def generateQuad(self, operator='', op1='', op2='', result=''):
        self.quads.append(quad(operator, op1, op2, result))
        self.progCounter +=1

    def fill(self, cont):
        self.quads[cont].result = self.progCounter
    
    def printQuads(self):
        i = 0
        for q in self.quads:
            print i, q.operator, q.op1, q.op2, q.result
            i += 1

    def printQuadsFile(self, fileName):
        #print constants
        f = open(fileName, 'a')
        i = 0
        for q in self.quads:
            s = q.operator
            if not q.op1 == None:
                s +=" " + str(q.op1.Address)
            else:
                s+= " N"
            if not q.op2 == None:
                s+= " " + str(q.op2.Address)
            else:
                s+=" N"
            if type(q.result) is int:
                s+= " "+str(q.result)
            else:
                s+= " "+str(q.result.Address)
            s+="\n"
            f.write(s)
        f.close()
