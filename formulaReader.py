import copy
from logicalObjects import GenericObj, Singleton
from formulaSimplifier import checkTruthTable
freshVariableName="Yns"
def mymain(input):
    input=input.replace(" ","")
    splited=input.split('(')
    totalMap={}
    unfinished=[]
    for i in range(len(splited)):
        unfinished.append(i)
        tmp=splited[i].split(")",1)
        totalMap[str(i)]=GenericObj(tmp[0])
        ele=splited[i]
        while ")" in ele:
            ele=ele.split(")",1)[1]
            bracketsClosed(i, unfinished, totalMap, ele)
    if totalMap["0"].getType()=="none":
        totalMap["0"].setType("|")
    result=toTseiten(totalMap["0"])
    toPrint=result.toString()
    if not '(' in toPrint:
        toPrint=toPrint+')'
    else:
        toPrint=toPrint[1:]
    print(f"tseitin({input}) = ( {freshVariableName}, {toPrint}")

def bracketsClosed(index, unfinished, totalMap, input):
    current=totalMap[str(index)]
    unfinished.remove(index)
    while not(index in unfinished) and index!=0:
        index-=1
    totalMap[str(index)]=totalMap[str(index)].spreadObject(current)
    totalMap[str(index)].addString(input.split(")")[0])
def toTseiten(input):
    input.toCNF()
    obj=copy.deepcopy(input)
    obj=checkTruthTable(obj)
    if obj.toString()=="T":
        output=Singleton(freshVariableName)
        return output
    elif obj.toString()=="!T":
        output=Singleton("!"+freshVariableName)
        return output
    obj2=copy.deepcopy(obj)
    obj2.negate()
    obj2=checkTruthTable(obj2)
    if obj2.toString()=="T":
        output=Singleton("!"+freshVariableName)
        return output
    elif obj2.toString()=="!T":
        output=Singleton(freshVariableName)
        return output
    posClause=grouper(obj2, Singleton(freshVariableName))
    negClause=grouper(obj, Singleton('!'+freshVariableName))
    tseiten=grouper(posClause, negClause, '&')
    tseiten.toCNF()
    return tseiten
def grouper(obj1, obj2, type="|"):
    parentObj=GenericObj()
    parentObj.setType(type)
    if obj1.getType()==type:
        for ele in obj1.getElements():
            parentObj.getElements().append(ele)
    else:
        parentObj.getElements().append(obj1)
    if obj2.getType()==type:
        for ele in obj2.getElements():
            parentObj.getElements().append(ele)
    else:
        parentObj.getElements().append(obj2)
    return parentObj

tests = ['!p', 'p&r' , '(p&r)|(!p|!r)', 'p<=>(p&r)']
for test in tests:
    mymain(test)
#mymain('p<=>(p&r)')
#mymain("a&b")