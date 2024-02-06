import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

from utils import logger, result_path, email_conf


class PostInfo:
    end_mark = '-end-'

    def __init__(self, paper, date):
        self.title = list()
        self.url = list()
        self.section = list()
        self.date = datetime.strptime(date, '%Y%m%d') if len(date) > 0 else datetime.now()
        self.path = ''
        self.paper = paper

    def is_recorded(self):
        year = self.date.year
        month = self.date.month
        day = self.date.day

        self.path = result_path + '/{}-{:0>2d}-{:0>2d}'.format(year, month, day) + '_' + self.paper + '.txt'
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                texts = f.read()
                if self.end_mark in texts:
                    return True
        except FileNotFoundError:
            # windows下无法使用该方法
            if os.name == 'posix':
                os.mknod(self.path)
            logger.info('first time to check, create file!')

        return False

    def write_head(self, file_handle):
        head_info = '{}-{:0>2d}-{:0>2d}'.format(self.date.year, self.date.month, self.date.day)
        file_handle.write('=' * 10 + head_info + '=' * 10 + '\n')

    def write_single(self, file_handle, i):
        # 此处不太可能超过100条，02d够用
        file_handle.write('**************{:0>2d}**************\n'.format(i + 1))
        # section
        file_handle.write('版面：{}\n'.format(self.section[i]))
        # title
        file_handle.write('标题：{}\n'.format(self.title[i]))
        # url
        file_handle.write('地址：{}\n'.format(self.url[i]))

    def write_tail(self, file_handle):
        file_handle.write('=' * 12 + self.end_mark + '=' * 13)

    def save(self):
        if self.is_recorded():
            return

        if len(self.title) != len(self.url):
            logger.error('title len not equal to url!, date{}'.format(datetime.strftime(self.date, '%Y%m%d')))
            return

        file_handle = open(self.path, 'w', encoding='utf-8')

        self.write_head(file_handle)

        for i in range(len(self.title)):
            self.write_single(file_handle, i)

        self.write_tail(file_handle)
        file_handle.close()

        self.send_email()

    def send_email(self):
        if email_conf['enable'] == 0:
            return

        # 没有结果不发送
        if not self.title:
            return

        # 设置发件人、收件人、主题和正文
        smtp_server = email_conf['smtp_server']
        port = email_conf['port']  # SMTP服务器端口，根据实际情况修改
        sender_email = email_conf['username']
        password = email_conf['password']  # SMTP服务器密码，根据实际情况修改
        receiver_email = email_conf['receiver']

        # 创建MIMEText对象，设置邮件格式
        with open(self.path, 'r', encoding='utf-8') as f:
            msg = MIMEText(''.join(f.readlines()))

        date_str = datetime.strftime(self.date, '%Y-%m-%d')
        paper_name = '人民日报'
        if self.paper == 'ad':
            paper_name = '安徽日报'
        elif self.paper == 'gm':
            paper_name = '光明日报'

        msg['Subject'] = "{}_{}".format(date_str, paper_name)
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            # 连接到SMTP服务器并发送邮件
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()  # 启用TLS加密传输
                server.login(sender_email, password)  # 登录SMTP服务器
                server.sendmail(sender_email, receiver_email, msg.as_string())
            print('Email sent successfully!')
        except Exception as e:
            print('Error occurred:', e)
