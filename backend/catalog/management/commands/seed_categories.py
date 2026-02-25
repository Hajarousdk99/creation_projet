from django.core.management.base import BaseCommand

from catalog.models import Category

FEMME_SUBCATEGORIES = [
    ("Robes ", "robes"),
    ("Muscs", "muscs"),
    ("Parfums", "parfums"),
    ("Sacs", "sacs"),
]


class Command(BaseCommand):
    help = "Crée les catégories Femme / Homme et les sous-catégories Femme."

    def handle(self, *args, **options):
        femme, _ = Category.objects.get_or_create(
            slug="femme",
            defaults={"name": "Femme", "parent": None},
        )
        homme, _ = Category.objects.get_or_create(
            slug="homme",
            defaults={"name": "Homme", "parent": None},
        )

        for name, slug in FEMME_SUBCATEGORIES:
            Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "parent": femme},
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Catégories créées: Femme (avec Robes, Muscs, Parfums, Sacs), Homme."
            )
        )
