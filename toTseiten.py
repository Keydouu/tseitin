import copy
from logicalObjects import GenericObj, setFreshVariableName
import sys

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
        j=i
        while ")" in ele:
            ele=ele.split(")",1)[1]
            bracketsClosed(j, unfinished, totalMap, ele)
            while not(j in unfinished) and j!=0:
                j-=1
    if totalMap["0"].getType()=="none":
        totalMap["0"].setType("|")
    fullResult=totalMap["0"].toTseiten()
    toPrint=fullResult.toString()
    if '(' in toPrint:
        toPrint=fullResult.toString()[1:-1]
    print(toPrint)

def bracketsClosed(index, unfinished, totalMap, input):
    current=totalMap[str(index)]
    unfinished.remove(index)
    while not(index in unfinished) and index!=0:
        index-=1
    totalMap[str(index)]=totalMap[str(index)].spreadObject(current)
    totalMap[str(index)].addString(input.split(")")[0])


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("Usage: python toTseiten.py <input_string> <fresh_variable_name>")
        sys.exit(1)
    input_string = sys.argv[1]
    if len(sys.argv) > 2:
        setFreshVariableName(sys.argv[2])
    mymain(input_string)