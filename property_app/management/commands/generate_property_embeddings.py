from django.core.management.base import BaseCommand
from property_app.models import Property
from property_app.embeddings import embed_property


class Command(BaseCommand):
    help = "Generate embeddings for all active properties"

    def handle(self, *args, **options):
        properties = Property.objects.filter(is_active=True)
        self.stdout.write(f"Generating embeddings for {properties.count()} properties...")
        
        for property_obj in properties:
            property_obj.embedding = embed_property(property_obj)
            property_obj.save()
            self.stdout.write(f"Generated embedding for {property_obj.title}")
        
        self.stdout.write(self.style.SUCCESS("Successfully generated embeddings for all properties!"))
