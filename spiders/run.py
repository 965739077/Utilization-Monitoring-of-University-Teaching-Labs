from wsgiref import headers

from bs4 import BeautifulSoup

import requests
import re
import hashlib
import base64
import execjs
import time
import mysql.connector



def MD5_HEX(str):
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("demo01.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

class UESTC(object):
    image_url = "https://jwnew.hait.edu.cn/hngxyjw/cas/genValidateCode"
    url = "https://jwnew.hait.edu.cn/hngxyjw/custom/js/SetKingoEncypt.jsp"
    login_url = "https://jwnew.hait.edu.cn/hngxyjw/cas/logon.action"
    loginafter_url = "http://xjwnew.hait.edu.cn/hngxyjw/MainFrm.html"

    HEADERS = {
        'Host': "jwnew.hait.edu.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'Accept': "text/plain, */*; q=0.01",
        'Referer': "https://jwnew.hait.edu.cn/hngxyjw/cas/login.action",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9"
    }
    HEADERS1 = {
        'Host': "jwnew.hait.edu.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'Accept': "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9"
    }
    Headers = {
        'Accept': "text/plain, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.8",
        'Connection': "keep-alive",
        'Content-Length': "1124",
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "jwnew.hait.edu.cn",
        'Origin': "http://jwnew.hait.edu.cn",
        'Referer': "https://jwnew.hait.edu.cn/hngxyjw/cas/login.action",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        'X-Requested-With': "XMLHttpRequest"
    }

    def __init__(self, username, password):
        self.__session = requests.session()
        self.username = username
        self.password = password
        self.lists = []
        self.time = int(time.time())
        self.date = None
        self.week = None
        self.today = None

    def get_score(session):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="laboratory"
        )
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE token (id INT AUTO_INCREMENT PRIMARY KEY, building VARCHAR(255),classroom VARCHAR(255),unit VARCHAR(255),course_code VARCHAR(255),course_name VARCHAR(255),class_code VARCHAR(255),employee_code VARCHAR(255),teacher VARCHAR(255),student_count VARCHAR(255),campus VARCHAR(255),week VARCHAR(255),time VARCHAR(255),admin_class VARCHAR(255))")
        #url = 'https://jwnew.hait.edu.cn/hngxyjw/kbbp/dykb.qxkb.kc_data.jsp'
        url = 'https://jwnew.hait.edu.cn/hngxyjw/kbbp/dykb.qxkb.jsi_data2.jsp'
        # 这个data包含了所有项，但有些其实的非必须的
        formdata = {
            'xnxq': '2022,0',
            'xssj': 'xssj',
            'xsrq': 'xsrq',
            'xn': '2022',
            'xn1': '',
            '_xq': '',
            'xq_m': '1',
            'selXQ': '2',
            'selLF':'',
            'selJSLX':'08',
            'sybm':'',
            'selGS':'2',
            'chkXSDYRQ': 'on',
            'menucode_current': 'SB09'
        }
        headers = {'referer': 'https://jwnew.hait.edu.cn/hngxyjw/kbbp/dykb.qxkb.jsi.html?menucode=SB09'}
        # 使用session
        r = session.__session.post(url,data=formdata, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        cell_data = []
        for row in rows :
            cells = row.find_all('td')
            a1 = cells[0].text.strip()
            a2 = cells[1].text.strip()
            a3 = cells[2].text.strip()
            a4 = cells[3].text.strip()
            a5 = cells[4].text.strip()
            a6 = cells[5].text.strip()
            a7 = cells[6].text.strip()
            a8 = cells[7].text.strip()
            a9 = cells[8].text.strip()
            b1 = cells[9].text.strip()
            b2 = cells[10].text.strip()
            b3 = cells[11].text.strip()
            b5 = cells[12].text.strip()
            cell_data.append([a1, a2, a3, a4, a5, a6, a7, a8,a9,b1,b2,b3,b5])
        sql = "INSERT INTO token (building,classroom,unit,course_code,course_name,class_code,employee_code,teacher,student_count,campus,week,time,admin_class) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.executemany(sql, cell_data)
        mydb.commit()
        print(mycursor.rowcount, "record(s) inserted.")
    def login(self):

        username = self.username
        password = self.password
        txt_mm_expression = "12"
        txt_mm_userzh = "0"
        txt_mm_length = str(len(password))
        image = self.__session.get(self.image_url, headers=self.HEADERS)
        _sessionid = image.cookies.get("JSESSIONID")
        with open('img1.png', 'wb') as f:
            f.write(image.content)

        # 识别验证码
        import ddddocr
        ocr = ddddocr.DdddOcr(beta=True)
        with open("img1.png", 'rb') as f:
            image = f.read()
        res = ocr.classification(image)
        print(res)

        randnumber = res
        # randnumber = input("请输入验证码:\n")
        p_username = "_u" + randnumber
        p_password = "_p" + randnumber
        password1 = MD5_HEX(MD5_HEX(password) + MD5_HEX(randnumber))
        username1 = username + ";;" + _sessionid
        username1 = str(base64.b64encode(username1.encode("utf-8")), "utf-8")
        rep = self.__session.get(self.url, headers=self.HEADERS)
        text = rep.text
        _deskey = re.search(r"var _deskey = '(.*?)';", text)
        _nowtime = re.search(r"var _nowtime = '(.*?)';", text)
        parms = p_username + "=" + username1 + "&" + p_password + "=" + password1 + "&randnumber=" + randnumber + "&isPasswordPolicy=1" + "&txt_mm_expression=" + txt_mm_expression + "&txt_mm_length=" + txt_mm_length + "&txt_mm_userzh=" + txt_mm_userzh
        token = MD5_HEX(MD5_HEX(parms) + MD5_HEX(_nowtime.group(1)))
        jsstr = get_js()
        ctx = execjs.compile(jsstr)
        _parms = str(base64.b64encode(ctx.call('strEnc', parms, _deskey.group(1)).encode("utf-8")), "utf-8")
        data = 'params=' + _parms + '&token=' + token + "&timestamp=" + _nowtime.group(1)
        # data = 'params='+'&token='+"&timestamp="+_nowtime.group(1)
        res = self.__session.post(self.login_url, headers=self.Headers, data=data)
        print(res.text)


    def run(self):
        self.login()
        # self.evaluate()
        self.get_score()
if __name__ == '__main__':
    # def run_():
    username = input('请输入用户名:\n')
    password = input('请输入密码:\n')
    spider = UESTC(username, password)
    spider.run()
