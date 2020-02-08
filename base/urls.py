"""Url module for base."""
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path

from base.views import base
from base.views import user

urlpatterns = [
    path('', base.index, name='index'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('accounts/password_change/done/', base.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_change/', PasswordChangeView.as_view(success_url='done'), name='password_change'),

    path('accounts/registration/', base.registration, name='registration'),

    path('site_rules/', base.site_rules, name='site_rules'),
    path('statistics/', base.statistics, name='statistics'),

    path('user/color/', user.change_user_color, name='change_color'),
    path('user/sounds/', user.change_sound_setting, name='chat_sound')
]
