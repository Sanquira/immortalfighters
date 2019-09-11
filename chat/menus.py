from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("city", MenuItem("Hospoda",
                               reverse("chat:index"),
                               check=lambda request: request.user.is_authenticated))
