from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^orentapp/', include('orentapp.urls')), # url application Orent
    url(r'^admin/', include(admin.site.urls)), # url administration projet Orent
    url(r"^accounts/", include("account.urls")), # url django user account
)
