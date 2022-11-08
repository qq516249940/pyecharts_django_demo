from django.contrib import admin

from cmdb.models import Asset,Server,SecurityDevice,StorageDevice,NetworkDevice,Software
 
# Register your models here.
### 注册模型
# 注册Asset数据库模型到 admin管理页面查看  ，这个叫方法，还有一个叫装饰器@admin.register(Asset)
admin.site.register(Asset)
admin.site.register(Server)
admin.site.register(SecurityDevice)
admin.site.register(StorageDevice)
admin.site.register(NetworkDevice)
admin.site.register(Software)