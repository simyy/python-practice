#!/usr/bin/env python
# encoding: utf-8

import os
import re
import socket
import time
import sys
import subprocess


def test(v):
    test.result = v
    return v


def Int2StringNetmask(netmaskInt):
    netmaskInt = int(netmaskInt)
    netmask = []
    while netmaskInt > 7:
        netmask.append('255')
        netmaskInt = netmaskInt - 8
    if netmaskInt != 0:
        netmask.append(str(int('1' * netmaskInt + '0' * (8 - netmaskInt), 2)))
    if len(netmask) < 4:
        netmask.extend(['0'] * (4 - len(netmask)))
    return '.'.join(netmask)


def String2IntNetmask(str):
    n = 0
    for item in str.split('.'):
        if item == '255':
            n += 8
        elif item == '0':
            continue
        else:
            m = bin(int(item, 10))[2:]
            n += len(m.replace('0', ''))
    return n


def get_ip_netmask(ip_address):
    ip, netmask = ip_address.split('/')
    return ip, Int2StringNetmask(netmask)


def gen_ip_address(ip, netmask):
    return '%s/%d' % (ip, String2IntNetmask(netmask))


def isIPV4(ipv4):
    try:
        socket.inet_aton(ipv4)
    except socket.error:
        return False
    return True


def isDomainName(addr):
    if re.match(r'^(\w+\.)+\w+$', addr):
        return True
    return False

def isTime(t):
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', t):
        return True
    return False


def isNETMASK(netmask):
    NETMASK = (
        "0.0.0.0",
        "128.0.0.0", 
        "192.0.0.0",
        "224.0.0.0",
        "240.0.0.0",
        "248.0.0.0",
        "252.0.0.0",
        "254.0.0.0",
        "255.0.0.0",
        "255.128.0.0", 
        "255.192.0.0",
        "255.224.0.0",
        "255.240.0.0",
        "255.248.0.0",
        "255.252.0.0",
        "255.254.0.0",
        "255.255.0.0",
        "255.255.128.0",
        "255.255.192.0", 
        "255.255.224.0",
        "255.255.240.0",
        "255.255.248.0",
        "255.255.252.0",
        "255.255.254.0",
        "255.255.255.0",
        "255.255.255.128",  
        "255.255.255.192",
        "255.255.255.224",
        "255.255.255.240",
        "255.255.255.248",
        "255.255.255.252",
        "255.255.255.254",
        "255.255.255.255",
    )
    if netmask not in NETMASK:
        return False
    return True


def isIPV6(ipv6):
    ipv6 = ipv6.split('/')
    if len(ipv6) != 2:
        return False
    try:
        socket.inet_pton(socket.AF_INET6, ipv6[0])
    except socket.error:
        return False
    return True


def get_interfaces():
    """
    获取所有网络接口信息
    遇到任何
    """
    interfaces = {}
    for line in os.popen('ip -o addr show'):
        if test(re.match('^(\d+):\s+(\w+):\s+<(.+?)>\s+.+?state\s+(\w+)\s+.+?link/(\w+)\s+(\S+)\s+.+?\n$', line)):
            m = test.result
            flags = m.group(3).split(',')
            if 'LOOPBACK' in flags:
                continue
            interfaces[m.group(2)] = {
                #'enabled': 'UP' in flags,
                'connected': {'UP': True, 'DOWN': False}.get(m.group(4)),
                'mac': m.group(6),
                'ipv4': "",
                'ipv6': "",
                'netmask': "",
            }
        elif test(re.match('^\d+:\s+(\w+)\s+inet\s+(\S+)\s+.+?\n$', line)):
            m = test.result
            name = m.group(1)
            interface = interfaces.get(name)
            if not interface:
                continue
            ip, mask = m.group(2).split('/')
            interface['ipv4'] = ip
            interface['netmask'] = Int2StringNetmask(mask)
        elif test(re.match('^\d+:\s+(\w+)\s+inet6\s+(\S+)\s+.+?\n$', line)):
            m = test.result
            name = m.group(1)
            interface = interfaces.get(name)
            if not interface:
                continue
            interface['ipv6'] = m.group(2)
    return interfaces


def get_name_servers():
    """
    获取域名服务器IP地址列表
    """
    name_servers = list()
    for line in open('/etc/resolv.conf'):
        if test(re.match('^\s*nameserver\s+(\S+)\s*\n$', line)):
            name_servers.append(test.result.group(1))
    return name_servers


def get_route():
    """
    获取路由信息

    Params
    ----------------
    ip: IP 
    interface： dev
    status: 连接状态
    type: 默认路由或自定义路由
    src: 源地址
    dst：目的地址
    """
    routes = {}
    for dev in ['eth0', 'eth1']:
        if not os.path.exists('/etc/sysconfig/network-scripts/route-%s' % dev):
            continue
        with open('/etc/sysconfig/network-scripts/route-%s' % dev) as f:
            for line in f.readlines():
                if test(re.match('^\s*default\s+via\s+(\S+)\s+$', line)):
                    m = test.result
                    default_route = {
                        'ip': m.group(1),
                        'interface': dev,
                        'status': 0,
                        'type': 0,
                    }
                    routes['default'] = default_route
                elif test(re.match('^\s*(\S+)\s+via\s+(\S+)\s+$', line)):
                    m = test.result
                    other_route = {
                        'dst': m.group(1),
                        'src': m.group(2),
                        'interface': dev,
                        'status': 0,
                        'type': 1,
                    }
                    routes['other'] = other_route
    for line in os.popen('ip route show'):
        if test(re.match('^\s*default\s+via\s+(\S+)\s+dev\s+(\S+)\s*\n$', line)):
            m = test.result
            default_route = {
                'ip': m.group(1),
                'interface': m.group(2),
                'status': 1,
                'type': 0,
            }
            routes['default']['status'] = 1
        elif test(re.match('^\s*(\S+)\s+via\s+(\S+)\s+dev\s+(\S+)\s*\n$', line)):
            m = test.result
            other_route = {
                'dst': m.group(1),
                'src': m.group(2),
                'interface': m.group(3),
                'status': 1,
                'type': 1,
            }
            routes['other']['status'] = 1
    return [value for key, value in routes.items()]


