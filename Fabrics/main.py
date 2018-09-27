# -*- coding: utf-8 -*-

import os

def comm_result(command):
    comm = '''fab -H localhost run_command:command='%s' -f Fabrics/fabfile.py''' % command
    print(comm)
    result = os.popen(comm)
    result = result.read()
    return result