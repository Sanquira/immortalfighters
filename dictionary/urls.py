from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('spells/', views.spells, name='spells'),  # Spells list
    path('spells_table/', views.spells_table, name='spells_table'),  # Spells list data table
    path('spells/delete/999/', views.spell_delete, name="spell_delete"),  # Dummy delete
    path('spells/delete/<int:pk>/', views.spell_delete, name="spell_delete"),  # Delete spell
    path('spells/item/', views.spell_edit, name='spell_edit'),  # Add spell
    path('spells/item/999/', views.spell_item_view, name='spell_item'),  # Dummy view
    path('spells/item/<int:pk>/', views.spell_item_view, name='spell_item'),  # View spell
    path('spells/item/999/edit/', views.spell_edit, name='spell_edit'),  # Dummy edit
    path('spells/item/<int:pk>/edit/', views.spell_edit, name='spell_edit'),  # Edit spell
    
    path('skills/', views.skills, name='skills'),  # Skills list
    path('skills_table/', views.skills_table, name='skills_table'),  # Skills list data table
    path('skills/delete/999/', views.skill_delete, name="skill_delete"),  # Dummy delete
    path('skills/delete/<int:pk>/', views.skill_delete, name="skill_delete"),  # Delete skill
    path('skills/skill/', views.skill_edit, name='skill_edit'),  # Add skill
    path('skills/skill/999/', views.skill_item_view, name='skill_item'),  # Dummy view
    path('skills/skill/<int:pk>/', views.skill_item_view, name='skill_item'),  # View skill
    path('skills/skill/999/edit/', views.skill_edit, name='skill_edit'),  # Dummy edit
    path('skills/skill/<int:pk>/edit/', views.skill_edit, name='skill_edit'),  # Edit skill
    
    path('items/', views.items, name='items'),
    path('items/delete/<int:pk>/', views.item_delete, name="item_delete"),
    path('items/item/', views.item_item, name='item_item'),
    path('items/item/<int:pk>/', views.item_item, name='item_item'),
    
    path('mobs/', views.mobs, name='mobs'),

]
