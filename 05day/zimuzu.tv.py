# -*- coding:utf-8 -*-

import requests
import json
import re
from lxml import etree

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

    def login(self):
        self.account = raw_input('请输入用户名：')
        self.password = raw_input('请输入密码：')
        self.form_data = {
            "account": self.account,
            "password": self.password,
            "remember": 1,
            "url_back": self.BASE_URL
        }
        self.session = requests.session()
        self.session.post(self.LOGIN_URL, headers=self.headers, data=self.form_data)

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
        params = {'keyword': search_info}
        search_response = self.session.get(self.SEARCH_URL, params=params, headers=self.headers)
        html = etree.HTML(search_response.content)
        # 此处xpath匹配出的结果为/resource/31951，详情页为/resource/list/31951，进行re.sub替换
        link = html.xpath('//div[@class="clearfix search-item"]/div[@class="fl-img"]/a/@href')[0]
        link_total = self.BASE_URL + re.sub(r'\b/\b', '/list/', link)
        return self.session.get(link_total, headers=self.headers).content

    def write(self, content):
        with open(self.search+'.txt', 'w') as f:
            data = etree.HTML(content)
            dl = data.xpath('//div[@class="fr"]/a[@type="ed2k"]/@href')
            print dl
            for i in dl:
                f.write(i.encode('utf-8')+'\n')

if '__main__' == __name__:
    z = Zimuzu()
    z.login()
    if z.login_check():
        z.write(z.search())

