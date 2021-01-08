from django.core.mail import send_mail
from celery_tasks.main import app


# subject, message, from_email, recipient_list,
# subject, 主题
@app.task
def celery_send_email(email):
    subject = '主题'
    # message, 邮件内容
    message = '邮件内容'
    # from_email, 谁发的邮件
    from_email = '美多商城<qi_rui_hua@163.com>'  # recipient_list, 收件人列表 ['邮箱','邮箱',,]
    # recipient_list = [email]
    recipient_list = [email]
    send_mail(subject,
              message,
              from_email,
              recipient_list)
