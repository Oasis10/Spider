# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
import time

# 创建PhantomJS浏览器驱动对象
driver = webdriver.PhantomJS()

# 发送页面请求
driver.get("http://www.zimuzu.tv/User/Login/")
time.sleep(4)
print '读取字幕组登录页面完毕'

# 输入账户名
driver.find_element_by_name('email').send_keys(u'624702322@qq.com')
# 输入密码
driver.find_element_by_name('password').send_keys(u'61287427')
# 保存截图
driver.save_screenshot('zimuzu.png')
# 模拟点击登录
driver.find_element_by_id('login').click()
time.sleep(4)
print '保存页面完毕'
driver.save_screenshot('zimuzu_login.png')

with open('zimuzu2.html', 'w') as f:
    f.write(driver.page_source)

driver.quit()

