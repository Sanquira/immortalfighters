from django.urls import path

from base import views

urlpatterns = [
    path('', views.index, name='index'),
    path('banners', views.banners, name='banners'),
    path('registration', views.registration, name='registration'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('site_rules', views.site_rules, name='site_rules'),
]
