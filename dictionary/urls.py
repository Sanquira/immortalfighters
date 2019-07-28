from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('skills', views.skills, name='skills'),

    path('races', views.races, name='races'),
    path('professions', views.professions, name='professions'),

    path('spells', views.spells, name='spells'),  # Spells list
    path('spells_table', views.spells_table, name='spells_table'),  # Spells list data table
    path('spells/delete/999', views.spell_delete, name="spell_delete"),  # Dummy delete
    path('spells/delete/<int:pk>', views.spell_delete, name="spell_delete"),  # Delete spell
    path('spells/item', views.spell_item, name='spell_item'),  # Add spell
    path('spells/item/<int:pk>', views.spell_item, name='spell_item'),  # View spell
    path('spells/item/999/edit', views.spell_edit, name='spell_edit'),  # Dummy edit
    path('spells/item/<int:pk>/edit', views.spell_edit, name='spell_edit'),  # Edit spell

    path('items', views.items, name='items'),
    path('items/delete/<int:pk>', views.item_delete, name="item_delete"),
    path('items/item', views.item_item, name='item_item'),
    path('items/item/<int:pk>', views.item_item, name='item_item'),

    path('skills', views.skills, name='skills'),
    path('skills/delete/<int:pk>', views.skill_delete, name="skill_delete"),
    path('skills/skill', views.skill_item, name='skill_item'),
    path('skills/skill/<int:pk>', views.skill_item, name='skill_item'),
]
