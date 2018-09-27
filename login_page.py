# -*-coding:utf-8 -*-
import time
from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
import pymysql

import captcha

app = Flask(__name__)
Bootstrap(app)

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='cui123', db='bootstrap', charset='utf8')
cursor = conn.cursor()


@app.route('/login', methods=['GET'])
def index_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def index_post():
    email_tem = request.form['email']
    sql_email = "select * from user where email='{0}'".format(email_tem)
    cursor.execute(sql_email)
    email = cursor.fetchall()
    sql_user = "select * from user"
    cursor.execute(sql_user)
    users = cursor.fetchall()
    if not email:
        return render_template('login.html', state='没有此用户，快滚！', email_re=request.form['email'])
    if request.form['email'] == email[0][1] and request.form['password'] == email[0][2]:
        return render_template('bbs_index.html', email_re=request.form['email'], users=users)
    else:
        return render_template('login.html', state='登陆失败,密码错误', email_re=request.form['email'])


@app.route('/', methods=['GET'])
def bbs_index():
    return render_template('bbs_index.html')


@app.route('/register', methods=['GET'])
def register_get():
    image, captcha_str = captcha.captcha()
    img_name = 'static/images/{}.jpg'.format(time.time())
    print(img_name)
    image.save(img_name, 'jpeg')
    print(captcha_str)
    return render_template('register.html', img_name=img_name, captcha_str=captcha_str)


# @app.route('/register', methods=['POST'])
# def register_post():
#     email_tem = request.form['email']
#     password_tem = request.form['password']
#     captcha_tem = request.form['captcha'].upper()
#     captcha_str = request.form['captcha_str']
#     img_name = request.form['img_name']
#     if captcha_tem != captcha_str:
#         return render_template('register.html', state='验证码错误', email_re=request.form['email'], img_name=img_name,
#                                captcha_str=captcha_str)
#     sql = "select * from user where email='{0}'".format(email_tem)
#     cursor.execute(sql)
#     email = cursor.fetchall()
#     if email:
#         return render_template('register.html', state='此用户已注册！大傻子！', email_re=request.form['email'], img_name=img_name,
#                                captcha_str=captcha_str)
#     sql = "INSERT INTO user(email,password) VALUES('{0}','{1}')".format(email_tem, password_tem)
#     cursor.execute(sql)
#     print(sql)
#     conn.commit()
#     return render_template('register.html', state='注册成功', email_re=request.form['email'], img_name=img_name,
#                            captcha_str=captcha_str)


if __name__ == '__main__':
    app.run(debug=True)
