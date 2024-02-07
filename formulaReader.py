import copy
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
    #print(totalMap["0"].toString()[1:-1])
    if totalMap["0"].getType()=="none":
        totalMap["0"].setType("|")
    result=toTseiten(totalMap["0"])
    input=totalMap['0'].toString()
    if not '(' in input:
        input='('+ input+')'
    print(f"tseitin{input} = ( {freshVariableName}, {result.toString()[1:]}")

def bracketsClosed(index, unfinished, totalMap, input):
    current=totalMap[str(index)]
    unfinished.remove(index)
    while not(index in unfinished) and index!=0:
        index-=1
    totalMap[str(index)]=totalMap[str(index)].spreadObject(current)
    totalMap[str(index)].addString(input.split(")")[0])
def toTseiten(obj):
    obj2=copy.deepcopy(obj)
    obj2.negate()
    tseiten=grouper(grouper(obj2, Singleton(freshVariableName)), grouper(obj, Singleton('!'+freshVariableName)), '&')
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

class GenericObj:
    def __init__(self, str=""):
        self.type="none"
        self.elements=[]
        if "&" in str:
            self.type="&"
        elif "|" in str:
            self.type="|"
        if self.type!="none":
            for s in str.split(self.type):
                if len(s)>0:
                    self.elements.append(Singleton(s))
        elif len(str)>0:
            self.elements.append(Singleton(str))
    def negate(self):
        for i in self.elements:
            i.negate()
        if self.type=="&":
            self.type="|"
        elif self.type=="|":
            self.type="&"
    def addString(self, str):
        if self.type=="none":
            if "&" in str:
                self.type="&"
            elif "|" in str:
                self.type="|"
            else:
                print("???")
        for s in str.split(self.type):
            if len(s)>0:
                self.elements.append(Singleton(s))
    def spreadObject(self, obj):
        self.elements.append(obj)
        return self
    def toCNF(self):
        for ele in self.elements:
            ele.toCNF()
        newElements=[]
        if self.type=="&":#simple grouping
            for ele in self.elements:
                for ele2 in ele.getElements():
                    newElements.append(ele2)
            self.elements=newElements
        elif self.type=="|":# a | b | ( c & d) |( (e | f) & (g | h))
            tmp=GenericObj()
            tmp.setType("|")
            tmpArray=tmp.getElements()
            for ele in self.elements:
                if ele.getType()=="singleton":
                    tmpArray.append(ele)
                elif ele.getType()=="|":
                    for ele2 in ele.getElements():
                        tmpArray.append(ele2)
            newSelf=GenericObj()
            newSelf.setType("&")
            newSelf.getElements().append(tmp)
            for ele in self.elements:#for every child ( OR between them)
                if ele.getType()=="&":# contain AND
                    newElements=copy.deepcopy(newSelf.getElements())
                    newSelf.getElements().clear()
                    for ele2 in ele.getElements():#for every grand child ( contain OR )
                        for ne in newElements:
                            tmp=copy.deepcopy(ne).getElements()
                            for ele3 in ele2.getElements():#for every greater grand child ( OR between them)
                                tmp.append(ele3)
                            tmpObj=GenericObj()
                            tmpObj.setType("|")
                            tmpObj.elements=tmp
                            newSelf.getElements().append(tmpObj)
                    newElements.clear()
            self.setType("&")
            self.elements=newSelf.getElements()
        else:
            print("unknown error")
    def getType(self):
        return self.type
    def getElements(self):
        return self.elements
    def setType(self, newType):
        self.type=newType
    def toString(self):
        if self.type=="none":
            return "NULL"
        if len(self.elements)==1:
            return self.elements[0].toString()
        output="("
        for ele in self.elements:
            if len(output)>1:
                output+=self.type
            output+=ele.toString()
        return output+")"
    def __str__(self):
        return self.toString()
class Singleton:
    def __init__(self, name):
        self.name = name
        self.type="singleton"
    def getNegatedName(self):
        if self.name[0]=='!':
            return self.name[1:]
        else:
            return "!"+self.name
    def negate(self):
        if self.name[0]=='!':
            self.name=self.name[1:]
        else:
            self.name="!"+self.name
    def toCNF(self):
        return
    def getType(self):
        return self.type
    def getElements(self):
        return [self]
    def toString(self):
        return self.name
    def __str__(self):
        return self.name
mymain("(p&r)|(!p|!r)")
#mymain("a&b")