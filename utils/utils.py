import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://root:123456@localhost:3306/laboratory')

df = pd.read_sql('select * from token',con=con)
df2 = pd.read_sql('select * from datatimes',con=con)
def typelist(type):
    type = df[type].fillna('').values
    type = list(map(lambda x:x.split(','),type))
    typelist = []
    for i in type:
        for j in i:
            typelist.append(j)
    return typelist
def typelist2(type):
    type = df2[type].fillna('').values
    type = list(map(lambda x:x.split(','),type))
    typelist2 = []
    for i in type:
        for j in i:
            typelist2.append(j)
    return typelist2