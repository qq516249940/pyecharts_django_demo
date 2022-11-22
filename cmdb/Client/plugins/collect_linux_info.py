#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess
import psutil


def collect():
    filter_keys = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
    raw_data = {}

    for key in filter_keys:
        try:
            res = subprocess.Popen("sudo dmidecode -t system|grep '%s'" % key,
                                   stdout=subprocess.PIPE, shell=True)
            result = res.stdout.read().decode()
            data_list = result.split(':')

            if len(data_list) > 1:
                raw_data[key] = data_list[1].strip()
            else:
                raw_data[key] = ''
        except Exception as e:
            print(e)
            raw_data[key] = ''

    data = dict()
    data['asset_type'] = 'server'
    data['manufacturer'] = raw_data['Manufacturer']
    data['sn'] = raw_data['Serial Number']
    data['model'] = raw_data['Product Name']
    data['uuid'] = raw_data['UUID']
    data['wake_up_type'] = raw_data['Wake-up Type']

    data.update(get_os_info())
    data.update(get_cpu_info())
    data.update(get_ram_info())
    data.update(get_nic_info())
    data.update(get_disk_info())
    return data


def get_os_info():
    """
    获取操作系统信息
    :return:
    """
    distributor = subprocess.Popen("lsb_release -a|grep 'Distributor ID'",
                                   stdout=subprocess.PIPE, shell=True)
    distributor = distributor.stdout.read().decode().split(":")

    release = subprocess.Popen("lsb_release -a|grep 'Description'",
                               stdout=subprocess.PIPE, shell=True)

    release = release.stdout.read().decode().split(":")
    data_dic = {
        "os_distribution": distributor[1].strip() if len(distributor) > 1 else "",
        "os_release": release[1].strip() if len(release) > 1 else "",
        "os_type": "Linux",
    }
    return data_dic


def get_cpu_info():
    """
    获取cpu信息
    :return:
    """
    raw_cmd = 'cat /proc/cpuinfo'

    raw_data = {
        'cpu_model': "%s |grep 'model name' |head -1 " % raw_cmd,
        'cpu_count':  "%s |grep  'processor'|wc -l " % raw_cmd,
        'cpu_core_count': "%s |grep 'cpu cores' |awk -F: '{SUM +=$2} END {print SUM}'" % raw_cmd,
    }

    for key, cmd in raw_data.items():
        try:
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            raw_data[key] = result.stdout.read().decode().strip()
        except ValueError as e:
            print(e)
            raw_data[key] = ""

    data = {
        "cpu_count": raw_data["cpu_count"],
        "cpu_core_count": raw_data["cpu_core_count"]
        }

    cpu_model = raw_data["cpu_model"].split(":")

    if len(cpu_model) > 1:
        data["cpu_model"] = cpu_model[1].strip()
    else:
        data["cpu_model"] = ''

    return data


def get_ram_info():
    """
    获取内存信息
    :return:
    """
    raw_total_size = psutil.virtual_memory().total/1024/1024/1024  # 字节转换为GB

    ram_data = {'ram': []}
    ram_data['ram_size'] = raw_total_size

    return ram_data


def get_nic_info():
    """
    获取网卡信息
    :return:
    """
    raw_data = subprocess.Popen("ifconfig -a", stdout=subprocess.PIPE, shell=True)

    raw_data = raw_data.stdout.read().decode().split("\n")

    nic_dic = dict()
    next_ip_line = False
    last_mac_addr = None

    for line in raw_data:
        if next_ip_line:
            next_ip_line = False
            nic_name = last_mac_addr.split()[0]
            mac_addr = last_mac_addr.split("HWaddr")[1].strip()
            raw_ip_addr = line.split("inet addr:")
            raw_bcast = line.split("Bcast:")
            raw_netmask = line.split("Mask:")
            if len(raw_ip_addr) > 1:
                ip_addr = raw_ip_addr[1].split()[0]
                network = raw_bcast[1].split()[0]
                netmask = raw_netmask[1].split()[0]
            else:
                ip_addr = None
                network = None
                netmask = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {'name': nic_name,
                                     'mac': mac_addr,
                                     'net_mask': netmask,
                                     'network': network,
                                     'bonding': 0,
                                     'model': 'unknown',
                                     'ip_address': ip_addr,
                                     }
            else:
                if '%s_bonding_addr' % (mac_addr,) not in nic_dic:
                    random_mac_addr = '%s_bonding_addr' % (mac_addr,)
                else:
                    random_mac_addr = '%s_bonding_addr2' % (mac_addr,)

                nic_dic[random_mac_addr] = {'name': nic_name,
                                            'mac': random_mac_addr,
                                            'net_mask': netmask,
                                            'network': network,
                                            'bonding': 1,
                                            'model': 'unknown',
                                            'ip_address': ip_addr,
                                            }

        if "HWaddr" in line:
            next_ip_line = True
            last_mac_addr = line
    nic_list = []
    for k, v in nic_dic.items():
        nic_list.append(v)

    return {'nic': nic_list}


def get_disk_info():
    """
    获取存储信息。
    本脚本只针对ubuntu中使用sda，且只有一块硬盘的情况。
    具体查看硬盘信息的命令，请根据实际情况，实际调整。
    如果需要查看Raid信息，可以尝试MegaCli工具。
    :return:
    """
    result =         {
            "model": "VBOX HARDDISK",
            "size": "50",
            "sn": "VBeee1ba73-09085302"
        }

    return result


if __name__ == "__main__":
    # 收集信息功能测试
    data = collect()
    print(data)