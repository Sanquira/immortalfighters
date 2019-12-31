"""Menu module for dictionary."""
from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("aid", MenuItem("Databáze",
                              reverse("dictionary:index"),
                              check=lambda request: request.user.is_authenticated))
