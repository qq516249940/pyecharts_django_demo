from django.contrib import admin

from cmdb.models import (Asset,Server,
                        SecurityDevice,StorageDevice,NetworkDevice,Software,
                        CPU,
                        IDC,
                        Manufacturer,
                        BusinessUnit,
                        Contract,
                        Tag,
                        RAM,
                        Disk,
                        NIC,
                        NewAssetApprovalZone,
                        EventLog

)
# Register your models here.
class NewAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]

### 注册模型
# 注册Asset数据库模型到 admin管理页面查看  ，这个叫方法，还有一个叫装饰器@admin.register(Asset)
# admin.site.register(Asset,AssetAdmin)
admin.site.register(Server)
admin.site.register(SecurityDevice)
admin.site.register(StorageDevice)
admin.site.register(NetworkDevice)
admin.site.register(Software)
admin.site.register(CPU)
admin.site.register([IDC,Manufacturer,BusinessUnit,Contract,Tag])
admin.site.register(RAM)
admin.site.register(Disk)
admin.site.register(NIC)
admin.site.register(NewAssetApprovalZone,NewAssetAdmin)
admin.site.register(EventLog)