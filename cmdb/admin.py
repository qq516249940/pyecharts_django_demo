from django.contrib import admin

# Register your models here.
from cmdb import models
from cmdb import asset_handler

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

    actions = ['approve_selected_new_assets']
    def approve_selected_new_assets(self, request, queryset):
        # 获得被打钩的checkbox对应的资产
        selected = request.POST.getlist('_selected_action')   #注意：django3.0后，ACTION_CHECKBOX_NAME的位置发生了改变。所以需要改成admin.helpers.ACTION_CHECKBOX_NAME或者'_selected_action'。
        success_upline_number = 0
        for asset_id in selected:
            obj = asset_handler.ApproveAsset(request, asset_id)
            ret = obj.asset_upline()
            if ret:
                success_upline_number += 1
        # 顶部绿色提示信息
        self.message_user(request, "成功批准  %s  条新资产上线！" % success_upline_number)
    approve_selected_new_assets.short_description = "批准选择的新资产"   

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