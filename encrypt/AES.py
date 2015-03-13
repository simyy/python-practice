"""
AES with xor encrypt and decrypt
"""

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto import Random
from pyDes import *
import base64
import itertools
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

key  = 'test1234'
salt = 'test1234'

class prpcrypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC

    #加密函数，如果text不足16位就用空格补足为16位，
    #如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self,text):
        #iv = Random.new().read(AES.block_size)
        cryptor = AES.new(self.key,self.mode, b'0000000000000000')
        #这里密钥key 长度必须为16（AES-128）,
        #24（AES-192）,或者32 （AES-256）Bytes 长度
        #目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        #所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode, b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

def encrypt(str):
    pc  = prpcrypt(key) #初始化密钥
    xor = ''.join([ chr(ord(x)^ord(y)) for x, y in zip(str, itertools.cycle(salt)) ])
    en  = pc.encrypt(xor)
    res = en[32:64] + '/' + en[0:32] + '/' + en[64:]
    return res

def decrypt(sstr):
    tmp = sstr.split('/')
    str = tmp[1] + tmp[0] + tmp[2]
    pc = prpcrypt(key) #初始化密钥
    xor = pc.decrypt(str)
    #for x, y in zip(xor, itertools.cycle(salt)):
    #    print x,y
    sr = ''.join([ chr(ord(x)^ord(y)) for x, y in zip(xor, itertools.cycle(salt)) ])
    return sr
    
