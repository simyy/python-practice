import socket
import fcntl
import struct


"""
获取主机ip地址
参数ifname: 通过'lo'获取的为环回地址, 通过'eth0'获取的为主机ip地址
"""
def get_ip_address(ifname='eth0'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),  
            0x8915, # SIOCGIFADDR  
            struct.pack('256s', ifname[:15])  
        )[20:24]) 
    except:
        ips = os.popen("LANG=C ifconfig | grep \"inet addr\" | grep -v \"127.0.0.1\" | awk -F \":\" '{print $2}' | awk '{print $1}'").readlines()
        if len(ips) > 0:
            return ips[0]
    return ''