def get_ntpd():
    """
    获取NTPD信息

    """
    p = os.popen('service ntpd status')
    line = p.readline() 
    if 'stop' in line:
        status = False
    else:
        status = True
    p = os.popen('cat /etc/ntp.conf | grep ^server | head -1 | awk \'{print $2}\'') 
    line = p.readline()
    addr = line.strip()
    return {"status":status, "addr":addr}    


def update_ntpd(addr, path="/etc/"):
    """
    更新NTPD默认服务器
    """ 
    p = os.popen('cat %sntp.conf' % path)
    lines = p.readlines()  
    r = filter(lambda x:re.match(r'^server .*\n', x), lines)
    if r:
        cmd = 'sed -i "/^%s/s/.*/server %s/" %sntp.conf' % (r[0][:-1], addr, path)
    else:
        cmd = 'echo "server %s" >> %sntp.conf' % (addr, path)
    os.popen(cmd)
    os.popen('service ntpd restart')
   

def set_ip_address(interface, ip, netmask):
    """
    设置某网络接口的IP地址
    """
    HWADDR = os.popen("cat /etc/sysconfig/network-scripts/ifcfg-%s | grep HWADDR |"
                      " awk -F'\"' '{print $2}'" % interface).readline().strip()
    NETWORK = ip[:ip.rfind('.')+1] + '0'
    content = "DEVICE=%s\nBOOTPROTO=static\nONBOOT=yes\nHWADDR=%s\nIPADDR=%s\n"\
              "NETMASK=%s\nNETWORK=%s\nTYPE=Ethernet\nUSERCTL=no\nPEERDNS=yes\nIPV6INIT=no" % \
              (interface, HWADDR, ip, netmask, NETWORK)
    with open('/etc/sysconfig/network-scripts/ifcfg-%s' % interface, 'w') as f:
        f.write(content)


def set_name_servers(name_servers):
    """
    设置域名服务器地址
    name_servers 为DNS列表
    """
    with open('/etc/resolv.conf', 'w') as fp:
        for name_server in name_servers:
            fp.write('nameserver %s%s' % (name_server, os.linesep))


def set_route(default, other):
    """
    设置路由
   
    Params
    -----------------
    default: 默认路由
    other: 其他路由配置，格式[dst, gw]
    """
    cmd = 'route del default > /dev/null; route add default gw %s > /dev/null; route -n | awk \'$2=="%s"{print $8}\'' % (default, default)
    p = os.popen(cmd)
    default_dev = p.readline().strip()

    dst = other[0].split('/')[0]
    src = other[1]
    cmd = 'route add %s gw %s > /dev/null; route -n | awk \'$2=="%s"{print $8}\'' \
          % (dst, src, src)
    p = os.popen(cmd)
    other_dev = p.readline().strip()

    os.system('rm -rf /etc/sysconfig/network-scripts/route-* > /dev/null')
    if default_dev == other_dev:
        with open('/etc/sysconfig/network-scripts/route-%s' % default_dev, 'w') as f:
            f.write('default via %s\n%s via %s' % (default, other[0], other[1]))
    else:
        with open('/etc/sysconfig/network-scripts/route-%s' % default_dev, 'w') as f:
            f.write('default via %s' % default)
        with open('/etc/sysconfig/network-scripts/route-%s' % other_dev, 'w') as f:
            f.write('%s via %s' % (other[0], other[1]))


def shut_down():
    """
    关闭服务器
    """
    os.system('shutdown -h now')


def restart():
    """
    关机重启
    """
    os.system('shutdown -r now') 


def restart_network():
    os.system('service network restart')


def restart_all_service():
    """
    重启所有服务
    所有服务应该由supervisor控制
    """
    os.system('supervisorctl restart all')


def command_run(command, timeout=5):
    proc = subprocess.Popen(command,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    poll_seconds = .250
    deadline = time.time() + timeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)
    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            proc.terminate()
    stdout,stderr = proc.communicate()
    return stdout,stderr,proc.returncode


def access_test(ip):
    cmd = "ping -c 2 %s | grep transmitted | awk -F',' '{print $2}' | awk '{print $1}'" % ip
    stdout, stderr, code = command_run(cmd)
    try:
        if stdout:
            if stdout.strip() == '2':
                return True
    except:
        pass
    return False


def mytest():
    #set_ip_address("eth1", "192.168.37.8", "255.255.255.0")
    #set_name_servers(["8.8.8.8", "144.144.144.144"])
    #set_gateway("10.18.25.1")
    #set_route('192.168.36.1', ['10.18.25.0/24', '10.18.208.1'] )
    print get_route()
    pass
    


if __name__ == '__main__':
    mytest()
