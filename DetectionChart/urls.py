from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^detvalue$', views.detvalue , name='detvalue'),
    path('downloadToExcel', views.downloadToExcel, name='downloadToExcel'),
    path('backupDatabase', views.backupDatabase, name='backupDatabase'),
    path('resetDatabase', views.resetDatabase, name='resetDatabase'),
    path('updateDatabase', views.updateDatabase, name='updateDatabase'),
    path('downloadOSXAtomicTests', views.downloadOSXAtomicTests, name='downloadOSXAtomicTests'),
    path('downloadLinuxAtomicTests', views.downloadLinuxAtomicTests, name='downloadLinuxAtomicTests'),
]