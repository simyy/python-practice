"""
DES with base64 encrypt and decrypt
"""
from pyDes import *
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

key = 'test1234'

def encrypt_Des(str):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(str))

def decrypt_Des(str):
    k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(str))
