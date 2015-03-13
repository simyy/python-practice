from DBUtils.PooledDB import PooledDB
import MySQLdb
pool = PooledDB(MySQLdb, 5, host="127.0.0.1", user="root", passwd="123123", db="test")


db = pool.connection()
cur = db.cursor()
cur.execute("create table if not exists test1(k char(32), v int)")
cur.execute("insert into test1 values('k1', 1)")
cur.execute("insert into test1 values('k2', 2)")
cur.execute("insert into test1 values('k3', 3)")
cur.close()
db.commit()
db.close()

db = pool.connection()
cur = db.cursor()
cur.execute("select * from test1")
reslut = cur.fetchall()
cur.close()
db.close()
print reslut

 