#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
常用网络命令的python封装
"""

import os
import re
import socket


def Int2StringNetmask(netmaskInt):
    """
    24 => 255.255.255.0
    """
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
    """
    255.255.255.0 => 24
    """
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
    """
    127.0.0.1/24 返回 127.0.0.1 255.255.255.0
    """
    ip, netmask = ip_address.split('/')
    return ip, Int2StringNetmask(netmask)


def gen_ip_address(ip, netmask):
    """
    127.0.0.1 255.255.255.0 生成 127.0.0.1/24
    """
    return '%s/%d' % (ip, String2IntNetmask(netmask))


def isIPV4(ipv4):
    try:
        socket.inet_aton(ipv4)
    except socket.error:
        return False
    return True


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



def shut_down(cancel=False, delay=10):
    """
    关闭服务器
    默认延迟10秒关机
    cancel 为取消关机
    """
    if cancel:
        os.system('shutdown -c')
    else:
        os.system('shutdown -h %d' % timeout)


def restart():
    """
    关机重启
    """
    os.system('shutdown -r now')


def restart_all_service():
    """
    重启所有服务
    所有服务应该由supervisor控制
    """
    os.system('supervisorctl restart all')


 
def test(v):
    test.result = v
    return v
 
 
def get_interfaces():
    """
    获取所有网络接口信息
    遇到任何错误均抛出异常
    """
    interfaces = dict()
 
    # 获取接口名、索引号、启停状态、连接状态、硬件地址、IPv4地址
    for line in os.popen('ip -o addr show'):
        if test(re.match('^(\d+):\s+(\w+):\s+<(.+?)>\s+.+?state\s+(\w+)\s+.+?link/(\w+)\s+(\S+)\s+.+?\n$', line)):
            m = test.result
            # 这些标记的含义参见“/linux/if.h”中的“IFF_...”宏
            flags = m.group(3).split(',')
            # 去掉回环接口
            if 'LOOPBACK' in flags:
                continue
            interfaces[m.group(2)] = {
                'index': int(m.group(1)),
                'enabled': 'UP' in flags,
                'connected': {'UP': True, 'DOWN': False}.get(m.group(4)),
                'hardware_address': m.group(6),
                'wireless': False,
                'ip_addresses': list()
            }
        elif test(re.match('^\d+:\s+(\w+)\s+inet\s+(\S+)\s+.+?\n$', line)):
            m = test.result
            name = m.group(1)
            interface = interfaces.get(name)
            if not interface:
                # 此处就排除了上面去掉的接口，例如loopback接口
                continue
            interface['ip_addresses'].append(m.group(2))
 
    # 获取无线类型的接口
    for line in os.popen('iw dev'):
        if test(re.match('^\s+Interface\s+(\w+)\s*?\n$', line)):
            # 接口是否为wireless
            interfaces[test.result.group(1)]['wireless'] = True
 
    # 获取无线类型的接口的连接信息
    for name in interfaces:
        interface = interfaces[name]
        if interface['wireless']:
            for line in os.popen('iw dev %s link' % name):
                # 此处也可以通过“Connected ...”行判断是否已连接，但是上面已经判断了
                if test(re.match('^\s+SSID:\s+(\S+)\s*?\n$', line)):
                    # 获取SSID
                    interface['ssid'] = test.result.group(1)
 
    return interfaces
 
 
def get_default_route():
    """
    获取默认路由信息
    """
    default_route = None
 
    for line in os.popen('ip route show'):
        if test(re.match('^\s*default\s+via\s+(\S+)\s+dev\s+(\S+)\s*\n$', line)):
            m = test.result
            default_route = {
                'ip_address': m.group(1),
                'interface_name': m.group(2)
            }
            break
 
    return default_route
 
 
def get_name_servers():
    """
    获取域名服务器IP地址列表
    """
    name_servers = list()
 
    for line in open('/etc/resolv.conf'):
        if test(re.match('^\s*nameserver\s+(\S+)\s*\n$', line)):
            name_servers.append(test.result.group(1))
 
    return name_servers
 
 
def print_state(interfaces, default_route, name_servers):
    """
    打印所有网络接口、路由以及DNS信息
    """
    # 网络接口
    print('Network Interfaces:')
    print('    %10s  %8s  %17s  %s' % (
        'name',
        'type',
        'mac address',
        'state',
    ))
    print('    ----------  --------  -----------------  -----')
    for name in interfaces:
        interface = interfaces[name]
        state = list()
        if interface['enabled']:
            state.append('enabled')
        if interface['connected']:
            state.append('connected')
        if test(interface.get('ssid')):
            state.append('ssid:%s' % test.result)
        if len(interface['ip_addresses']):
            state.append('ip:%s' % ','.join(interface['ip_addresses']))
        print('    %10s  %8s  %17s  %s' % (
            name,
            'wireless' if interface['wireless'] else 'wired',
            interface['hardware_address'],
            ', '.join(state) if len(state) else 'N/A'
        ))
    print()
 
    # 默认路由
    print('Default Gateway:')
    if default_route:
        print('    ---> %s ---> %s' % (default_route['interface_name'], default_route['ip_address']))
    else:
        print('    N/A')
    print()
 
    # DNS
    print('DNS:')
    if len(name_servers):
        print('    %s' % ', '.join(name_servers))
    else:
        print('    N/A')
    print()
 
 
def cleanup_all(interfaces):
    """
    清理网络接口所有的设置、默认路由以及DNS
    """
    # 结束“supplicant”进程
    os.system('killall wpa_supplicant')
 
    # 禁用所有网络接口，删除所有IP地址以及路由
    for name in interfaces:
        os.system('ip link set %s down' % name)
        os.system('ip addr flush %s' % name)
 
    # 删除所有DNS地址
    open('/etc/resolv.conf', 'w').close()
 
 
def enable_interface(interface_name):
    """
    启用网络接口
    """
    os.system('ip link set %s up' % interface_name)
 
 
def disable_interface(interface_name):
    """
    禁用网络接口
    """
    os.system('ip link set %s down' % interface_name)
 
 
def get_ssids(interface_name):
    """
    扫描SSID
    """
    ssids = list()
 
    for line in os.popen('iw dev %s scan' % interface_name):
        if test(re.match('^\s+SSID:\s+(\S+)\s*?\n$', line)):
            ssids.append(test.result.group(1))
 
    return ssids
 
 
def connect_wireless(interface_name, ssid):
    """
    连接非加密的无线网
    """
    os.system('iw dev %s connect -w %s' % (interface_name, ssid))
 
 
def connect_wireless_with_wep(interface_name, ssid, keys):
    """
    连接WEP加密的无线网
    """
    os.system('iw dev %s connect -w %s key %s' % (interface_name, ssid, ' '.join(keys)))
 
 
def connect_wireless_with_wpa(interface_name, ssid, key):
    """
    连接WPA加密的无线网
    """
    os.system(
        'wpa_supplicant -i %s -D nl80211,wext -s -B -P /var/run/wpa_supplicant.%s.pid -C /var/run/wpa_supplicant' % (
            interface_name, interface_name
        ))
    os.system('wpa_cli -i %s add_network' % interface_name)
    os.system('wpa_cli -i %s set_network 0 ssid \'"%s"\'' % (interface_name, ssid))
    os.system('wpa_cli -i %s set_network 0 key_mgmt WPA-PSK' % interface_name)
    os.system('wpa_cli -i %s set_network 0 psk \'"%s"\'' % (interface_name, key))
    os.system('wpa_cli -i %s enable_network 0' % interface_name)
 
 
def disconnect_wireless(interface_name):
    """
    关闭无线连接
    """
    pattern = '^\s*\S+\s+(\S+)\s+.+?wpa_supplicant.%s.pid.+?\n$' % interface_name
    for line in os.popen('ps aux'):
        if test(re.match(pattern, line)):
            pid = test.result.group(1)
            os.system('kill -9 %s' % pid)
    os.system('iw dev %s disconnect' % interface_name)
 
 
def set_dhcp(interface_name):
    """
    使用DHCP设置接口
    """
    os.system('dhclient -r %s' % interface_name)
    os.system('dhclient %s' % interface_name)
 
 
def set_ip_addresses(interface_name, ip_addresses):
    """
    设置某网络接口的IP地址
    """
    os.system('ip addr flush %s' % interface_name)
    for ip_address in ip_addresses:
        os.system('ip addr add %s dev %s' % (ip_address, interface_name))
 
 
def set_default_route(interface_name, ip_address):
    """
    设置默认路由
    """
    os.system('ip route del default')
    os.system('ip route add default via %s dev %s' % (ip_address, interface_name))
 
 
def set_name_servers(name_servers):
    """
    设置域名服务器地址
    """
    with open('/etc/resolv.conf', 'w') as fp:
        for name_server in name_servers:
            fp.write('nameserver %s%s' % (name_server, os.linesep))
