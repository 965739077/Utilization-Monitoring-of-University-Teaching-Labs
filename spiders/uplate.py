import pymysql
import pandas as pd
import datetime

# 连接数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='laboratory')
cursor = conn.cursor()

# 创建datatimes表
cursor.execute('CREATE TABLE IF NOT EXISTS datatimes (id INT NOT NULL, start DATETIME NOT NULL, end DATETIME NOT NULL)')

# 查询数据
cursor.execute('SELECT id, week, time FROM token')
data = cursor.fetchall()


# 定义每节课的时间范围
time_range = {
    1: (datetime.time(8, 0), datetime.time(8, 50)),
    2: (datetime.time(9, 00), datetime.time(9, 50)),
    3: (datetime.time(10, 10), datetime.time(11, 00)),
    4: (datetime.time(11, 10), datetime.time(12, 00)),
    5: (datetime.time(14, 30), datetime.time(15, 20)),
    6: (datetime.time(15, 30), datetime.time(16, 20)),
    7: (datetime.time(16, 40), datetime.time(17, 30)),
    8: (datetime.time(17, 40), datetime.time(18, 30)),
    9: (datetime.time(19, 30), datetime.time(20, 20)),
    10: (datetime.time(20, 30), datetime.time(21, 30))
}


# 处理数据并生成日期列表
date_list = []
for d in data:
    if d[1] is not None and d[2] is not None:
        week_range_list = d[1].split(',')
        time_range_str = d[2].replace('[', '')
        day = time_range_str[0]
        time_range_list = time_range_str[1:-1].split('-')
        start_time = int(time_range_list[0])
        end_time = int(time_range_list[1])
        chinese_weekdays = {'一': 'Monday', '二': 'Tuesday', '三': 'Wednesday', '四': 'Thursday', '五': 'Friday',
                            '六': 'Saturday', '日': 'Sunday'}
        weekday1 = chinese_weekdays[day]
        for week_range in week_range_list:
            if '-' in week_range:
                week_str = week_range.replace('单', '').replace('双', '')
                start_week, end_week = week_str.split('-')
            else:
                start_week = end_week = week_range.replace('单', '').replace('双', '')
            for week_range in week_range_list:
                if '-' in week_range:
                    week_str = week_range.replace('单', '').replace('双', '')
                    start_week, end_week = week_str.split('-')
                else:
                    start_week = end_week = week_range.replace('单', '').replace('双', '')
            for i in range(int(start_week), int(end_week) + 1):
                date = datetime.date(2023, 2, 20) + datetime.timedelta(
                    days=(i - 1) * 7 + (datetime.datetime.strptime(weekday1, '%A').weekday() + 1))
                start_datetime = datetime.datetime.combine(date, time_range[start_time][0])
                end_datetime = datetime.datetime.combine(date, time_range[end_time][1])
                date_list.append([d[0], start_datetime, end_datetime])
                # 插入数据到datatimes表
                cursor.execute('INSERT INTO datatimes (id, start, end) VALUES (%s, %s, %s)',
                               (d[0], start_datetime, end_datetime))
# 提交事务并关闭连接

conn.commit()
cursor.close()
conn.close()
"""
# 生成excel表格
df = pd.DataFrame(date_list, columns=['id', 'start_time', 'end_time'])
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
"""
