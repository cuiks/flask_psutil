# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

host = 'smtp.aliyun.com'
port = 25
sender = 'hero777@aliyun.com'
receiver = 'register012@163.com'


def add_info(info):
    f = open('report_base.html', 'rb')
    html = f.read()
    f.close()
    mail_body = html.replace(b'{{ data }}', str(info).encode()).decode('utf-8')
    f = open('report_html.html','w')
    f.write(mail_body)
    f.close()
    # print(mail_body)

    msg = MIMEText(mail_body, 'html', 'utf-8')

    msg['Subject'] = 'Cpu status'
    msg['From'] = sender
    msg['To'] = receiver

    try:
        s = smtplib.SMTP(host, port)
        s.login(sender, 'cui5211314')
        s.sendmail(sender, receiver, msg.as_string())
        print('************cpu占用超过 40%，提醒邮件发送成功************')
    except smtplib.SMTPException as e:
        print(e)
