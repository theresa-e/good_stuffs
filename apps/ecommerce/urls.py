from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    # Route for the homepage
    url(r'^$', views.index),

    # route for categories/all good stuff
    url(r'^categories', views.categories),

    # Login / registration
    url(r'^login', views.login), 
    url(r'^create-acct', views.create_acct), 

    # Handle form data for new user
    url(r'^process_new_user', views.process_new_user),

    # Handle form data for login request
    url(r'^process_login', views.process_login),
    url(r'^logout', views.logout),

    # Edit account info view
    url(r'^account/(?P<id>\d+)/edit', views.edit_acct_info), 
    url(r'^account/(?P<id>\d+)/process', views.process_edit_acct), 

    # Display user's account info
    url(r'^account/(?P<id>\d+)', views.account_info),

    # Cart and checkout routes
    url(r'^add_to_cart', views.add_to_cart), 
    url(r'^visit_cart', views.visit_cart), 
    url(r'^remove_item/(?P<name>\d+)', views.remove_item_cart), 
    url(r'^process_charge', views.charge), 
    url(r'^checkout', views.checkout), 
    url(r'^create_address', views.create_address), 

    # View all orders, products, and users. *Admin access only*
    url(r'^admin/orders', views.orders),
    url(r'^admin/products', views.products),
    url(r'^admin/users', views.users),

    # CRUD functionality for products
    url(r'^admin/add-product', views.add_product),
    url(r'^admin/process-product', views.process_product),
    url(r'^admin/product/delete/(?P<id>\d+)', views.delete_product),
    url(r'^admin/product/edit/(?P<id>\d+)', views.process_edit),
    url(r'^admin/product/edit-product/(?P<id>\d+)', views.edit_product),

    # Edit user info (including changing user_type to admin)
    url(r'^admin/user/edit-user/(?P<id>\d+)', views.edit_user),
]