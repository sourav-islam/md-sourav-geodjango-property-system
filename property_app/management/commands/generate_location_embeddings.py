from django.core.management.base import BaseCommand
from property_app.models import Location
from property_app.embeddings import embed_location


class Command(BaseCommand):
    help = "Generate embeddings for all active locations"

    def handle(self, *args, **options):
        locations = Location.objects.filter(is_active=True)
        self.stdout.write(f"Generating embeddings for {locations.count()} locations...")
        
        for location in locations:
            location.embedding = embed_location(location)
            location.save()
            self.stdout.write(f"Generated embedding for {location.name}")
        
        self.stdout.write(self.style.SUCCESS("Successfully generated embeddings for all locations!"))
