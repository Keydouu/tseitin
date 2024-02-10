import copy
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
            half1.getElements().append(copy.deepcopy(a))
            half1.getElements().append(copy.deepcopy(b))
            half1.toCNF()
            self.elements.append(half1)
            a.negate()
            b.negate()
            half2=GenericObj()
            half2.setType("&")
            half2.getElements().append(a)
            half2.getElements().append(b)
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
            else:
                print("???")
        for s in str.split(self.type):
            if len(s)>0:
                self.elements.append(Singleton(s))
    def spreadObject(self, obj):
        self.elements.append(obj)
        return self
    def toCNF(self):
        self.removeArrows()
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
        for ele in self.elements:
            if len(ele.getElements())>1:
                ele.setElements(ensure_unique(ele.getElements()))
        self.elements=ensure_unique(self.elements)
    def getType(self):
        return self.type
    def getElements(self):
        return self.elements
    def setElements(self, newElements):
        self.elements = newElements
    def contain(self, input):
        for ele in self.elements:
            if ele.toString()==input:
                return True
        return False
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
    def __repr__(self):
        return self.name

def ensure_unique(arr):
    unique_elements = []
    for element in arr:
        if element not in unique_elements:
            unique_elements.append(element)
    return unique_elements

def readSimpleStr(str):
    if "|" in str or "&" in str:
        return GenericObj(str)
    else:
        return Singleton(str)