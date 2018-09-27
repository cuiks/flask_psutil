# -*- coding: utf-8 -*-

import json
import urllib.request

zbx_url = "http://192.168.1.148/zabbix/api_jsonrpc.php"
zabbix_user = "Admin"
zabbix_pwd = "zabbix"


def get_token():
    dicts = '{"user": "Admin","password": "zabbix"}'
    url = zbx_url
    header = {"Content-Type": "application/json"}
    data = '''{
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": %s,
            "id": 0
	    }''' % dicts
    request = urllib.request.Request(url, data.encode())
    for key in header:
        request.add_header(key, header[key])
    try:
        result = urllib.request.urlopen(request)
    except urllib.request.URLError as e:
        print(e)
    else:
        response = json.loads(result.read())
        result.close()
        return response["result"]


def get_params(i):
    all_params = {
        '1': '{"output": ["hostid", "host"], "selectInterfaces": ["interfaceid", "ip"]}',
        '2': '{"output": "extend","graphids": "387"}',
        '3': '{ "output":"extend"}'
    }
    return all_params[i]


def get_action(i):
    all_action = {
        '1': 'host.get',
        '2': 'graphitem.get',
        '3': 'user.get'
    }
    return all_action[i]


def zbx_req(i):
    zbx_action = get_action(i)
    zbx_params = get_params(i)
    zbx_token = get_token()
    url = zbx_url
    header = {"Content-Type": "application/json"}
    data = '''{
            "jsonrpc": "2.0",
            "method": "%s",
            "params": %s,
            "auth" : "%s",
            "id": 1
    	    }''' % (zbx_action, zbx_params, zbx_token)

    request = urllib.request.Request(url, data.encode())
    for key in header:
        request.add_header(key, header[key])
        try:
            result = urllib.request.urlopen(request)
        except urllib.request.URLError as e:
            print(e)
        else:
            response = json.loads(result.read())
            if 'error' in response:
                print(response)
                return False
            else:
                return response['result']
