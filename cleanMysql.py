#!/usr/bin/env pthon
# -*- coding: utf-8 -*-

import time
import MySQLdb

def cleanVistHistory():
    conn = MySQLdb.connect(host = 'localhost', port = 3306,\
           charset = "utf8", user = 'xxx', passwd = 'xxx',\
           db = 'xxx')
    cursor = conn.cursor()
    current_date = time.strftime('%Y%m%d', time.localtime(time.time()-310))
    delete_table_sql = "DROP TABLE uri_visit_" + current_date
    #print delete_table_sql
    try:
        cursor.execute(delete_table_sql)
        cursor.execute("commit")
        print 'clean VisitHistory today'
    except:
        print 'no visitHistory today'
    delete_table_sql = "DROP TABLE tcpflow_" + current_date
    try:
        cursor.execute(delete_table_sql)
        cursor.execute("commit")
        print 'clean TcpflowHistory today'
    except:
        print 'no TcpflowHistory today'
    return

def cleanWarnList():
    conn = MySQLdb.connect(host = 'localhost', port = 3306,\
           charset = "utf8", user = 'xxx', passwd = 'xxx',\
           db = 'xxx')
    cursor = conn.cursor()
    current_date = time.strftime('%Y%m%d', time.localtime(time.time()-310))
    delete_table_sql = "DROP TABLE warn_block_record_" + current_date
    #print delete_table_sql
    try:
        cursor.execute(delete_table_sql)
        cursor.execut("commit")
        print 'clean warn_block_record today'
    except:
        print 'no warn_block_record today'  
    return


def Main():
    cleanVistHistory()
    cleanWarnList()

if __name__ == '__main__':
   Main()
