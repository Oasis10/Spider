# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib

# 创建CookieJar()对象,用来保存cookie
cookie_jar = cookielib.CookieJar()

# 创建cookie处理器对象，让自定义的opener拥有处理cookie的能力
cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)

# 创建自定义opener对象，用来发送请求
opener = urllib2.build_opener(cookie_handler)

form_data = {
    'email':'624702322@qq.com',
    'password':'61287427'
}

# url转码
data = urllib.urlencode(form_data)

url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}

# opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")]


request = urllib2.Request(url, data=data, headers=headers)

opener.open(request)

response = opener.open('http://www.zimuzu.tv')

with open('zimuzu_urllib2.html', 'w') as f:
    f.write(response.read())