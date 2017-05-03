#include <iostream>
#include <string>
#include <vector>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <stack>
#include <set>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <limits>
#include <cstdint>
#include <cmath>
#include <utility>

#include "individual.h"
#include "method.h"

#define TOURNAMENT_SIZE 5
#define PARSIMONY_PRESSURE 1.5

using namespace std;

vector <vector <double> > testArray;	
vector <pair <char, int> > functionSet;
vector <char> terminalSet;
vector <Individual> individuals;
int variables[58];
int functions[93];
string userFuncs[27];

vector <vector <double> > variableValues;

double crossoverRate = 0.9;
double mutationChance = 0.1;
double bestFitness = (double)INT32_MAX;
int bestIndex = -1;
int generation = 0;

int POPULATION_SIZE = 1000;
int GENERATIONS = 100000;
int AMMOUNT_VARIABLES;				//Does not count 'y', i.e. having y, x, z  = 2
int SAMPLE_SIZE;
double INPUT_SIZE;

string variableFile;

vector <method> methods;

/*
* This method receives a vector of vectors
* of doubles and uses it to calculate the
* results of the required operation.
* The ammount of vectors received depends on
* the arity of the operation required.
*/
vector <double> calculate(const vector <vector <double> > ops, string operation) {
	//this method executes the operations found
	//in the function string
	vector <double> ans;
	switch (operation[0]) {
	case '+':	//arity 2
		for (int i = 0; i<ops[0].size(); i++) {
			ans.push_back(ops[0][i] + ops[1][i]);
		}
		return ans;
	case '-':	//arity 2
		for (int i = 0; i<ops[0].size(); i++) {
			ans.push_back(ops[0][i] - ops[1][i]);
		}
		return ans;
	case '*':	//arity 2
		for (int i = 0; i<ops[0].size(); i++) {
			ans.push_back(ops[0][i] * ops[1][i]);
		}
		return ans;
	case '/':	//arity 2
				//protected division, can't divide by 0
		for (int i = 0; i<ops[0].size(); i++) {
			if (ops[1][i] < 0.0000001 && ops[1][i] > -0.0000001) {
				ans.push_back(0.0);
			}
			else {
				ans.push_back(ops[0][i] / ops[1][i]);
			}
		}
		return ans;
	default:
		//user defined function
		//check for arity 0
		if (ops.empty()) {
			vector <double> params;
			for (int i = 0; i < SAMPLE_SIZE; i++) {
				ans.push_back(methods[operation[0] - 'A'].execute(params));
			}
			return ans;
		}
		for (int i = 0; i < ops[0].size(); i++) {
			vector <double> params;
			for (int j = 0; j < ops.size(); j++) {
				params.push_back(ops[j][i]);
			}
			ans.push_back(methods[operation[0] - 'A'].execute(params));
		}
		return ans;
	}

}

/*
* This method parses and evaluates
* a solution tree for all of the
* training examples.
* It tokenizes the string and evaluates
* it from the end to the front.
*/
vector <double> evaluate(int index) {
	stack <vector <double> > calculator;

	//tokenize the string	
	string::size_type sz;
	stringstream ss(individuals[index].getSolution());
	string item;
	vector <string> tokens;
	while (getline(ss, item, ' ')) {
		tokens.push_back(item);
	}
	int i = tokens.size() - 1;
	//Evaluate tree from the end
	while (i >= 0) {
		if (functions[tokens[i][0] - 33] < 0 || tokens[i].length()>1) {
			//not an operator, push to stack
			if (tokens[i][0]>64 && variables[tokens[i][0] - 'A'] >= 0) {
				//if the token is a variable then insert the values
				calculator.push(variableValues[variables[tokens[i][0] - 'A']]);
			}
			else {
				//Push a vector of the value
				//double val = stod(tokens[i], &sz);	//this stopped working...??
				double val = strtod(tokens[i].c_str(), NULL);
				vector <double> v(SAMPLE_SIZE, val);
				calculator.push(v); //push the value of the token
			}
		}
		else {
			//A vector of vectors is created to manage
			//functions with different arities.
			vector <vector <double> > ops;
			//Find arity of the operator
			int arity = functions[tokens[i][0] - 33];
			for (int j = 0; j < arity; j++) {
				ops.push_back(calculator.top());
				calculator.pop();
			}
			calculator.push(calculate(ops, tokens[i]));
		}
		i--;
	}
	return calculator.top();
}

