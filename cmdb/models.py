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
    # business_unit = models.ForeignKey('BusinessUnit', null=True, blank=True, verbose_name='所属业务线',
    #                                   on_delete=models.SET_NULL)
    status = models.SmallIntegerField(
        choices=asset_status, default=0, verbose_name='设备状态')

    # manufacturer = models.ForeignKey('Manufacturer', null=True, blank=True, verbose_name='制造商',
    #                                  on_delete=models.SET_NULL)
    manage_ip = models.GenericIPAddressField(
        null=True, blank=True, verbose_name='管理IP')
    # tags = models.ManyToManyField('Tag', blank=True, verbose_name='标签')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='资产管理员', related_name='admin',
                              on_delete=models.SET_NULL)
    # idc = models.ForeignKey('IDC', null=True, blank=True,
    #                         verbose_name='所在机房', on_delete=models.SET_NULL)
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
        # print(self.get_asset_type_display())  格式get_xxx字段_display()  获取choices对应的值
        return '<%s>  %s' % (self.get_asset_type_display(), self.name)

    class Meta:   # 元数据类，每个元数据类也只对自己所在模型起作用。
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"  # 复数名
        ordering = ['-c_time']    # 排序  -表示降序排列
