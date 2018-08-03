from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'^processreg$',views.processreg),
    url(r'^success$',views.success),
    url(r'^logout$', views.logout),
    url(r'^processlog$', views.processlog),
    url(r'^home$', views.home),
    url(r'^add$',views.add),
    url(r'^add_travel_plan$', views.add_travel_plan),
    url(r'^destination/(?P<trip_id>\d+)$',views.destination),
    url(r'^join$',views.join)

]                           