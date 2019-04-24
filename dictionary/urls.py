from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('spells', views.spells, name='spells'),
    path('skills', views.skills, name='skills'),
    path('items', views.items, name='items'),
    path('races', views.races, name='races'),
    path('professions', views.professions, name='professions'),

    path('spells/add', views.spell_add, name="spell_add"),
]
