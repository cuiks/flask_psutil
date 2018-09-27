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
