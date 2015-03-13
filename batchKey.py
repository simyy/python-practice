#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sys
import paramiko
import MySQLdb
from init import *

#注意，此处不能用～来代替家目录
home_dir = '/home/yu'
id_rsa_pub = '%s/.ssh/id_rsa.pub' %home_dir

if not  id_rsa_pub:
    print 'id_rsa.pub Does not exist!'
    sys.exit(0)

file_object = open('%s/.ssh/config' %home_dir ,'w')
file_object.write('StrictHostKeyChecking no\n')
file_object.write('UserKnownHostsFile /dev/null')
file_object.close()


def up_key(host,port,user,passwd):
    ''' send id_rsa.pub to others servers '''
    try:
        s = paramiko.SSHClient()
	s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	s.connect(host, port, user, passwd)

        t = paramiko.Transport((host, port))
        t.connect(username=user, password=passwd, timeout=3)
        sftp =paramiko.SFTPClient.from_transport(t)

        print 'create Host:%s .ssh dir......' %host
        stdin,stdout,stderr=s.exec_command('mkdir ~/.ssh/')
        print 'upload id_rsa.pub to Host:%s......' %host
        sftp.put(id_rsa_pub, "/tmp/temp_key")
        stdin,stdout,stderr=s.exec_command('cat /tmp/temp_key >> ~/.ssh/authorized_keys && rm -rf /tmp/temp_key')
        print 'host:%s@%s auth success!\n' %(user, host)
        s.close()
        t.close()
    except Exception, e:
        #import traceback
        #traceback.print_exc()
        print 'connect error...'
        print 'delete ' + host  + ' from database...'
        delip(host)
        #delete from mysql****
        try:
            s.close()
            t.close()
        except:
            pass

def testconn(host, port, user, passwd):
    ''' judge connect or not '''
    try:
        print 'test conn: ',host
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, port, user, passwd, timeout = 3)
    except Exception as e:
        print 'connect error...'
        print 'delete ' + host + ' from database...'
        delip(host)
        s.close()

def run():
    ''' 
    must add a parameter:
    1. testconn : test connect
    2. batchkey : add id_rsa.pud to others
    '''
    ips = loadip()
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = ''
    print 'parameter: ',arg
    if len(ips) == 0:
        print 'no ip...'
        return
    if (arg != 'testconn') and (arg != 'batchkey'):
        print 'add a para: testconn or batchkey'
        return
    for line in ips:
        host = line[1]
        port = parseconf('conf.ini', 'port')
        user = parseconf('conf.ini', 'user')
        passwd = parseconf('conf.ini', 'password')
        if arg == 'testconn':
            testconn(host, int(port), user, passwd)
        elif arg=='batchkey':
            up_key(host, int(port), user, passwd)

    print 'testconn finish...'
           
if __name__ == '__main__':
    run()
