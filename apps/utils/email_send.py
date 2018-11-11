from django.core.mail import send_mail

from apps.users.models import EmailVerifyRecord
from mxonline.settings import EMAIL_FROM

import string
import random

# 生成随机字符串
def random_str(num=12):
    source = list(string.ascii_letters)
    for i in range(10):
        source.append(str(i))
    code_str = "".join(random.sample(source,num))
    # print(code_str)

    return code_str


def send_regist_email(email,send_type='register'):
    # 发送之前先保存到数据库,到时候查询连接是否存在
    # 实例化一个EmailVerifyRecord()
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 邮件内容
    email_title = ''
    email_body = ''

    if send_type == "register":
        email_title = "优课课堂邮箱验证"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/user/active/{0}/".format(code)

        #　使用Django内置函数完成邮件发送
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print("邮件发送成功")
        else:
            print("发送失败")

    if send_type == "forget":
        email_title = "优课课堂邮箱验证"
        email_body = "请点击下面的链接重置你的账号: http://127.0.0.1:8000/user/reset/{0}/".format(code)

        #　使用Django内置函数完成邮件发送
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
        else:
            print("发送失败")