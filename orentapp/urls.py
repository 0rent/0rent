from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from orentapp import views
from orentapp.views import *

urlpatterns = patterns('',
    # url main page
    url(r'^$', views.Index.as_view(), name='index'),
    # url product_detail
    url(r'^(?P<pk>\d+)/$', login_required(views.ProductDetailView.as_view()), name='product_detail'),
    # url product_list
    url(r'^product_list/$', login_required(views.ProductListView.as_view()), name='product_list'),
    # url product_use
    url(r'^(?P<product_id>\d+)/product_use/$', login_required(views.ProductUseView), name='product_use'),
    # url product_create
    url(r'^createproduct/$', login_required(ProductCreateView.as_view()), name='product_create'),
    # url product_update
    url(r'^(?P<pk>\d+)/updateproduct/$', login_required(ProductUpdateView.as_view()), name='product_update'),
    # url add user to group
    url(r'^(?P<pk>\d+)/addusertogroup/$', login_required(AddUserToGroupView.as_view()), name='add_user_to_group'),
)
