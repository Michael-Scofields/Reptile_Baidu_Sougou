# -*- coding: utf-8 -*-
import os
import time
import requests
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


def Sougou():
    try:
        global num_sougou
        url_sougou = "https://www.sogou.com/web?query=" + i + "&page=" + str(page)
        # print(url_sougou)
        html_sougou = requests.get(url_sougou, headers=head_sougou, timeout=10)
        html_sougou.encoding = "utf-8"
        content_sougou = html_sougou.text
        with open("Result_sougou.txt", "a" ,encoding='utf-8') as file, open("Re_Sougou.txt", "a" ,encoding='utf-8') as file_sougou_re:
            for j in src_item:
                if j in content_sougou:
                    for line in content_sougou.split("\n"):
                        if j in line and all(key not in line for key in exc_item):
                            num_sougou += 1
                            Results = u"[+] [S-{}] Warning [ {} ] [ {} ] {} -> {}\n".format(page, i, j, runtime, url_sougou)
                            print (Results)
                            file.write(Results)
                            file.write(line)
                            file.write(cutoff)
                            file_sougou_re.write(Results)
                            file_sougou_re.write(line)
                            file_sougou_re.write(cutoff)
                        else:
                            pass
                else:
                        pass
    except Exception as e:
        print("[{}] [Sougou] Connect Failed!".format(runtime))
        print(e)


def Baidu():
    try:
        global num_baidu
        url_baidu = "https://www.baidu.com/s?wd="+ i + "&pn=" + str(page - 1) + "0"
        # print(url_baidu)
        html_baidu = requests.get(url_baidu, headers=head_baidu, timeout=10)
        html_baidu.encoding = "utf-8"
        content_baidu = html_baidu.text
        with open("Result_baidu.txt", "a", encoding='utf-8') as file, open("Re_Baidu.txt", "a" ,encoding='utf-8') as file_baidu_re:
            for j in src_item:
                if j in content_baidu:
                    for line in content_baidu.split("\n"):
                        if j in line and all(key not in line for key in exc_item):
                            num_baidu += 1
                            Results = u"[+] [B-{}] Warning [ {} ] [ {} ] {} -> {}\n".format(page, i, j, runtime, url_baidu)
                            print (Results)
                            file.write(Results)
                            file.write(line)
                            file.write(cutoff)
                            file_baidu_re.write(Results)
                            file_baidu_re.write(line)
                            file_baidu_re.write(cutoff)
                        else:
                            pass
                else:
                    pass
    except Exception as e:
        print("[{}] [Sougou] Connect Failed!".format(runtime))
        print(e)


def Mail():
    sender = 'xxx@xxx.xxx'
    passWord = 'xxx'
    receivers = ['xxx@xxx.xxx', 'xxx@xxx.xxx' ]
    # receivers = ['xxx@xxx.xxx', ]

    msg = MIMEMultipart()
    msg['Subject'] = u'【敏感词搜索监测】' + runtime
    msg['From'] = sender
    msg_content = u'监测时间：{}\n监测页面：{}页\n监测结果：百度搜索{}条，搜狗搜索{}条。\n\n'.format(runtime, page, num_baidu, num_sougou)
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

    att1 = MIMEText(open('Re_baidu.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="Re_baidu.txt"'
    msg.attach(att1)

    att1 = MIMEText(open('Re_Sougou.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="Re_Sougou.txt"'
    msg.attach(att1)

    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        # s.set_debuglevel(1)
        s.login(sender, passWord)
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender, to, msg.as_string())
            print('Send to [{}] Success!'.format(to))
        s.quit()
        sendtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print ("[{}] All emails have been sent over!".format(sendtime))
    except Exception:
        print ("[{}] [Mail] --- Connect Failed! --- [Mail]".format(runtime))


if __name__ == '__main__':
    # starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cutoff = "\n----------------------------------------------\n\n"
    pages = 3
    # search_item = ["赌博", "博彩", "时时彩", "六合彩", "太阳神", "黑彩", "快彩", "七星彩", "七乐彩"]
    search_item = ["赌博", "博彩", "时时彩", "六合彩", "香港赛马会", "北京赛车", "草榴" ]
    src_item = ["xxx", "xxx", "xxx", "xxx", "xxx"]
    exc_item = ["xxx", "xxxx", "xxxxx"]
    head_sougou = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',\
        }
    head_baidu = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',\
        }
    # content_sougou = "Null"
    # content_baidu = "Null"
    while True:
        if os.path.exists("Re_Baidu.txt"):
            f1 = open('Re_Baidu.txt', "r+")
            f1.truncate()
        if os.path.exists("Re_Sougou.txt"):
            f2 = open('Re_Sougou.txt', "r+")
            f2.truncate()
        num_baidu = num_sougou = 0
        for i in search_item:
            for page in range(1, pages + 1):
                runtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                Sougou()
                Baidu()
        Mail()
        print ("Waiting 6h ...\n")
        time.sleep(300)
