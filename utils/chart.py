import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/laboratory')

def get_chart_data():
    # 获取本周的起始日期和结束日期
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # 获取本周使用的 datatimes 表中的 id
    datatimes = pd.read_sql(f"select id from datatimes where start >= '{start_date}' and end <= '{end_date}'", engine)
    ids = datatimes['id'].tolist()

    # 查询 token 表中对应的 classroom 字段
    classrooms = pd.read_sql(f"select building from token where id in ({','.join(map(str, ids))})", engine)
    # 查询 token 表中对应的 classroom 字段
    classrooms1 = pd.read_sql(f"select classroom from token where id in ({','.join(map(str, ids))})", engine)
    # 统计使用次数，并存储在字典中
    # 统计使用次数，并存储在字典中
    result=classrooms['building'].map(lambda x: str(x)).values
    classObj2 = {}
    for i in result:
        if classObj2.get(i, -1) == -1:
            classObj2[i] = 1
        else:
            classObj2[i] = classObj2[i] + 1
    # 对字典按照值进行排序
    sorted_classObj2 = sorted(classObj2.items(), key=lambda item: item[1], reverse=True)
    print(sorted_classObj2)
    # 获取排名列表和使用次数列表
    rank_list = [item[0] for item in sorted_classObj2]
    use_count_list = [item[1] for item in sorted_classObj2]
    return rank_list, use_count_list

def getTypesEcharts1():
    # 获取本周的起始日期和结束日期
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # 获取本周使用的 datatimes 表中的 id
    datatimes = pd.read_sql(f"select id from datatimes where start >= '{start_date}' and end <= '{end_date}'", engine)
    ids = datatimes['id'].tolist()

    # 查询 token 表中对应的 classroom 字段
    unit = pd.read_sql(f"select unit from token where id in ({','.join(map(str, ids))})", engine)
    typeList =unit['unit'].map(lambda x: str(x)).values
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

def getDatatimeEcharts1():
    # 获取本周的起始日期和结束日期
    today = datetime.now().date()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)

    # 获取本周使用的 datatimes 表中的 id
    datatimes = pd.read_sql(f"select id from datatimes where start >= '{start_date}' and end <= '{end_date}'", engine)
    ids = datatimes['id'].tolist()

    # 查询 token 表中对应的 classroom 字段
    unit = pd.read_sql(f"select unit from token where id in ({','.join(map(str, ids))})", engine)
    classList = unit['unit'].map(lambda x:str(x)).values
    classObj = {}
    for i in classList:
        if classObj.get(i, -1) == -1:
            classObj[i] = 1
        else:
            classObj[i] = classObj[i] + 1
    return list(classObj.keys()),list(classObj.values())

getTypesEcharts1()