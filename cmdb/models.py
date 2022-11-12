from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Asset(models.Model):
    """    所有资产的共有数据表    """

    asset_type_choice = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '存储设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
    )

    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )

    asset_type = models.CharField(
        choices=asset_type_choice, max_length=64, default='server', verbose_name="资产类型")
    name = models.CharField(max_length=64, unique=True,
                            verbose_name="资产名称")     # 不可重复
    sn = models.CharField(max_length=128, unique=True,
                          verbose_name="资产序列号")  # 不可重复
    business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
                                      on_delete=models.SET_NULL)
    status = models.SmallIntegerField(
        choices=asset_status, default=0, verbose_name='设备状态')

    manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商',
                                     on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name='管理IP')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin',
                              on_delete=models.SET_NULL)
    idc = models.ForeignKey('IDC', null=True, blank=True,
                            verbose_name='所在机房', on_delete=models.SET_NULL)
    # contract = models.ForeignKey(
    #     'Contract', null=True, blank=True, verbose_name='合同', on_delete=models.SET_NULL)

    purchase_day = models.DateField(null=True, blank=True, verbose_name="购买日期")
    expire_day = models.DateField(null=True, blank=True, verbose_name="过保日期")
    price = models.FloatField(null=True, blank=True, verbose_name="价格")

    approved_by = models.ForeignKey(User, null=True, blank=True, verbose_name='批准人', related_name='approved_by',
                                    on_delete=models.SET_NULL)

    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='批准日期')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def __str__(self):
        # print(self.get_asset_type_display())  格式get_xxx字段_display()  获取choices对应的值  http://www.john-player.com/django/how-to-register-a-model-with-django-admin/
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:   # 元数据类，每个元数据类也只对自己所在模型起作用。
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"  # 复数名
        ordering = ['-c_time']    # 排序  -表示降序排列

class Server(models.Model):
    """服务器设备"""

    sub_asset_type_choice = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )

    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)  # 非常关键的一对一关联！asset被删除的时候一并删除server
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="服务器类型")
    created_by = models.CharField(choices=created_by_choice, max_length=32, default='auto', verbose_name="添加方式")
    hosted_on = models.ForeignKey('self', related_name='hosted_on_server',
                                  blank=True, null=True, verbose_name="宿主机", on_delete=models.CASCADE)  # 虚拟机专用字段
    model = models.CharField(max_length=128, null=True, blank=True, verbose_name='服务器型号')
    raid_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='Raid类型')

    os_type = models.CharField('操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField('发行商', max_length=64, blank=True, null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

class SecurityDevice(models.Model):
    """安全设备"""

    sub_asset_type_choice = (
        (0, '防火墙'),
        (1, '入侵检测设备'),
        (2, '互联网网关'),
        (4, '运维审计系统'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="安全设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='安全设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '安全设备'
        verbose_name_plural = "安全设备"


class StorageDevice(models.Model):
    """存储设备"""

    sub_asset_type_choice = (
        (0, '磁盘阵列'),
        (1, '网络存储器'),
        (2, '磁带库'),
        (4, '磁带机'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="存储设备类型")
    model = models.CharField(max_length=128, default='未知型号', verbose_name='存储设备型号')

    def __str__(self):
        return self.asset.name + "--" + self.get_sub_asset_type_display() + str(self.model) + " id:%s" % self.id

    class Meta:
        verbose_name = '存储设备'
        verbose_name_plural = "存储设备"


class NetworkDevice(models.Model):
    """网络设备"""

    sub_asset_type_choice = (
        (0, '路由器'),
        (1, '交换机'),
        (2, '负载均衡'),
        (4, 'VPN设备'),
    )

    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="网络设备类型")

    vlan_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="VLanIP")
    intranet_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="内网IP")

    model = models.CharField(max_length=128, default='未知型号',  verbose_name="网络设备型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="设备固件版本")
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name="端口个数")
    device_detail = models.TextField(null=True, blank=True, verbose_name="详细配置")

    def __str__(self):
        return '%s--%s--%s <sn:%s>' % (self.asset.name, self.get_sub_asset_type_display(), self.model, self.asset.sn)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Software(models.Model):
    """
    只保存付费购买的软件
    """
    sub_asset_type_choice = (
        (0, '操作系统'),
        (1, '办公\开发软件'),
        (2, '业务软件'),
    )

    sub_asset_type = models.SmallIntegerField(choices=sub_asset_type_choice, default=0, verbose_name="软件类型")
    license_num = models.IntegerField(default=1, verbose_name="授权数量")
    version = models.CharField(max_length=64, unique=True, help_text='例如: RedHat release 7 (Final)',
                               verbose_name='软件/系统版本')

    def __str__(self):
        return '%s--%s' % (self.get_sub_asset_type_display(), self.version)

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"        

class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True, verbose_name="机房名称")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class Manufacturer(models.Model):
    """厂商"""

    name = models.CharField('厂商名称', max_length=64, unique=True)
    telephone = models.CharField('支持电话', max_length=30, blank=True, null=True)
    memo = models.CharField('备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"


class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level', on_delete=models.SET_NULL)   # 业务线可以有子业务线，因此使用一个外键关联自身模型；
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class Contract(models.Model):
    """合同"""

    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    memo = models.TextField('备注', blank=True, null=True)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详细', blank=True, null=True)
    start_day = models.DateField('开始日期', blank=True, null=True)
    end_day = models.DateField('失效日期', blank=True, null=True)
    license_num = models.IntegerField('license数量', blank=True, null=True)
    c_day = models.DateField('创建日期', auto_now_add=True)
    m_day = models.DateField('修改日期', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = "合同"


class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名', max_length=32, unique=True)
    c_day = models.DateField('创建日期', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = "标签"        