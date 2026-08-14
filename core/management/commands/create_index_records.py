from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Pokemon

from ...algolia.client import Algolia


class Command(BaseCommand):
    help = "Add records to the Algolia index."

    def handle(self, *args, **options):
        algolia = Algolia(settings.APPLICATION_ID, settings.WRITE_API_KEY)

        pokemon_list = Pokemon.objects.all()
        for pokemon in pokemon_list:
            algolia.save(
                {
                    "objectID": pokemon.id,
                    "name": pokemon.name,
                    "slug": pokemon.slug,
                    "sprite": f"http://localhost:8000/media/{pokemon.sprite}",
                }
            )
        self.stdout.write(self.style.SUCCESS("All records were saved in the index."))
