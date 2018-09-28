#!/usr/bin/env python3
# -*- conding:utf-8 -*-

'''
项目:电子词典

功能:电子词典服务端

相关技术:多进程 mysql等

作者：SanMuShen

邮箱:1943318083@11.com

'''

from socket import *
import sys
import time


# 登录界面
def one_fa(s):
    s = s
    s.send(('D').encode())
    n1 = input('请输入用户名:')
    n2 = input('请输入密码:')
    s.send(('%s %s'%(n1,n2)).encode())
    data = s.recv(1024)
    if data.decode() == 'OK':
        print('登录成功')
        three_fa(s)

    else:
        print(data.decode())

# 注册界面
def two_fa(s):
    print('----------注册---------')
    s.send(('Z').encode())
    n1 = input('请输入新用户名:')
    n2 = input('请输入密码:')
    s.send(('%s %s'%(n1,n2)).encode())
    data = s.recv(1024)
    if data.decode == 'OK':
        print('注册成功')
    else:
        print(data.decode())

# 进入二级界面
def three_fa(s):
    s = s
    while True:
        print('-----------1.查单词-------------')
        print('-----------2.历史记录-----------')
        print('-----------3.退出--------------')
        n = input('请输入你的选择:')
        if n == '1':
            cha_dict(s)
        elif n == '2':
            cha_lishi(s)
        elif n == '3':
            return

# 查询单词功能
def cha_dict(s):
    s.send(b'C')
    while True:
        n = input('请输入要查询的单词')
        s.send(('%s'%n).encode())
        if n != '##':
            data = s.recv(1024)
            if data.decode() == 'OK':
                data1 = s.recv(4096)
                if data1.decode() == '单词不存在':
                    print(data1.decode())
                print(data1.decode())
        else:
            break

# 查看用户查询历史记录功能
def cha_lishi(s):
    s.send(b'L')
    data = s.recv(4096)
    print(data.decode())

# 主界面
def main():
    if len(sys.argv) < 3:
        print('输入格式错误')
    # 创建套接字
    s = socket()
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    try:
        s.connect(ADDR)
    except Exception as e:
        print('连接服务器失败',e)
        return

    # 一级界面功能
    while True:
        print('-----------1.登录-----------')
        print('-----------2.注册-----------')
        print('-----------3.退出-----------')
        n = input('请输入你的选择:')
        if n == '1':
            one_fa(s)

        elif n == '2':
            two_fa(s)

        elif n == '3':
            break

if __name__ == '__main__':
    main()