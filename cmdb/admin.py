from django.contrib import admin

from cmdb.models import Asset
 
# Register your models here.
### 注册模型
# 注册Asset数据库模型到 admin管理页面查看
admin.site.register(Asset)