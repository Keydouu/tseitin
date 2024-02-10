from logicalObjects import GenericObj, Singleton
from pycsp3 import *
import os
def checkTruthTable(cnf):
    cnf.toCNF()
    newFormulaElements=[]
    for ele in cnf.getElements():
        if not checkTautologie(ele):
            newFormulaElements.append(ele)
    if len(newFormulaElements)==0:
        return Singleton("T")
    cnf.setElements(newFormulaElements)
    if not solve_cnf(cnf):
        return Singleton("!T")
    return cnf
def checkTautologie(f):
    if f.getType()=="singleton":
        return False
    formulaAsArray=f.toString()[1:-1].split("|")
    for ele in formulaAsArray:
        if "!"+ele in formulaAsArray:
            return True
    return False
def solve_cnf(cnf):
    variablesMap = {}
    i=0
    varName = lambda literal: literal.toString().replace("!", "")
    varIndex = lambda literal : variablesMap[varName(literal)]
    sign = lambda s: 0 if '!' in s.toString() else 1
    for clause in cnf.getElements():
        for literal in clause.getElements():
            if not varName(literal) in variablesMap:
                variablesMap[varName(literal)] = i
                i+=1
    variables=VarArray(size=len(variablesMap), dom={0 , 1})
    satisfy(
        [ sum(variables[varIndex(literal)] == sign(literal) for literal in clause.getElements())>=1 for clause in cnf.getElements()]
    )
    result = solve()
    clear()
    delete_logs()
    if result == UNSAT:
        return False
    return True
def delete_logs():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    for file in files:
        if file.endswith(".log") or file.endswith("formulaReader.xml"):
            file_path = os.path.join(current_directory, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")