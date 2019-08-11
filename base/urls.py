from django.urls import path

from base import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('accounts/log_in/', views.log_in, name='log_in'),
    path('accounts/log_out/', views.log_out, name='log_out'),
    path('login_required/', views.login_required, name='login_required'),
    path('site_rules/', views.site_rules, name='site_rules'),
    path('statistics/', views.statistics, name='statistics'),
]
