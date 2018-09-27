# -*- coding: utf-8 -*-
import re
import zipfile


base = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 'a', 11: 'b', 12: 'c'}


num_total = 1

while True:
    pwd = ''
    num = num_total
    while num > 0:
        index = num % len(base)
        num = num // len(base)
        pwd = str(base[index]) + pwd
    num_total += 1
    try:
        f = zipfile.ZipFile('D://cut.zip', 'r')
        for file in f.namelist():
            f.extract(file, 'd:', pwd=pwd.encode('ascii'))
        print(pwd,'successed!')
        break
    except Exception as e:
        print(pwd,'failed')
