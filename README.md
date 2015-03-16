#simplePython

>一些python封装的模块，可以提高开发效率。

##db数据库模块
>包含一些数据库模块

* DB.py 封装的MySQLdb模块
* DBPool.py封装了DBUtils、MySQLdb的数据库线程池

##encrypt加密模块
>包含AES、DES加密模块

* AES.py 封装Crypto的AES加密（AES+异或）
* DES.py 封装Crypto的DES加密

##network网络模块
>包含添加rsa-key、获取本地地址、sftp、解析HTML、扫描IP、socket模块

* BatchKey.py 批量设置免密码的SSH登陆
* GetIpAddress.py 获取主机IP地址
* ParamikoSftp.py SFTP通信
* ParseHtml.py 解析HTML
* ScanIp.py 扫描局域网IP
* ServerSocket.py socket服务器

##weibo_api
>微博API的二次开发

* weibo.py 原微博python的API
* weibo_api.py 二次封装

* GenerateVertifyCode.py 生成验证码
* Inotify.py linux监控文件变化的inotify
* Log.py logging的配置方法
* ProcessManager.py 进程管理
* Timer.py 类似crontab的定时库的封装
