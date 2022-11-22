from django.urls import path 

from . import views

urlpatterns = [
    path(r'report/', views.report, name='report'),
]