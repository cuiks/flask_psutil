# -*- coding: utf-8 -*-

from fabric.api import run, env
from fabric.tasks import execute

env.hosts = ['root@192.168.1.148:22']
env.passwords= {'root@192.168.1.148:22':'cui123'}

def run_command(command=''):
    return run(command)


def comm_result(comm):
    a = execute(run_command,comm)
    result_list = []
    for val in a.values():
        result_list.append(val)
    return result_list
