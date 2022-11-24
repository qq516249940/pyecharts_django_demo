from django.urls import path 

from . import views

app_name = "cmdb"    #  前端页面访问{% url 'cmdb:dashboard' %}用到这里的cmdb

urlpatterns = [
    path(r'report/', views.report, name='report'),  # <---
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('detail/<int:asset_id>/', views.detail, name="detail"),
    path('', views.dashboard), 
]