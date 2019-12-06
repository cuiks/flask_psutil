# -*- coding: utf-8 -*-
import time

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import psutil
from flask_login import login_required, logout_user, login_user, current_user
import threading
from flask_socketio import SocketIO

from post_email import add_info
from exts import db, login_manger
from models import Role, Cpu_status
from forms import LoginForm
from save_status import save_cpu
import captcha
from tongyong import zbx_req
from Fabrics import fabfile

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = threading.Lock()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:***@127.0.0.1/bootstrap'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

is_login = ''

th_saveCpu = threading.Thread(target=save_cpu)
th_saveCpu.start()


@app.route('/user')
def user_form():
    if is_login == '':
        return redirect(url_for('login_get'))
    pids = psutil.pids()
    pro_list = []
    pro = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
            pro_list.append([p.name(), p.status(), p.create_time()])
        except Exception as e:
            print(e)
    return render_template('users.html', pro_list=pro_list, user=is_login)


@app.route('/disk')
def disk():
    if is_login == '':
        return redirect(url_for('login_get'))
    disk_list = psutil.disk_partitions()
    disk_lists = []
    for i, dis in enumerate(disk_list):
        disk_lists.append([i + 1, psutil.disk_usage(dis.device)])
    disk_listss = []
    i = 0
    while i < len(disk_lists):
        if i + 1 < len(disk_lists):
            disk_listss.append([disk_lists[i], disk_lists[i + 1]])
        else:
            disk_listss.append([disk_lists[i], ''])
        i += 2
    print(disk_lists)
    return render_template('disk.html', disk_list=disk_listss, user=is_login)


@app.route('/memory')
def memory():
    if is_login == '':
        return redirect(url_for('login_get'))
    total = str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2))
    free = str(round(psutil.virtual_memory().free / (1024 * 1024 * 1024), 2))
    used = str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2))
    return render_template('memory.html', total=total, free=free, used=used, user=is_login)


@app.route('/net')
def net():
    if is_login == '':
        return redirect(url_for('login_get'))
    net = psutil.net_io_counters()
    recv = round(net.bytes_recv / (1024 * 1024), 2)
    recverr = round(net.errin / (1024 * 1024), 2)
    sent = round(net.bytes_sent / (1024 * 1024), 2)
    senterr = round(net.errout / (1024 * 1024), 2)
    return render_template('net.html', recv=recv, sent=sent, senterr=senterr, recverr=recverr, user=is_login)


send_count = 0


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    global send_count
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        add_time = int(time.time() * 1000)
        cpu_used = psutil.cpu_percent(interval=None)
        if cpu_used >= 80 and send_count == 0:
            print('cpu_used:', cpu_used)
            time.sleep(5)
            data = []
            with app.app_context():
                reload_data = db.session.quewszeAry(Cpu_status).order_by('-id').limit(20).all()
                for i in reload_data:
                    data.append([float(i.add_time), float(i.cpu_used)])
                print(data)
            add_info(data)
            send_count += 1
        socketio.emit('server_response', {'cpu_used': cpu_used, 'add_time': add_time}, namespace='/get_datas')


@app.route('/cpu')
def cpu():
    if is_login == '':
        return redirect(url_for('login_get'))

    return render_template('cpu.html', async_mode=socketio.async_mode, user=is_login)


# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/get_datas')
def test_connect():
    # print('调用了')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


@app.route('/index', methods=['GET'])
def index_get():
    return render_template('index.html', user=is_login)


@app.route('/index', methods=['POST'])
def index_post():
    zbx_params = request.form['zbx_params']
    results = zbx_req(zbx_params)
    return render_template('index.html', user=is_login, results=results)


@app.route('/', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login_post():
    global is_login
    email_tem = request.form['email']
    print(email_tem)
    result = db.session.query(Role).filter_by(email=email_tem).first()
    # print('result:', result)
    if not result:
        return render_template('login.html', state='没有此用户', email_re=request.form['email'])
    if request.form['email'] == result.email and request.form['password'] == result.password:
        is_login = email_tem
        return render_template('index.html')
    else:
        return render_template('login.html', state='登陆失败,密码错误', email_re=request.form['email'])


@app.route('/logout')
def logout():
    global is_login
    # 用户登出
    is_login = ''
    return redirect(url_for('login_get'))


@app.route('/register', methods=['GET'])
def register_get():
    image, captcha_str = captcha.captcha()
    img_name = 'static/images/{}.jpg'.format(time.time())
    print(img_name)
    image.save(img_name, 'jpeg')
    print(captcha_str)
    return render_template('register.html', img_name=img_name, captcha_str=captcha_str)


@app.route('/register', methods=['POST'])
def register_post():
    email_tem = request.form['email']
    password_tem = request.form['password']
    captcha_tem = request.form['captcha'].upper()
    captcha_str = request.form['captcha_str']
    img_name = request.form['img_name']
    if captcha_tem != captcha_str:
        return render_template('register.html', state='验证码错误', email_re=request.form['email'], img_name=img_name,
                               captcha_str=captcha_str)
    email = db.session.query(Role).filter_by(email=email_tem).first()
    if email:
        return render_template('register.html', state='此用户已注册!', email_re=request.form['email'], img_name=img_name,
                               captcha_str=captcha_str)
    user_add = Role(email=email_tem, password=password_tem)
    db.session.add(user_add)
    db.session.commit()
    return render_template('register.html', state='注册成功', email_re=request.form['email'], img_name=img_name,
                           captcha_str=captcha_str)


@app.route('/fabric', methods=['POST'])
def fabric():
    command = request.form['comm_text']
    print(command)
    comm_result = fabfile.comm_result(command)
    print(comm_result)
    return render_template('index.html', user=is_login, comm_result=comm_result)


if __name__ == '__main__':
    socketio.run(app, debug=True)
