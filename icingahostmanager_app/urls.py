app_name = "icingahostmanager_app"

from django.conf.urls import url
from django.urls import path
from . import views
from django.http import HttpResponseRedirect
urlpatterns = [
    url(r'^$', views.index),
    url(r'^addsinglehost/',views.addsinglehost),
    url(r'^bulkuploadhosts/',views.bulkuploadhosts),
    url(r'^logout/$',views.ihm_logout),
]
