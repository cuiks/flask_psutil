# psutil_webshow
## 整体的框架是使用的Flask
为了方便大家直接使用，本系统需要配置：

1。链接本地数据库。
`app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://数据库用户:数据库密码@127.0.0.1/数据库名`<br>
用到的表：<br>
在创建models时，Role使用到表:'user',user表结构为:id,email,password。<br>
数据示例:`1  1@1.com  123`<br>
在save_status文件中保存cpu数据使用到表cpu_used;结构为:id,cpu_used,add_time。<br>
数据示例：`1 10.1 1537517750804`<br>
2。因为使用socketio运行的方式，所以使用pycharm启动时，控制台不会显示启动的host。<br>
3。使用socketio的方式，让后端程序在产生数据后主动向前端js推送。<br>
4。tongyong.py文件为使用zabbix的API，所以需要有一台安装了zabbix的linux机器，然后修改：<br>
`zbx_url = "http://192.168.1.148/zabbix/api_jsonrpc.php"
zabbix_user = "Admin"
zabbix_pwd = "zabbix"`
5。Fabrics下的frbfile为使用fabric，所以需要一台装有fabric的linux机器。然后修改:<br>
`env.hosts = ['root@liunx_host:22']
env.passwords= {'root@linux_host:22':'password'}`
6。post_email文件中，sender需要替换成自己的邮箱，receiver替换成自己的接收邮箱。s.login(sender,password)后面的密码也要改为自己的