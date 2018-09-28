#!/usr/bin/env python3
#-*- conding:utf-8 -*-

'''
项目:电子词典

功能:电子词典服务端

相关技术:多进程 mysql等

作者：SanMuShen

邮箱:1943318083@11.com

'''

from socket import *
import os
import pymysql
import signal
import sys
import time

# 用户登录功能
def one_shou(c,db):
    data = c.recv(1024).decode()
    data = data.split(' ')
    cursor = db.cursor()
    sql1 = 'select name,passwd from user where name = "%s"'%data[0]
    try:
        # python操作mysql数据库
        cursor.execute(sql1)
        # 获取从数据库返回的元组
        data1 = cursor.fetchall()
        db.commit()
    except:
        s = '数据库查不到'
        c.send(s.encode())

    if not data1:
        s = '用户名不存在'
        c.send(s.encode())
        
    else:
        # 判断条件输入的用户名和密码必须和数据库里的相同
        if data1[0][0] == data[0] and data1[0][1] == data[1]:
            c.send(b'OK')
            print('登录成功')
            while True:
                data = c.recv(1024)
                if data.decode() == 'C':
                    print('查单词')
                    cha_dict(c,db,data1[0][0])
                elif data.decode() == 'L':
                    cha_lishi(c,db,data1[0][0])
        else:
            s = '账号或密码错误'
            c.send(s.encode())

# 用户注册功能
def two_shou(c,db):
    data = c.recv(1024).decode()
    data = data.split(' ')
    cursor = db.cursor()
    sql = 'insert into user(name,passwd) values("%s","%s")'%(data[0],data[1])
    try:
        cursor.execute(sql)
        c.send(b'OK')
        db.commit()
    except:
        db.rollback()
        c.send(('注册失败').encode())

# 查询单词注释功能
def cha_dict(c,db,name):
    while True:
        data = c.recv(1024).decode()
        if not data:
            print('不查了')
            sys.exit()
        if data == '##':
            print('不查了')
            break
        cursor = db.cursor()
        sql = 'select interpret from words where word = "%s"'%data

        # 将查询的单词添加到数据库hist表中
        sql1 = 'insert into hist(name,word) values("%s","%s")'%(name,data)
        try:
            cursor.execute(sql)
            data1 = cursor.fetchall()
            cursor.execute(sql1)
            c.send(b'OK')
            db.commit()
            # 防止粘包睡眠1秒
            time.sleep(1)

        except:
            # 出现异常则事务回滚
            db.rollback()
        if not data1:
            s = '单词不存在'
            c.send(s.encode())
        else:
            c.send(data1[0][0].encode())

# 获取用户查询的单词历史
def cha_lishi(c,db,name):
        print('开始查询历史记录')
        cursor = db.cursor()
        sql = 'select name,word,time from hist where name ="%s";'%name
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except:
            sys.exit()
        if not data:
            s = '没有历史记录'
            c.send(s.encode())
        else:
            for l in data:
                c.send(str(l).encode())

# 服务端框架
def main():
    # 创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict')
    
    # 创建TCP套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',8888))
    s.listen(5)

    # 忽略子进程退出信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        name = ''
        try:
            # 等待客户端连接
            c,addr = s.accept()
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        print('已连接',addr)

        # 创建父子进程
        pid = os.fork()

        # 子进程功能
        if pid == 0:
            s.close()
            print('子进程准备处理请求')
            while True:
                try:
                    data = c.recv(1024)
                except:
                    break
                if data.decode() == 'D':
                    one_shou(c,db)
                elif data.decode() == 'Z':
                    print('正在注册')
                    two_shou(c,db)

            # 关闭数据库
            db.close()
            sys.exit()

        else:
            # 关闭客户端套接字
            c.close()
            continue

if __name__ == '__main__':
    main()