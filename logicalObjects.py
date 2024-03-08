import copy
allSingletons=[]
freshVarsMap={}
freshVar="Y"
class GenericObj:
    def __init__(self, str=""):
        self.isCNF=False
        self.type="none"
        self.elements=[]
        if "&" in str:
            self.type="&"
        elif "|" in str:
            self.type="|"
        if "<=>" in str:
            self.type="<=>"
        elif "=>" in str:
            self.type="=>"
        elif "<=" in str:
            self.type="<="
        if self.type!="none":
            for s in str.split(self.type):
                if len(s)>0:
                    self.elements.append(Singleton(s))
        elif len(str)>0:
            self.elements.append(Singleton(str))
    def removeArrows(self):
        if self.type=="<=>":
            if len(self.elements)!=2:
                print("input error, except random result")
            a=self.elements[0]
            b=self.elements[1]
            self.elements=[]
            self.type="|"
            half1=GenericObj()
            half1.setType("&")
            a2=copy.deepcopy(a)
            b2=copy.deepcopy(b)
            half1.getElements().append(a)
            half1.getElements().append(b)
            half1.toCNF()
            self.elements.append(half1)
            a2.negate()
            b2.negate()
            half2=GenericObj()
            half2.setType("&")
            half2.getElements().append(a2)
            half2.getElements().append(b2)
            half2.toCNF()
            self.elements.append(half2)
            self.elements=ensure_unique(self.elements)
        elif self.type=="=>":
            self.type="|"
            if len(self.elements)!=2:
                print("input error, except random result")
            self.elements[0].negate()
        elif self.type=="<=":
            self.type="|"
            if len(self.elements)!=2:
                print("input error, except random result")
            self.elements[1].negate()
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
            elif "<=>" in str:
                self.type="<=>"
            elif "=>" in str:
                self.type="=>"
            elif "<=" in str:
                self.type="<="
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
        self.removeArrows()
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
        for ele in self.elements:
            if len(ele.getElements())>1:
                ele.setElements(ensure_unique(ele.getElements()))
        self.elements=ensure_unique(self.elements)
        cnfSimplifier(self)
    def toTseiten(self, finalOutput=True):
        if len(self.elements)==1:
            return self.elements[0].toTseiten(finalOutput)
        freshChildren=[]
        for element in self.elements:
            freshChildren.append(element.toTseiten(False))
        self.elements=freshChildren
        self.defineFreshVar()
        if not finalOutput:
            return self.freshVariable
        FinalObj.toCNF()
        FinalObj.getElements().append(self.freshVariable)
        return FinalObj
    def defineFreshVar(self):
        a = self.toString()
        if not ( a in freshVarsMap ):
            self.freshVariable = Singleton(freshVar+str(len(freshVarsMap)+1))
            freshVarsMap[a] = self.freshVariable
            tmp = GenericObj()
            tmp.setType("<=>")
            tmp.getElements().append(self.freshVariable)
            tmp.getElements().append(self)
            FinalObj.getElements().append(tmp)
        else :
            self.freshVariable = freshVarsMap[a]
    def getType(self):
        return self.type
    def getElements(self):
        return self.elements
    def setElements(self, newElements):
        self.elements = newElements
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
    def __repr__(self):
        return self.toString()
    def getDimacs(self):
        output="p cnf "+str(len(allSingletons))+" "+str(len(self.elements))
        for element in self.elements:
            output = output + "\n" + element.asDimacsClause()+" 0"
        return output
    def asDimacsClause(self):
        output=""
        for element in self.elements:
            output = output + " " + element.asDimacsClause()
        if output != "":
            output = output[1:]
        return output
class Singleton:
    def __init__(self, name):
        if not (pureName(name) in allSingletons): 
            allSingletons.append(pureName(name))
        self.index = allSingletons.index(pureName(name))
        self.name = name
        self.type="singleton"
    def asDimacsClause(self):
        if self.name[0]=='!':
            return str((allSingletons.index(self.name[1:])+1)*-1)
        else:
            return str(allSingletons.index(pureName(self.name))+1)
    def toTseiten(self, finalOutput=True):
        if finalOutput:
            return self
        return self
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
    def __repr__(self):
        return self.name

def pureName(name):
    if name[0]=='!':
            return name[1:]
    return name

def setFreshVariableName(name):
    freshVar=name
def ensure_unique(arr):
    unique_elements = []
    for element in arr:
        if element not in unique_elements:
            unique_elements.append(element)
    return unique_elements

FinalObj = GenericObj()
FinalObj.setType("&")

def cnfSimplifier(cnf):
    newFormulaElements=[]
    for ele in cnf.getElements():
        if not checkTautologie(ele):
            newFormulaElements.append(ele)
    if len(newFormulaElements)==0:
        return Singleton("T")
    cnf.setElements(newFormulaElements)
    for ele in cnf.getElements():
        if ele.getType()!="singleton":
            ele.setElements(ensure_unique(ele.getElements()))
    return cnf
def checkTautologie(f):
    if f.getType()=="singleton":
        return False
    formulaAsArray=f.toString()[1:-1].split("|")
    for ele in formulaAsArray:
        if "!"+ele in formulaAsArray:
            return True
    return False