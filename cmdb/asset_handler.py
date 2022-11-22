import json
from cmdb import models


class NewAsset(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': self.data.get('ram_size'),
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),

        }
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults)

        return '资产已经加入或更新待审批区！'

def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    """
    记录日志
    """
    event = models.EventLog()
    if log_type == "upline":
        event.name = "%s <%s> ：  上线" % (asset.name, asset.sn)
        event.asset = asset
        event.detail = "资产成功上线！"
        event.user = request.user
    elif log_type == "approve_failed":
        event.name = "%s <%s> ：  审批失败" % (new_asset.asset_type, new_asset.sn)
        event.new_asset = new_asset
        event.detail = "审批失败！\n%s" % msg
        event.user = request.user
    # 更多日志类型.....
    event.save()        

class ApproveAsset:
    """
    审批资产并上线。
    """
    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        # 为以后的其它类型资产扩展留下接口
        func = getattr(self, "_%s_upline" % self.new_asset.asset_type)
        ret = func()
        return ret

    def _server_upline(self):
        # 在实际的生产环境中，下面的操作应该是原子性的整体事务，任何一步出现异常，所有操作都要回滚。
        asset = self._create_asset()  # 创建一条资产并返回资产对象。注意要和待审批区的资产区分开。
        try:
            self._create_manufacturer(asset) # 创建厂商
            self._create_server(asset)       # 创建服务器
            self._create_CPU(asset)          # 创建CPU
            self._create_RAM(asset)          # 创建内存
            self._create_disk(asset)         # 创建硬盘
            self._create_nic(asset)          # 创建网卡
            self._delete_original_asset()    # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=e, new_asset=self.new_asset, request=self.request)
            print(e)
            return False
        else:
            # 添加日志
            log("upline", asset=asset, request=self.request)
            print("新服务器上线!")
            return True

    def _create_asset(self):
        """
        创建资产并上线
        :return:
        """
        # 利用request.user自动获取当前管理人员的信息，作为审批人添加到资产数据中。
        asset = models.Asset.objects.create(asset_type=self.new_asset.asset_type,
                                            name="%s: %s" % (self.new_asset.asset_type, self.new_asset.sn),
                                            sn=self.new_asset.sn,
                                            approved_by=self.request.user,
                                            )
        return asset

    def _create_manufacturer(self, asset):
        """
        创建厂商
        :param asset:
        :return:
        """
        # 判断厂商数据是否存在。如果存在，看看数据库里是否已经有该厂商，再决定是获取还是创建。
        m = self.new_asset.manufacturer
        if m:
            manufacturer_obj, _ = models.Manufacturer.objects.get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()

    def _create_server(self, asset):
        """
        创建服务器
        :param asset:
        :return:
        """
        models.Server.objects.create(asset=asset,
                                     model=self.new_asset.model,
                                     os_type=self.new_asset.os_type,
                                     os_distribution=self.new_asset.os_distribution,
                                     os_release=self.new_asset.os_release,
                                     )

    def _create_CPU(self, asset):
        """
        创建CPU.
        教程这里对发送过来的数据采取了最大限度的容忍，
        实际情况下你可能还要对数据的完整性、合法性、数据类型进行检测，
        根据不同的检测情况，是被动接收，还是打回去要求重新收集，请自行决定。
        这里的业务逻辑非常复杂，不可能面面俱到。
        :param asset:
        :return:
        """
        cpu = models.CPU.objects.create(asset=asset)
        cpu.cpu_model = self.new_asset.cpu_model
        cpu.cpu_count = self.new_asset.cpu_count
        cpu.cpu_core_count = self.new_asset.cpu_core_count
        cpu.save()

    def _create_RAM(self, asset):
        """
        创建内存。通常有多条内存
        :param asset:
        :return:
        """
        ram_list = self.data.get('ram')
        if not ram_list:    # 万一一条内存数据都没有
            return
        for ram_dict in ram_list:
            if not ram_dict.get('slot'):
                raise ValueError("未知的内存插槽！")  # 使用虚拟机的时候，可能无法获取内存插槽，需要你修改此处的逻辑。
            ram = models.RAM()
            ram.asset = asset
            ram.slot = ram_dict.get('slot')
            ram.sn = ram_dict.get('sn')
            ram.model = ram_dict.get('model')
            ram.manufacturer = ram_dict.get('manufacturer')
            ram.capacity = ram_dict.get('capacity', 0)
            ram.save()

    def _create_disk(self, asset):
        """
        存储设备种类多，还有Raid情况，需要根据实际情况具体解决。
        这里只以简单的SATA硬盘为例子。可能有多块硬盘。
        :param asset:
        :return:
        """
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:  # 一条硬盘数据都没有
            return
        for disk_dict in disk_list:
            if not disk_dict.get('sn'):
                raise ValueError("未知sn的硬盘！")  # 根据sn确定具体某块硬盘。
            disk = models.Disk()
            disk.asset = asset
            disk.sn = disk_dict.get('sn')
            disk.model = disk_dict.get('model')
            disk.manufacturer = disk_dict.get('manufacturer'),
            disk.slot = disk_dict.get('slot')
            disk.capacity = disk_dict.get('capacity', 0)
            iface = disk_dict.get('interface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                disk.interface_type = iface

            disk.save()

    def _create_nic(self, asset):
        """
        创建网卡。可能有多个网卡，甚至虚拟网卡。
        :param asset:
        :return:
        """
        nic_list = self.data.get("nic")
        if not nic_list:
            return

        for nic_dict in nic_list:
            if not nic_dict.get('mac'):
                raise ValueError("网卡缺少mac地址！")
            if not nic_dict.get('model'):
                raise ValueError("网卡型号未知！")

            nic = models.NIC()
            nic.asset = asset
            nic.name = nic_dict.get('name')
            nic.model = nic_dict.get('model')
            nic.mac = nic_dict.get('mac')
            nic.ip_address = nic_dict.get('ip_address')
            if nic_dict.get('net_mask'):
                if len(nic_dict.get('net_mask')) > 0:
                    nic.net_mask = nic_dict.get('net_mask')[0]
            nic.save()

    def _delete_original_asset(self):
        """
        这里的逻辑是已经审批上线的资产，就从待审批区删除。
        也可以设置为修改成已审批状态但不删除，只是在管理界面特别处理，不让再次审批，灰色显示。
        不过这样可能导致待审批区越来越大。
        :return:
        """
        self.new_asset.delete()    