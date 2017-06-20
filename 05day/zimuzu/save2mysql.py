# -*- coding:utf-8 -*-

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Zimuzu2Mysql(object):


    def __init__(self, host="localhost", port=3306, user="root", password="mysql", db="zimuzu", charset="utf8"):
        """初始化"""
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.__charset = charset
        try:
            self.__open()
        except Exception, e:
            print e

    def __open(self):
        """建立python和MySQL的连接"""
        self.__conn = MySQLdb.connect(
            host = self.__host,
            port = self.__port,
            user = self.__user,
            passwd = self.__password,
            db = self.__db,
            charset = self.__charset
        )
        self.__cursor = self.__conn.cursor()

    def close(self):
        """关闭连接"""
        self.__cursor.close()
        self.__conn.close()

    def create_table(self, name):
        """创建数据库表"""
        print name
        try:
            sql = "create table " + name + " (id int unsigned auto_increment primary key not null,link text); "
            print sql
            self.__cursor.execute(sql)
            self.__conn.commit()
        except Exception, e:
            print "添加失败，错误代码为：", e
            return False

    def insert(self, name, link):
        """增加数据"""
        # 构造sql语句
        print name
        try:
            # sql = "INSERT INTO " + name + " VALUES (0,%s); "
            sql = "INSERT INTO " + name + " VALUES (0," + "'" + link + "'" + "); "
            print sql
            # 执行sql语句
            # result = self.__cursor.execute(sql, [link])
            result = self.__cursor.execute(sql)
            # 判断是否执行成功
            if result == 1:
                self.__conn.commit()
                return True
            else:
                return False

        except Exception, e:
            print "添加失败，错误代码为：", e
            return False
