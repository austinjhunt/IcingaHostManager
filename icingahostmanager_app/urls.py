app_name = "icingahostmanager_app"

from django.conf.urls import url
from django.urls import path
from . import views
from django.http import HttpResponseRedirect
urlpatterns = [
    url(r'^$', views.index),
    url(r'^addsinglehost/',views.addsinglehost),
    url(r'^bulkuploadhosts/',views.bulkuploadhosts),
    url(r'^edit_host/',views.edit_host),
    url(r'^submit_successful_hosts/', views.submit_successful_hosts),
    url(r'^logout/$',views.ihm_logout),
]
