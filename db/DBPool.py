#!/usr/bin/env python
#-*- encoding:utf-8 -*-

'''
使用DBUtils来实现数据库线程池
'''

import MySQLdb
from DBUtils.PooledDB import PooledDB
from MySQLdb.cursors import DictCursor

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'123123',
    'db':'test',
    'charset':'utf8'
}

class DB(object):
    '''

    '''
    _pool = None

    def __init__(self):
        self._conn = DB._getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def _getConn():
        if DB._pool is None:
            try:
                DB._pool = PooledDB(
                    MySQLdb,
                    mincached=1,
                    maxcached=20,
                    maxusage=100,
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    passwd='123123',
                    db='test',
                    cursorclass=DictCursor
                )
            except Exception as e:
                print 'dbpoll error:',e
        return DB._pool.connection()

    def _query(self, sql, param):
        '''
        sql请求
        :param sql: sql语句
        :param param: 参数
        :return: 返回查询数量，错误返回False
        '''
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
        except Exception as e:
            print e
            return False
        return count

    def queryAll(self, sql, param=None):
        '''
        查询并返回所有数据
        :param sql: sql select语句
        :param param: 参数
        :return: 返回请求结果，错误返回False
        '''
        count = self._query(sql, param)
        if count == False or count < 0:
            return False
        elif count > 0:
            try:
                result = self._cursor.fetchall()
            except Exception as e:
                print e
                result = False
        return result

    def queryOne(self, sql, param=None):
        '''
        查询并返回一条数据
        :param sql: sql select语句
        :param param: 参数
        :return: 返回请求结果，错误返回False
        '''
        count = self._query(sql, param)
        if count == False or count < 0:
            return False
        elif count > 0:
            try:
                result = self._cursor.fethone()
            except Exception as e:
                print e
                result = False
        return False

    def queryMany(self, sql, num, param=None):
        '''
        查询并返回num个数据
        :param sql: sql select语句
        :param num: 请求数量
        :param param: 参数
        :return: 返回请求结果
        '''
        count = self._query(sql, param)
        if count == False or count < 0:
            return False
        elif count > 0:
            try:
                result = self._cursor.fetchmany(num)
            except Exception as e:
                print e
                result = False
        return result

    def _getInsertId(self):
        '''
        :return: 获取当前连接最后一次插入操作生成的id,如果没有则为０
        '''
        try:
            self._cursor.execute('SELECT @@IDENTITY AS id')
            result = self._cursor.fetchall()
        except Exception as e:
            print e
            return False
        return result[0]['id']

    def insertOne(self, sql, values):
        '''
        插入一条数据
        :sql: sql insert语句
        :param values: 插入数据
        :return: 返回id
        '''
        try:
            self._cursor.execute(sql, values)
        except Exception as e:
            print e
            return False
        return self._getInsertId()

    def insertMany(self, sql, values):
        '''
        插入多个数据
        :param sql: sql insert语句
        :param values: 插入数据
        :return: 返回插入数据数量
        '''
        try:
            count = self._cursor.executemany(sql,values)
        except Exception as e:
            print e
            return  False
        return count

    def update(self, sql, param=None):
        '''
        更新数据
        :param sql: sql update语句
        :param param: 参数
        :return: 返回更新数量
        '''
        try:
            count = self._query(sql, param)
        except Exception as e:
            print e
            return False
        return count

    def delete(self, sql, param=None):
        '''
        删除数据
        :param sql: sql delete语句
        :param param: 参数
        :return: 返回删除数量
        '''
        try:
            count = self._query(sql, param)
        except Exception as e:
            print e
            return False
        return count

    def begin(self):
        '''
        开始事务
        :return: 成功返回True,否则返回False
        '''
        try:
            pass
        except Exception as e:
            print e
            return False
        return True

    def end(self, option='commit'):
        '''
        结束事务或回滚
        :param option: 选择参数，提交事务
        :return: 成功返回True,否则返回False
        '''
        try:
            if option == 'commit':
                self._conn.commit()
            else:
                self._conn.rollback()
        except Exception as e:
            print e
            return False
        return True

    def dispose(self, isEnd=1):
        '''
        结束事务并关闭连接
        :param isEnd: commit or rollback
        :return: 成功返回True,否则返回False
        '''
        try:
            if isEnd == 1:
                self.end('commit')
            else:
                self.end('rollback')
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print e
            return False
        return True

if __name__ == '__main__':
    db = DB()
    #print db.insertOne('insert test (id) values (%s)', 3)
    #print db.insertOne('insert test (id) values (%s)', 4)
    #print db.queryAll('select * from test')
    #print db.update('update test set id=5 where id=1')
    #print db.queryAll('select * from test')
    db.begin()
    print 'begin'
    print db.insertOne('insert test (id) values (%s)', 15)
    print db.insertOne('insert test (id) values (%s)', 16)
    print db.queryAll('select * from test')
    print 'rollback'
    db.dispose(0)
    db1 = DB()
    print db1.queryAll('select * from test')
