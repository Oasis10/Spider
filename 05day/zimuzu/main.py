# -*- coding:utf-8 -*-


from zimuzu import *

def main():
    print '-*'*20, '\n', '\n', '\n'
    print '欢迎使用zimuzu.tv下载器 V1.1', '\n', '\n', '\n'
    print '-*' * 20
    z = Zimuzu()
    while True:
        login_mode = raw_input('***请选择登录方式：1、系统默认-登录 2、用户名密码-登录   ')
        if z.login(login_mode):
            if z.login_check():
                save_mode = raw_input('***请选择保存方式：1、保存到本地文件 2、保存到MySQL数据库中   ')
                if save_mode == '1':
                    z.save_file(z.search())
                elif save_mode == '2':
                    z.save_mysql(z.search())
                else:
                    print '输入有误，请重新输入！'
            else:
                print '登录失败，请确认用户名和密码后重试！'
        else:
            print '输入有误，请重新输入！'

if '__main__' == __name__:
    main()
