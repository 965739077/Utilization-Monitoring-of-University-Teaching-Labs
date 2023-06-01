import re
from flask import Flask, request, render_template, session, redirect, jsonify
from utils import query
from utils.getHomeData import *
from utils.getSearch import *
from utils.Datatimes import *
from utils.chart import *
app = Flask(__name__)
app.secret_key = 's'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        def filter_fn(item):
            return request.form['email'] in item and request.form['password'] in item
        users = query.querys('select * from user',[],'select')
        filter_user = list(filter(filter_fn,users))
        if len(filter_user):
            session['email'] = request.form['email']
            return redirect('/Auto')
        else:
            return render_template('error.html',message='邮箱或密码错误')
@app.route('/laginOut')
def loginOut():
    session.clear()
    return redirect('/login')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        print(request.form)
        if request.form['password'] != request.form['passwordChecked']:
            return render_template('error.html',message='两次密码不符合')
        def filter_fn(item):
            return request.form['email'] in item
        users = query.querys('select * from user',[],'select')
        filter_list = list(filter(filter_fn,users))
        if len(filter_list):
            return render_template('error.html',message='该用户已被注册')
        else:
            query.querys('insert into user(email,password) values(%s,%s)',[request.form['email'],request.form['password']])
            return redirect('/login')
@app.route('/home',methods=['GET','POST'])
def home():
    email = session.get('email')
    typesEcharts = getTypesEcharts()
    rows, coloumn =getDatatimeEcharts()
    tabledata = getTableData()
    maxClass,maxB3,maxA2,minA2 = getHomeData()
    return render_template(
        'index.html',
        email=email,
        maxClass=maxClass, maxB3=maxB3, maxA2=maxA2, minA2=minA2,typesEcharts=typesEcharts,
        rows=rows,
        coloumn=coloumn,
        tabledata=tabledata
    )

@app.before_request
def before_requre():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == "/login":
        return
    if request.path == "/register":
        return
    email = session.get('email')
    if email:
        return None
    return redirect('/login')

@app.route('/')
def allRequest():
    return redirect('/login')


@app.route('/Auto',methods=['GET','POST'])
def Auto():
    # 获取当前的本地时间
    local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    email = session.get('email')
    # 连接数据库，并查询 datatimes 表中的所有记录
    maxClass, maxB3, maxA2, minA2 = getHomeData()
    date_str = datetime.now().strftime('%Y-%m-%d')
    # 比较本地时间和每条记录的开始时间和结束时间，判断哪些记录正在使用
    mask = (df2['start'] <= local_time) & (df2['end'] >= local_time)
    in_use_df = df2[mask]
    # 获取 datatimes 表中记录，该记录有一个对应的 text_id
    datatimes_records = in_use_df.to_dict(orient='records')
    # 从 datatimes 记录中获取 text_id
    in_text_records = []
    for datatimes_record in datatimes_records:
        text_id = datatimes_record['id']
        text_record = pd.read_sql("SELECT * FROM token WHERE id = %(text_id)s", con=con, params={'text_id': text_id})
        in_text_record = text_record.to_dict(orient='records')
        in_text_records.extend(in_text_record)
    # 去除重复的记录
    in_text_records = list(set([tuple(record.items()) for record in in_text_records]))
    in_text_records = [dict(record) for record in in_text_records]
    # 将正在使用的记录传递到 Auto 页面上
    in_use_data = in_use_df.to_dict(orient='records')
    #获取排行榜
    chart_row,char_colomn = get_chart_data()
    types123 = getTypesEcharts1()
    ro, col = getDatatimeEcharts1()
    # 渲染 Auto 页面，并将本地时间和正在使用的记录传递到页面上
    return render_template('Auto.html',types123=types123,ro=ro,col=col,chart_row=chart_row, char_colomn=char_colomn,local_time=local_time, in_use_data=in_use_data,date_str=date_str,email=email,maxClass=maxClass, maxB3=maxB3, maxA2=maxA2, minA2=minA2,in_text_records=in_text_records)

@app.route('/search/<int:classId>',methods=['GET','POST'])
def search(classId):
    email = session.get('email')
    if request.method == 'GET':
        resultData = getClassId(classId)
    else:
        request.form = dict(request.form)
        resultData = getClassData(request.form['searchData'])

    return render_template('search.html',resultData=resultData,email=email)

@app.route('/classroom-usage', methods=['POST'])
def get_classroom_usage():
    week = request.json['week']
    weekday = request.json['weekday']

    # 查询数据库获取教室使用情况
    connection = query()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name, week, time FROM token WHERE week=%s AND time LIKE %s"
            cursor.execute(sql, (week, f'%{weekday}%'))
            result = cursor.fetchall()
    finally:
        connection.close()

    # 构造响应数据
    data = []
    for row in result:
        classroom = {}
        classroom['name'] = row['name']
        classroom['usage'] = '空闲' if row['b2'] == '0' else '占用'
        data.append(classroom)

    return jsonify(data)
if __name__ == '__main__':
    app.run()
