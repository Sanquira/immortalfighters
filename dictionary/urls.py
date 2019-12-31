"""Url module for dictionary."""
from django.urls import path

from dictionary.views.beast_view import BeastView
from dictionary.views.skill_view import SkillView
from dictionary.views.spell_view import SpellView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns.extend(BeastView().generate_path())
urlpatterns.extend(SkillView().generate_path())
urlpatterns.extend(SpellView().generate_path())
