from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    # route for the homepage!
    url(r'^$', views.index),
    # route for categories/all good stuff
    url(r'^categories', views.categories),
    # login / registration
    url(r'^login', views.login), 
    # login / registration
    url(r'^create-acct', views.create_acct), 
    # handles form data for new user
    url(r'^process_new_user', views.process_new_user),
    # handles form data for login request
    url(r'^process_login', views.process_login)

]                            
