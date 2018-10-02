from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),   # route for the homepage!
    url(r'^categories', views.categories), # route for categories/all good stuff
    url(r'^login', views.login), # login / registration
    url(r'^create-acct', views.create_acct) # login / registration

]                            
