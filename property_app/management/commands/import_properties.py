import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.gis.geos import Point
from property_app.models import Location, Property


class Command(BaseCommand):
    help = 'Import properties from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        df = pd.read_csv(csv_file)

        total_imported = 0
        for index, row in df.iterrows():
            # Get or create Location
            location_name = row['location_name']
            location_slug = slugify(location_name)
            location, created = Location.objects.get_or_create(
                slug=location_slug,
                defaults={'name': location_name}
            )

            # Update location point if lat and lon are provided
            if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')):
                location.point = Point(float(row['longitude']), float(row['latitude']), srid=4326)
                location.save()

            # Create property slug
            property_slug = slugify(row['title'])
            # Ensure slug is unique
            original_slug = property_slug
            counter = 1
            while Property.objects.filter(slug=property_slug).exists():
                property_slug = f"{original_slug}-{counter}"
                counter += 1

            # Parse amenities
            amenities = []
            if pd.notna(row.get('amenities')):
                amenities = [a.strip() for a in row['amenities'].split(',')]

            # Parse is_featured
            is_featured = False
            if pd.notna(row.get('is_featured')):
                is_featured = str(row['is_featured']).lower() in ('true', '1', 'yes')

            # Create Property
            property = Property.objects.create(
                location=location,
                title=row['title'],
                slug=property_slug,
                description=row.get('description', ''),
                property_type=row['property_type'],
                status=row.get('status', 'available'),
                price=row['price'],
                bedrooms=row.get('bedrooms', 0),
                bathrooms=row.get('bathrooms', 0),
                area_sqft=row.get('area_sqft'),
                address=row.get('address', ''),
                amenities=amenities,
                is_featured=is_featured
            )

            # Update property point if lat and lon are provided
            if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')):
                property.point = Point(float(row['longitude']), float(row['latitude']), srid=4326)
                property.save()

            total_imported += 1

            if total_imported % 50 == 0:
                self.stdout.write(f"Imported {total_imported} properties so far...")

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {total_imported} properties!"))
