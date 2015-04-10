#python2.7.8

import pwd
import grp
import os

uid = pwd.getpwnam("nobody").pw_uid
gid = grp.getgrnam("nogroup").gr_gid
path = '/tmp/f.txt'
os.chown(path, uid, gid)
