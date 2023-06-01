from .utils import *

def getHomeData():
    maxClass = len(df.values) #实验室使用总次数
    counts = df["classroom"].value_counts()
    minA2 = counts.idxmin()#使用最少的实验室
    maxA2 = counts.idxmax()#使用最多的实验室
    counts1 = df2["start"].value_counts()
    maxB3 = counts1.idxmax()#实验室使用峰值
    return maxClass,maxB3,maxA2,minA2
    #实验室直接利用率 =（学期实验学时数 / 实验室额定学时数）×100 %
def getTypesEcharts():
    typeList =typelist('unit')
    typeObj = {}
    for i in typeList:
        if typeObj.get(i,-1) == -1:
            typeObj[i]=1
        else:
            typeObj[i]=typeObj[i]+1
    typesEcharts = []
    for key,value in typeObj.items():
        typesEcharts.append({
            'name':key,
            'value':value
        })
    return typesEcharts

def getDatatimeEcharts():
    classList = df['unit'].map(lambda x:str(x)).values
    classObj = {}
    for i in classList:
        if classObj.get(i, -1) == -1:
            classObj[i] = 1
        else:
            classObj[i] = classObj[i] + 1
    return list(classObj.keys()),list(classObj.values())

def getTableData():
    return df.values
