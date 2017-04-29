#pragma once
#ifndef FUNCTION_H
#define FUNCTION_H


#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <stdio.h>
#include <stdlib.h>

struct INSTRUCTION {
	string opt;
	int op1;    //address
	int op2;    //address
	int res;    //address
};

class method {
private:
	string name;
	int params;     //how many parameters
	int intVars[2000];
	int intVarStart;

	double floatVars[2000];
	int floatVarStart;

	int intTemps[3000];
	int intTempStart;

	double floatTemps[3000];
	int floatTempStart;

	bool boolTemps[2000];
	int boolTempStart;

	int intConst[2000];
	int iCP;
	int intConstStart;

	double floatConst[2000];
	int fCP;
	int floatConstStart;

	vector <INSTRUCTION> instructions;

public:
	method() { params = 0; }
	method(string filename) { readFile(filename); }
	void readFile(string filename);
	double execute(vector <double> parameters);
	double obtainValue(int address);
	void setValue(double value, int address);

	int getParams() { return params; }
	string getName() { return name; }
};


void method::readFile(string filename) {
	iCP = fCP = 0;
	intVarStart = 1000;
	floatVarStart = 3000;
	intTempStart = 5000;
	floatTempStart = 8000;
	boolTempStart = 11000;
	intConstStart = 13000;
	floatConstStart = 15000;
	//open file
	ifstream file(filename);
	int consts;
	file >> name;
	file >> consts;
	string s;

	//CHECK IF THEY ARE PASSED IN ORDER!!!!
	for (int i = 0; i<consts; i++) {
		file >> s;
		int pos = atoi(s.substr(2).c_str());
		if (pos < floatConstStart) {
			file >> intConst[pos - intConstStart];
		}
		else {
			file >> floatConst[pos - floatConstStart];
		}
	}
	file >> params;

	//read instruction list
	int val;
	while (file >> s) {
		INSTRUCTION i;
		i.opt = s;
		if (s == "goto") {
			file >> s >> s >> val;
			i.op1 = -1;
			i.op2 = -1;
			i.res = val;
		}
		else if (s == "gotof") {
			file >> val;
			i.op1 = val;
			file >> s >> val;
			i.op2 = -1;
			i.res = val;
		}
		else if (s == "ret") {
			file >> s >> s >> val;
			i.op1 = -1;
			i.op2 = -1;
			i.res = val;
		}
		else if (s == "=") {
			file >> val;
			i.op1 = val;
			i.op2 = -1;
			file >> s>>val;
			i.res = val;
		}
		else {
			file >> val;
			i.op1 = val;
			file >> val;
			i.op2 = val;
			file >> val;
			i.res = val;
		}
		instructions.push_back(i);
	}
	file.close();
}

double method::execute(vector <double> parameters) {
	for (int i = 0; i < params; i++) {
		floatVars[i] = parameters[i];
	}
	int pC = 0;	//program counter
	int total = 0;

	while (pC < instructions.size()) {
		if (total++ > 3000) {
			cout << "Error, possible infinite loop in tree...\n";
			exit(EXIT_FAILURE);
		}
		if (instructions[pC].opt == "goto") {
			pC = instructions[pC].res;
		}
		else if (instructions[pC].opt == "gotof") {
			//evaluate expression
			if (!boolTemps[instructions[pC].op1 - boolTempStart]) {
				pC = instructions[pC].res;
			}
			else {
				pC++;
			}
		}
		else if(instructions[pC].opt == "ret") {
			return obtainValue(instructions[pC].res);
		}
		else if (instructions[pC].opt == "=") {
			setValue(obtainValue(instructions[pC].op1), instructions[pC].res);
			pC++;
		}
		else {
			double op;
			switch (instructions[pC].opt[0]) {
				case '+':
					setValue(obtainValue(instructions[pC].op1) + obtainValue(instructions[pC].op2), instructions[pC].res);
					break;
				case '-':
					setValue(obtainValue(instructions[pC].op1) - obtainValue(instructions[pC].op2), instructions[pC].res);
					break;
				case '*':
					setValue(obtainValue(instructions[pC].op1) * obtainValue(instructions[pC].op2), instructions[pC].res);
					break;
				case '/':
					op = obtainValue(instructions[pC].op2);
					if (op > -0.000001 && op < 0.000001) {
						setValue(1.0, instructions[pC].res);
					}
					setValue(obtainValue(instructions[pC].op1) / obtainValue(instructions[pC].op2), instructions[pC].res);
					break;
				case '<':
					if (instructions[pC].opt.length() > 1) {
						if (obtainValue(instructions[pC].op1) <= obtainValue(instructions[pC].op2)) {
							boolTemps[instructions[pC].res - boolTempStart] = true;
						}
						else {
							boolTemps[instructions[pC].res - boolTempStart] = false;
						}
					}
					else {
						if (obtainValue(instructions[pC].op1) < obtainValue(instructions[pC].op2)) {
							boolTemps[instructions[pC].res - boolTempStart] = true;
						}
						else {
							boolTemps[instructions[pC].res - boolTempStart] = false;
						}
					}
					break;
				case '>':
					if (instructions[pC].opt.length() > 1) {
						if (obtainValue(instructions[pC].op1) >= obtainValue(instructions[pC].op2)) {
							boolTemps[instructions[pC].res - boolTempStart] = true;
						}
						else {
							boolTemps[instructions[pC].res - boolTempStart] = false;
						}
					}
					else {
						if (obtainValue(instructions[pC].op1) > obtainValue(instructions[pC].op2)) {
							boolTemps[instructions[pC].res - boolTempStart] = true;
						}
						else {
							boolTemps[instructions[pC].res - boolTempStart] = false;
						}
					}
					break;
				case '=':
					if (obtainValue(instructions[pC].op1) == obtainValue(instructions[pC].op2)) {
						boolTemps[instructions[pC].res - boolTempStart] = true;
					}
					else {
						boolTemps[instructions[pC].res - boolTempStart] = false;
					}
					break;
				case '!':
					if (obtainValue(instructions[pC].op1) != obtainValue(instructions[pC].op2)) {
						boolTemps[instructions[pC].res - boolTempStart] = true;
					}
					else {
						boolTemps[instructions[pC].res - boolTempStart] = false;
					}
					break;
			}
			pC++;
		}
	}
	return 0;
}

double method::obtainValue(int address) {
	if (address < floatVarStart) {
		return (double)intVars[address - intVarStart];
	}
	if (address < intTempStart) {
		return floatVars[address - floatVarStart];
	}
	if (address < floatTempStart) {
		return (double)intTemps[address - intTempStart];
	}
	if (address < boolTempStart) {
		return floatTemps[address - floatTempStart];
	}
	if (address < intConstStart) {
		return (double)boolTemps[address - boolTempStart];
	}
	if (address < floatConstStart) {
		return (double)intConst[address - intConstStart];
	}
	return floatConst[address - floatConstStart];
}

void method::setValue(double value, int address) {
	if (address < floatVarStart) {
		intVars[address - intVarStart] = (int)value;
	}
	else if (address < intTempStart) {
		floatVars[address - floatVarStart] = value;
	}
	else if (address < floatTempStart) {
		intTemps[address - intTempStart] = (int)value;
	}
	else if (address < boolTempStart) {
		floatTemps[address - floatTempStart] = value;
	}
	else if (address < intConstStart) {
		boolTemps[address - boolTempStart] = (bool)value;
	}
	else {
		cout << "ERROR EN SET VALUE\n";
	}
}


#endif