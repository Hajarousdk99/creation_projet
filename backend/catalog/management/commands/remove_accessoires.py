from django.core.management.base import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    help = "Supprime la catégorie Accessoires (et ses sous-catégories / produits liés)."

    def handle(self, *args, **options):
        deleted = Category.objects.filter(slug="accessoires").delete()
        count = deleted[0] if isinstance(deleted, tuple) else 0
        self.stdout.write(self.style.SUCCESS(f"Catégorie Accessoires supprimée ({count} objet(s))."))
