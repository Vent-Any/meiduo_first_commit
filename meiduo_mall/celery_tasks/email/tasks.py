from django.core.mail import send_mail
from celery_tasks.main import app


# subject, message, from_email, recipient_list,
# subject, 主题
@app.task
def celery_send_email(email, verify_url):
    subject = '主题'
    # message, 邮件内容
    message = ''
    # from_email, 谁发的邮件
    from_email = '美多商城<qi_rui_hua@163.com>'  # recipient_list, 收件人列表 ['邮箱','邮箱',,]
    # 设置邮件内容  以网址形式显示内容  (激活邮件)
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
    # recipient_list = [email]
    # 设置可接受人的列表
    recipient_list = [email]
    # 发送邮件
    send_mail(subject,
              message,
              from_email,
              recipient_list,
              html_message=html_message)