void evaluateFitness() {
	//Evaluate the string against the multiple test cases
	for (int i = 0; i < POPULATION_SIZE; i++) {
		vector <double> results;
		results = evaluate(i);
		double error = 0;
		for (int j = 0; j < SAMPLE_SIZE; j++) {
			//Mean square error
			error += pow(testArray[j][0] - results[j], 2);
		}
		individuals[i].setFitness(error / INPUT_SIZE);
		if ((error / INPUT_SIZE) < bestFitness) {
			bestFitness = error / INPUT_SIZE;
			bestIndex = i;
		}
	}
}

double evaluateSingle(int index) {
	//only run the tests for a single individual
	double error = 0;
	vector <double> results = evaluate(index);
	for (int j = 0; j < SAMPLE_SIZE; j++) {
		error += pow(testArray[j][0] - results[j], 2);
	}
	if ((error / INPUT_SIZE) < bestFitness) {
		bestFitness = error / INPUT_SIZE;
		bestIndex = index;
	}
	return error / INPUT_SIZE;
}


int tournament(bool type) {
	//Tournament selection
	//type = true for normal, false for negative tournament
	double fitness = (double)INT32_MAX;
	if (!type)fitness = 0;
	int index = 0;
	for (int i = 0; i < TOURNAMENT_SIZE; i++) {
		int ind = rand() % POPULATION_SIZE;
		string s = individuals[ind].getSolution();
		int nodes = count(s.begin(), s.end(), ' ');
		//check tournament type
		if (((individuals[ind].getFitness() + nodes*PARSIMONY_PRESSURE) < fitness) == type) {
			if (!type) {
				if (ind == bestIndex) {
					i--;
					continue;
				}
			}
			fitness = individuals[ind].getFitness() + nodes*PARSIMONY_PRESSURE;
			index = ind;
		}
	}
	return index;
}

void generateOffspring() {
	double random = ((double)rand() / (RAND_MAX));
	Individual ind(functionSet, terminalSet);
	int index;
	//offspring is generated either by crossover or mutation
	if (random < crossoverRate) {
		//crossover, pick two parents
		int parent1 = tournament(true);
		int parent2 = tournament(true);
		ind.crossOver(individuals[parent1].getSolution(), individuals[parent2].getSolution());
		//find a suitable candidate to replace
		index = tournament(false);
		individuals[index].setSolution(ind.getSolution());
		individuals[index].setFitness(evaluateSingle(index));
	}
	else {
		//mutation
		index = tournament(true);
		ind.setSolution(individuals[index].getSolution());
		ind.mutate();
		index = tournament(false);
		individuals[index].setSolution(ind.getSolution());
		individuals[index].setFitness(evaluateSingle(index));
	}
}

void readUserFunctions(int uf) {
	//read all of the user functions from files
	string filename = "";
	for (int i = 0; i < uf; i++) {
		stringstream ss;
		ss<<i+1;
		filename = ss.str()+".gp";
		method m(filename);
		methods.push_back(m);
		//user functions start from 'A' to 'Z'
		functions['A' + i - 33] = m.getParams();
		functionSet.push_back(make_pair('A' + i, m.getParams()));
		userFuncs[i] = m.getName();
	}
}

