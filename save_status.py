# -*- coding: utf-8 -*-
import time
import psutil
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='cui123', db='bootstrap')
cursor = conn.cursor()

sql = '''insert into cpu_used(cpu_used,add_time) values (%s,%s)'''


def save_cpu():
    while True:
        # print('执行')
        add_time = int(time.time() * 1000)
        cpu_used = psutil.cpu_percent(interval=None)
        # print(add_time, cpu_used)
        time.sleep(1)
        sql_now = sql % (cpu_used, add_time)
        cursor.execute(sql_now)
        conn.commit()


# th_saveCpu = threading.Thread(target=save_cpu)
# th_saveCpu.start()
