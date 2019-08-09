from django.urls import reverse
from menu import MenuItem, Menu

# Menu IF
Menu.add_item("main", MenuItem("F.A.Q",
                               reverse("base:index")))
Menu.add_item("main", MenuItem("Pomoc",
                               reverse("base:index")))
Menu.add_item("main", MenuItem("Web",
                               reverse("base:index")))
Menu.add_item("main", MenuItem("Sestava",
                               reverse("base:index")))
Menu.add_item("main", MenuItem("Pravidla stránky",
                               reverse("base:site_rules")))

# Hra online
Menu.add_item("game", MenuItem("Questy",
                               reverse("base:index")))
Menu.add_item("game", MenuItem("Hadanky",
                               reverse("base:index")))
Menu.add_item("game", MenuItem("Jeskyně",
                               reverse("base:index")))
Menu.add_item("game", MenuItem("Deadland",
                               reverse("base:index")))

# Město
Menu.add_item("city", MenuItem("Hřbitov",
                               reverse("base:index")))
Menu.add_item("city", MenuItem("Cvičistě",
                               reverse("base:index")))

# Pomoc
Menu.add_item("aid", MenuItem("Certifikace",
                              reverse("base:index")))
Menu.add_item("aid", MenuItem("Smajlíci",
                              reverse("base:index")))
