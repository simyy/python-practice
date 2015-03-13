#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                                   
import os
import sys
import paramiko                                                                                           

localPath = '/home/'                                                              
remotePath = '/home/                                                                    

def init_sftp():                                                                                          
    privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')                                                  
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)                                         
    username = 'admin'                                                                                 
    transport = paramiko.Transport(("192.168.0.2",22))                                                    
    transport.connect(username = username, pkey = mykey)                                                  
    sftp = paramiko.SFTPClient.from_transport(transport)                                                  
    return sftp, transport
    
def run():  
    sftp, transport = init_sftp()                                                                         
    sftp.put('/home/test', '/home/test')                                                
    sftp.close()                                                                                          
    transport.close() 
