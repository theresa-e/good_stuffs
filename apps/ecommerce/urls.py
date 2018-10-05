from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    # route for the homepage!
    url(r'^$', views.index),
    # route for categories/all good stuff
    url(r'^categories', views.categories),
    # login / registration
    url(r'^login', views.login), 
    url(r'^create-acct', views.create_acct), 
    # handles form data for new user
    url(r'^process_new_user', views.process_new_user),
    # handles form data for login request
    url(r'^process_login', views.process_login),
    url(r'^logout', views.logout),
    # display account info
    url(r'^account', views.account_info), 
    
    # route to admin dashboard
    url(r'^admin/orders', views.orders),
    url(r'^admin/products', views.products),
    url(r'^admin/users', views.users),
    url(r'^admin/add-product', views.add_product),
    url(r'^admin/process-product', views.process_product),
    url(r'^admin/product/delete/(?P<id>\d+)', views.delete_product),
    url(r'^admin/product/edit/(?P<id>\d+)', views.process_edit),
    url(r'^admin/product/edit-product/(?P<id>\d+)', views.edit_product),
    url(r'^admin/user/edit-user/(?P<id>\d+)', views.edit_user),
]