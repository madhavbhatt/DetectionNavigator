from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^detvalue$', views.detvalue , name='detvalue'),
    path('downloadToExcel', views.downloadToExcel, name='downloadToExcel'),
    path('resetDatabase', views.resetDatabase, name='resetDatabase'),
    path('updateDatabase', views.updateDatabase, name='updateDatabase'),
    path('logoutView',views.logoutView,name="logoutView"),
]