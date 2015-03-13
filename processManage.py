#!/usr/bin/env python
# encoding:utf8

import os 
import time

def getProcessPid(processName):
    '''user pid time cmd parameter'''
    #cmd = 'ps aux|grep ' + processName  + '|grep -v grep |awk \'{print $1,$2,$10,$11,$12}\''
    cmd = 'ps aux|grep ' + processName  + '|grep -v grep|grep -v processManage|awk \'{print $2}\''
    #print cmd
    res = os.popen(cmd).read() 
    lines = res.split('\n')
    #print res
    res = []
    for line in lines:
        if line != '':
            res.append(int(line))
    return res

def killProcessByName(processName):
    #cmd = 'kill 9 `ps aux|grep ' + processName  + '|grep -v grep|grep -v processManage|awk \'{print $2}\'`'
    pids = getProcessPid(processName)
    print pids
    for pid in pids:
        cmd = 'kill 9 ' + str(pid)
        os.system(cmd)

def killProcessByPid(pid):
    cmd = 'kill 9 ' + pid
    os.system(cmd)

def showProcessStatus(processName):
    cmd = 'ps aux|grep ' + processName  + '|grep -v grep|grep -v processManage|awk \'{print $1,$2,$10,$11,$12}\''
    res = os.popen(cmd).read()
    return res

def getProcessIsRuning(processName, timeout):
	cmd = 'ps aux|grep ' + processName + '|grep -v grep|grep -v processManage|awk \'{print $2,$11}\''
	t = 0
	res = ''
	while res == '':
		if(t >= timeout):
			return -1
		t += 1
		res = os.popen(cmd).read()
		time.sleep(t)
	return 1

if __name__ == '__main__':
    #print getProcessPid('nginx'),
    #print '--------------------------------------'
    #print getProcessPid('test'),
    #print '--------------------------------------'
    #print getProcessPid('rtest'),
    #print '--------------------------------------'
    #print getProcessPid('memcache')

    #killProcessByName('test.py')
    #killProcessByPid(raw_input())
    #tmp = showProcessStatus('ptest')
    #tmp = getProcessPid('test.py')
    #print tmp

    #killProcessByName('test.py')
	print getProcessIsRuning('nginx', 10)
