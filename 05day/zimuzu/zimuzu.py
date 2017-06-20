# -*- coding:utf-8 -*-

import requests
import json
import re
from lxml import etree
from save2mysql import Zimuzu2Mysql


class Zimuzu(object):

    def __init__(self):
        self.BASE_URL = 'http://www.zimuzu.tv'
        self.LOGIN_URL = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
        self.SEARCH_URL = 'http://www.zimuzu.tv/search/index?'
        self.CHECK_LOGIN_URL = 'http://www.zimuzu.tv/user/login/getCurUserTopInfo'
        self.headers = {
            "Host":"www.zimuzu.tv",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        }

    def login(self,op_num):
        if op_num == '1':
            account = '624702322@qq.com'
            password = '61287427'
        elif op_num == '2':
            account = raw_input('请输入用户名：')
            password = raw_input('请输入密码：')
        else:
            return False
        form_data = {
            "account": account,
            "password": password,
            "remember": 1,
            "url_back": self.BASE_URL
        }
        self.session = requests.session()
        self.session.post(self.LOGIN_URL, headers=self.headers, data=form_data)
        return True

    def login_check(self):
        json_data = self.session.get(self.CHECK_LOGIN_URL, headers=self.headers).content
        data = json.loads(json_data)
        if data['status'] == 1:
            print '登录成功！'
            return True
        else:
            print '登录失败，请重试！'
            return False

    def search(self):
        # 查询
        search_info = raw_input('请输入要查询的电视剧或电影：')
        self.search = search_info
        print '您所查询的是：' + search_info
        params = {'keyword': search_info}
        search_response = self.session.get(self.SEARCH_URL, params=params, headers=self.headers)
        html = etree.HTML(search_response.content)
        # 此处xpath匹配出的结果为/resource/31951，详情页为/resource/list/31951，进行re.sub替换
        link = html.xpath('//div[@class="clearfix search-item"]/div[@class="fl-img"]/a/@href')[0]
        link_total = self.BASE_URL + re.sub(r'\b/\b', '/list/', link)
        print '下载页面详细链接为：' + link_total
        return self.session.get(link_total, headers=self.headers).content

    def save_file(self, content):
        with open(self.search+'.txt', 'w') as f:
            data = etree.HTML(content)
            dl = data.xpath('//div[@class="fr"]/a[@type="ed2k"]/@href')
            for i in dl:
                print i
                f.write(i.encode('utf-8')+'\n')
        print '保存成功！保存的文件为：' + self.search + '.txt'

    def save_mysql(self, content):
        op_num = raw_input('请选择mysql存储方式：1、系统默认-登录 2、用户名密码-登录   ')
        if op_num == '1':
            m = Zimuzu2Mysql()
        elif op_num == '2':
            user = raw_input('请输入用户名：')
            password = raw_input('请输入密码： ')
            m = Zimuzu2Mysql(user=user, password=password)
        else:
            print '输入有误，请重新输入！'
        data = etree.HTML(content)
        dl = data.xpath('//div[@class="fr"]/a[@type="ed2k"]/@href')
        # 创建数据库表
        m.create_table(self.search)
        # 向数据库中添加数据
        for link in dl:
            m.insert(self.search, link.encode('utf-8'))
        # 执行完毕，关闭数据库
        m.close()
        print self.search + '-下载链接已成功存入数据库！'








