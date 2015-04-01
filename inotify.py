#!/usr/bin/env python
# -*- utf-8 -*-

'''
Linux Inotify to monitor dir or files
'''


import os
import time
import pyinotify

def getFileList(path = ''):
    r = []
    if not path:
        return r
    try:
        for root,dirs,files in os.walk(path):
            for i in files:
                fullpath = os.path.join(root, i)
		r.append((i, fullpath))
    except Exception, e:
	    print 'Error: %s'%e
    return r

class Event:
    def __init__(self, mlist):
        self.event = {}
        self.mlist = mlist

    def create(self):
		return
	
    def access(self):
		return
	
    def close(self, key):
		if key not in self.event:
			self.event[key]={'CLOSE':0}
		eventDict = self.event[key]
		n = eventDict['CLOSE']
		#if not ((n + 1) % 3):
		#	print '***************close'
		#	eventDict['CLOSE'] = 0
		#else:
		#	eventDict['CLOSE'] = n + 1
		#do someting here
		print '********close'
		#print self.event
		#print eventDict
    
    def modify(self):
		return

class EventHandler(pyinotify.ProcessEvent):
    
    def __init__(self, fevent):
		self.mlist = fevent.mlist 
		self.fevent = fevent

    def process_IN_CREATE(self, event):
		#print 'get a create event'
		return

    def process_IN_CLOSE_WRITE(self, event):
		#print '-------------------------'
		#print 'get a close event'
		#print event.path
		#print event.name
		#print '-------------------------'
		if event.name in self.mlist:
			fevent.close(event.name)

    def process_IN_MOVED_TO(self, event):
		#print 'get a mv to event'     
		return

if __name__ == '__main__':
    #print getFileList('/dev/shm/flow') 
    os.system("sysctl -n -w fs.inotify.max_user_watches=65535")
    os.system("sysctl -n -w fs.inotify.max_user_instances=1024")
    os.system("sysctl -n -w fs.inotify.max_queued_events=32000")
    # watch manager
    mask = pyinotify.IN_CLOSE_WRITE|pyinotify.IN_CREATE|pyinotify.IN_MOVED_TO
	#monitor files name
    mlist = ['test.py']
    fevent = Event(mlist)
    handler = EventHandler(fevent)
    wm = pyinotify.WatchManager()
    wm.add_watch('/root/yxd/autoTest', mask, rec=True)
    wm.add_watch('/root/yxd/ll', mask, rec=True)
    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()
