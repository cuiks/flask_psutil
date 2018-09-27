# -*- coding: utf-8 -*-
# !/usr/bin/env python

from fabric.api import run, env

env.hosts = ['root@192.168.1.148:22', ]
env.password = 'cui123'


def run_command(command=''):
    run(command)
