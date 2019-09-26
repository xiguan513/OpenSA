#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Author: 习惯
Email: songbing513@mail.com
"""

import MySQLdb
import os
try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'conf/autoconfig.ini'))



class DbOpt:
    def __init__(self):
        self.Host = config.get('db','host')
        self.user = config.get('db','user')
        self.pwd = config.get('db','password')
        self.db = config.get('db','database')
        self.port = int(config.get('db','port'))

    def con(self):
        return  MySQLdb.connect(self.Host,self.user,self.pwd,self.db,self.port)



if __name__ == '__main__':
    dbcon = DbOpt().con()
    cur = dbcon.cursor()
    cur.execute('select git_name from gitinfo where git_ssh="ssh://git@192.168.1.228:7999/yun/test.git"')
    for data in cur.fetchall():
        print(data[0])