int readRunParameters() {
	//read the run parameters from file
	string descriptor;
	int userFunctions;
	ifstream fs;
	fs.open("parameters.gp");
	fs >> variableFile;
	fs >> userFunctions;
	while (fs >> descriptor) {
		switch (descriptor[0]) {
		case 'p':
			//popsize
			fs >> POPULATION_SIZE;
			break;
		case 'm':
			//mutation
			fs >> mutationChance;
			break;
		case 'g':
			//generations
			fs >> GENERATIONS;
			break;
		case 'c':
			//crossover
			fs >> crossoverRate;
			break;
		}
	}
	variableFile = variableFile.substr(1, variableFile.length() - 2);
	fs.close();
	return userFunctions;
}

string replaceUserFunctions(int uf, int index) {
	//when printing, replace all single letter functions
	//with the full function name
	string solution = individuals[index].getSolution();
	for (int i = 0; i < uf; i++) {
		char search = 'A' + i;
		string rep = userFuncs[i];
		size_t start_pos = 0;
		while ((start_pos = solution.find(search, start_pos)) != string::npos) {
			solution.replace(start_pos, 1, rep);
			start_pos += rep.length();
		}
	}
	return solution;
}

int main() {
	srand(time(NULL));
	//prepare arrays
	memset(variables, -1, sizeof(variables));
	memset(functions, -1, sizeof(functions));

	//read function set from file
	ifstream fs("functions.gp");
	char func;
	int arity;
	while (fs >> func) {
		fs >> arity;
		functions[func - 33] = arity;
		functionSet.push_back(make_pair(func, arity));
	}
	fs.close();

	//read run parameters
	int userFunctions = readRunParameters();
	
	//read user functions
	readUserFunctions(userFunctions);

	//read values and variables from file
	fs.open(variableFile);
	//read variable letters first
	string vars;
	getline(fs, vars);
	AMMOUNT_VARIABLES = count(vars.begin(), vars.end(), ' ');
	for (int i = 2, j = 0; i < vars.length(); i += 2, j++) {
		terminalSet.push_back(vars[i]);
		variables[vars[i] - 'A'] = j;
	}

	//read values
	double val;
	int i = 0;
	while (fs >> val) {
		vector <double> ts;
		ts.push_back(val);
		for (int j = 1; j<AMMOUNT_VARIABLES+1; j++) {
			fs >> val;
			ts.push_back(val);
		}
		testArray.push_back(ts);
		i++;
	}
	SAMPLE_SIZE = i;
	INPUT_SIZE = (double)SAMPLE_SIZE;
	fs.close();

	//create a vector of values for each variables
	//these vectors are used when parsing the tree
	for (int i = 1; i<AMMOUNT_VARIABLES + 1; i++) {
		vector <double> vals;
		for (int j = 0; j<SAMPLE_SIZE; j++) {
			vals.push_back(testArray[j][i]);
		}
		variableValues.push_back(vals);
	}

	//generate individuals
	for (int i = 0; i < POPULATION_SIZE; i++) {
		char type = 'f';
		if (rand() % 2 < 0.5) {
			type = 'g';
		}
		Individual ind(functionSet, terminalSet, -10, 10, 2+(i/(POPULATION_SIZE/2)), type, mutationChance, crossoverRate);
		individuals.push_back(ind);
		//cout<<"\n"<<ind.getSolution()<<endl;
	}
	//evaluate fitness of the initial population

	evaluateFitness();

	//start of the run
	cout << "Starting...\n";
	for (; generation < GENERATIONS; generation++) {
		if(generation % (GENERATIONS/10) == 0){
			cout<<"Generation : "<<generation<<"...\n";
		}
		generateOffspring();
		if(bestFitness < 0.00001){
			cout<<"Found a good candidate\n";
			break;
		}
	}
	string bestSolution = replaceUserFunctions(userFunctions, bestIndex);
	size_t nodesBest = count(bestSolution.begin(), bestSolution.end(), ' ');
	cout << "Generation: " << generation << "\t Best Fitness: " << bestFitness << "\nSolution: " << bestSolution << endl <<"NODES: "<<nodesBest+1<< endl;
	return 0;
}