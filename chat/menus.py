"""
Menu entries for the chat application
"""
from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("city", MenuItem("Hospoda",
                               reverse("chat:list_rooms"),
                               check=lambda request: request.user.is_authenticated))
