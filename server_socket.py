#!/usr/bin/env python
#-*- encoding:utf-8 -*-

'''
a example server writen in python
author: yxd123
create: 2014/9/11
blog: http://www.cnblogs.com/coder2012/
'''
import socket

class Server:
    def __init__(self, ip, port, pro, num, BUFSIZE=1024):
        self.ip = ip
        self.port = port
        self.pro = pro
        self.num = num
        self.BUFSIZE = BUFSIZE
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.num)

    def loop(self):
        while True:
            print 'waiting for connectin...'
            clnsock, addr = self.sock.accept()
            print 'connection addr:%',addr
            while True:
                data = clnsock.recv(self.BUFSIZE)
                print data
                if not data:
                    clnsock.close()
                    break
        self.sock.close()

if __name__ == '__main__':
    myServer = Server('localhost', 1235, 'tcp', 5)
    myServer.loop()