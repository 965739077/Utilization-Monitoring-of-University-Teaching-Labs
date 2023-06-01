from .utils import *

def getClassId(classId):
    tableData = df.values
    resultData = []
    for i in tableData:
        print(i[0],classId)
        if i[0] == classId:
            resultData.append(list(i))
    return resultData
def getClassData(searchData):
    tableData = df.values
    resultData = []
    for i in tableData:
        if i[13].find(searchData) != -1:
            resultData.append(i)
    return resultData