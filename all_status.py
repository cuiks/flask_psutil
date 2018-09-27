# -*- coding: utf-8 -*-
import time

import psutil

'''
# functions
    "pid_exists", "pids", "process_iter", "wait_procs",             # proc
    "virtual_memory", "swap_memory",                                # memory
    "cpu_times", "cpu_percent", "cpu_times_percent", "cpu_count",   # cpu
    "cpu_stats",  # "cpu_freq",
    "net_io_counters", "net_connections", "net_if_addrs",           # network
    "net_if_stats",
    "disk_io_counters", "disk_partitions", "disk_usage",            # disk
    # "sensors_temperatures", "sensors_battery", "sensors_fans"     # sensors
    "users", "boot_time",                                           # others
'''


class Cpu_status():
    # cpu
    # cpu_num = psutil.cpu_count(logical=False)
    # print('物理cpu数量:', cpu_num)
    # cpu_use = psutil.cpu_percent(0.1)
    # print('cpu当前利用率为', cpu_use)
    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=False)
        self.cpu_use = psutil.cpu_percent()

    def cpu_used(self):
        return psutil.cpu_percent()


class Memory_status():
    # memory
    # free = str(round(psutil.virtual_memory().free / (1024 * 1024 * 1024), 2))
    # print('空闲内存为:%sG' % free)
    # used = str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2))
    # print('使用内存为:%sG' % used)
    # total = str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2))
    # print('总内存为:%sG' % total)
    def __init__(self):
        self.used = str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2))
        self.free = str(round(psutil.virtual_memory().free / (1024 * 1024 * 1024), 2))
        self.total = str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2))


class Disk_status():
    def __init__(self):
        self.total = ''
        self.used = ''
        self.free = ''
        # self.diskinfo = psutil.disk_partitions()

    # yingpan
    def disk_info(self):
        disk_list = []
        diskinfo = psutil.disk_partitions()
        # self.diskinfo = psutil.disk_partitions()
        for i, disk in enumerate(diskinfo):
            # print('磁盘%s:' % i)
            info = psutil.disk_usage(disk.device)
            disk_list.append(info)
        return disk_list
        #     self.total = str(int(info.total / (1024 * 1024 * 1024)))
        #     self.used = str(int(info.used / (1024 * 1024 * 1024)))
        #     self.free = str(int(info.free / (1024 * 1024 * 1024)))
        # print('总容量:%sG' % str(int(info.total / (1024 * 1024 * 1024))))
        # print('已用:%sG' % str(int(info.used / (1024 * 1024 * 1024))))
        # print('空闲:%sG' % str(int(info.free / (1024 * 1024 * 1024))))


class Net_status():
    # #wangka
    # net = psutil.net_io_counters()
    # recv = round(net.bytes_recv / (1024 * 1024), 2)
    # errin = round(net.errin / (1024 * 1024), 2)
    # sent = round(net.bytes_sent / (1024 * 1024), 2)
    # errout = round(net.errout / (1024 * 1024), 2)
    # print('网卡接收:%sM' % recv)
    # print('网卡接收失败:%sM' % errin)
    # print('网卡发送:%sM' % sent)
    # print('网卡发送失败:%sM' % errout)
    def __init__(self):
        self.net = psutil.net_io_counters()
        self.recv = round(self.net.bytes_recv / (1024 * 1024), 2)
        self.errin = round(self.net.errin / (1024 * 1024), 2)
        self.sent = round(self.net.bytes_sent / (1024 * 1024), 2)
        self.errout = round(self.net.errout / (1024 * 1024), 2)


class User_status():
    # # #users
    # user_count = len(psutil.users())
    # user_list = ','.join([u.name for u in psutil.users()])

    # print('当前存在 %s 个用户，分别为: %s' % (user_count, user_list))
    #
    # #jincheng
    # for psid in psutil.pids():
    #     p = psutil.Process(psid)
    #     pro_name = p.name()
    #     pro_status = p.status()
    #     pro_creat_time = p.create_time()
    # print('进程名: %s 状态: %s 创建时间: %s' % (p.name(), p.status(), p.create_time()))
    def __init__(self):
        self.user_count = len(psutil.users())
        self.user_list = [u.name for u in psutil.users()]
        self.pids = psutil.pids()


import pymysql
def add_status():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='cui123', db='bootstrap')
    cursor = conn.cursor()

    cpu = Cpu_status()
    while True:
        time.sleep(1)
        cpu_used = cpu.cpu_used()
        add_time = int(time.time() * 1000)
        # print(cpu_used, add_time)
        sql = '''insert into cpu_used(add_time,cpu_used) values (%s,%s)''' % (cpu_used, add_time)
        cursor.execute(sql)
        conn.commit()
