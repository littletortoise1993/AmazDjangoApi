from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
from AppBase import models


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def SendEmail(mailTo,title,mailContent):
    try:
        # 获取发件人信息
        fromUserInfos = models.EmailSendFromDefaultSettings.objects.all()
        if len(fromUserInfos) <= 0:
            return "系统未设置发件人信息"
        defaultFromUserInfo = fromUserInfos[0]
        password = defaultFromUserInfo.userPassword
        from_addr = defaultFromUserInfo.formUser

        # 获取邮件信息

        smtp_server = defaultFromUserInfo.smtpServer
        to_addr = mailTo
        msg = MIMEMultipart()
        msgText = MIMEText(mailContent, 'html', 'utf-8')
        msg.attach(msgText)
        msg['From'] = _format_addr('%s <%s>' % (defaultFromUserInfo.userShowName, defaultFromUserInfo.formUser))
        msg['To'] = mailTo
        msg['Subject'] = Header(title, 'utf-8').encode()
        # # 添加附件
        # filepath = emailRecordInfo.mailAttchment.path
        # filename = emailRecordInfo.mailAttchment.name
        #
        # attach = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
        # attach["Content-Type"] = 'application/octet-stream'
        # attach["Content-Disposition"] = 'attachment; filename=' + filename
        # msg.attach(attach)

        # 开始发送邮件
        server = smtplib.SMTP_SSL(smtp_server, 465) #25改为465 解决centos下发送不了邮件问题
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        return "success"
    except Exception as e:
        return str(e)


