# import psutil
# import datetime
# import time
# def func1():
#     # CPU的逻辑核数
#     cpu_count = psutil.cpu_count()
#     # cpu的使用率
#     cup_per = psutil.cpu_percent(interval=0.5) # 0.5刷新频率
#     print(f"cpu的逻辑核数为{cpu_count},cpu的平均使用率为{cup_per}")
#     # 内存信息
#     memory_info = psutil.virtual_memory()
#     # 总内存
#     memory_total = memory_info.total / 1024 / 1024
#     # 内存使用率
#     #memory_per = (memory_total - memory_info.available) / memory_total * 100
#     memory_per = memory_info.percent
#     print(f"总内存大小为{memory_total}M,内存的使用率为{memory_per}")
#     # 硬盘信息
#     disk_info = psutil.disk_usage("/") # 根目录磁盘信息
#     #print(disk_info)
#     # 根目录大小
#     disk_total = disk_info.total
#     # 根目录使用情况
#     disk_per = float(disk_info.used / disk_total * 100 )
#     print(f"根目录大小为{disk_total / 1024 / 1024}M，根目录使用率为{round(disk_per,2)}")
#     # 网络使用情况
#     net = psutil.net_io_counters()
#     #print(net)
#     # 网卡配置信息
#     net_ipy = psutil.net_if_addrs()
#     #print(f"net_ipy {net_ipy}")
#     net_ip = net_ipy['enp0s31f6'][0][1]
#     print(f"本机的IP地址为{net_ip}")
#     # 收取数据
#     net_recv = float( net.bytes_recv / 1024 /1024)
#     # 发送数据
#     net_sent = float(net.bytes_sent /1024 /1024)
#     print(f"网络收取{round(net_recv,2)}M的数据，发送{round(net_sent,2)}M的数据")
#     # 获取当前系统时间
#     current_time = datetime.datetime.now().strftime("%F %T") # %F年月日 %T时分秒
#     print(f"当前时间是：{current_time}")
#     time.sleep(1)
 
# start = time.time()
# end = time.time()
# count = 0
# while end - start <= 10:
#     count += 1
#     end = time.time()
#     print(f"执行第{count}次".center(50,'*'))
#     func1()

import psutil
from subprocess import PIPE
p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"],stdout=PIPE)
p.name()
p.username()