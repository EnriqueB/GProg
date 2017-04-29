import sys
class Var:
    def __init__(self, Name='', Type=int, Address='0', Value = 0):
        self.Name = Name
        self.Type = Type
        self.Address = Address
        self.Value = Value

    def __str__(self):
        return "{}".format(str(self.Name))

class procedureDirectory:
    constants = {}

    def __init__(self, identifier):
        self.identifier = identifier
        self.parameters = {}
        self.vars = {}
        self.constants
        self.type = None
        self.quads = []

        self.nextIntVar = 1000
        self.nextFloatVar = 3000
        self.nextIntTemp = 5000
        self.nextFloatTemp = 8000
        self.nextBoolTemp = 11000
        self.nextIntConst = 13000
        self.nextFloatConst = 15000

    def add_var(self, ID, type):
        if ID in self.vars:
            print("ERROR: Variable '{}' already declared".format(str(ID)))
            sys.exit()
        else:
            if type == int:
                self.vars[ID] = Var(ID, type, self.nextIntVar)
                self.nextIntVar += 1
                return self.vars[ID]
            else:
                self.vars[ID] = Var(ID, type, self.nextFloatVar)
                self.nextFloatVar += 1
                return self.vars[ID]
    
    def add_temp(self, type):
        ID = ""
        if type == int:
            ID = "Ti"+str(self.nextIntTemp)
            self.vars[ID] = Var(ID, type, self.nextIntTemp)
            self.nextIntTemp += 1
        
        if type == float:
            ID = "Tf"+str(self.nextFloatTemp)
            self.vars[ID] = Var(ID, type, self.nextFloatTemp)
            self.nextFloatTemp += 1
        
        if type == bool:
            ID = "Tb"+str(self.nextBoolTemp)
            self.vars[ID] = Var(ID, type, self.nextBoolTemp)
            self.nextBoolTemp += 1
        return self.vars[ID]
    
    def add_const(self, type, val):
        ID = ""
        if type == int:
            ID = "Ci"+str(self.nextIntConst)
            self.vars[ID] = Var(ID, type, self.nextIntConst, val)
            self.nextIntConst+=1
        
        if type == float:
            ID = "Cf"+str(self.nextFloatConst)
            self.vars[ID] = Var(ID, type, self.nextFloatConst, val)
            self.nextFloatConst+=1
        return self.vars[ID]

    def get_var(self, ID):
        if ID in self.vars:
            return self.vars[ID]
        elif ID in self.parameters:
            return self.parameters[ID]
        else:
            print("ERROR: Varible '{}' not declared".format(str(ID)))
            sys.exit()

    def add_parameter(self, ID, type):
        if ID in self.parameters:
            print("ERROR: Variable '{}' already declared".format(str(ID)))
        else:
            self.parameters[ID] = Var(ID, type, self.nextFloatVar)
            self.nextFloatVar+=1

    def get_parameter(self, ID):
        if ID in self.parameters:
            return self.parameters[ID]
        else:
            print("ERROR: Variable '{}' not declared".format(str(ID)))

    def print_vars(self):
        for v in self.vars:
            print "\t\t", v
    
    def print_parameters(self):
        for p in self.parameters:
            print "\t\t", p
    
    def print_to_file(self, filename):
        f = open(filename, "a")
        f.write(str(self.nextIntConst-13000+self.nextFloatConst-15000))
        f.write("\n")
        for k, v in self.vars.iteritems():
            if v.Address >= 13000:
                s = v.Name + " " +str(v.Value) + "\n"
                f.write(s)
        f.write(str(len(self.parameters)))
        f.write("\n")