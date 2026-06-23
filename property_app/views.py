from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from pgvector.django import CosineDistance
from .models import Property, Location
from .embeddings import embed_text


class HomepageView(TemplateView):
    template_name = 'property_app/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_properties'] = Property.objects.filter(is_featured=True, is_active=True)[:6]
        return context


class PropertyListView(ListView):
    model = Property
    template_name = 'property_app/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        
        location_query = self.request.GET.get('location', '').strip()
        property_type = self.request.GET.get('property_type', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        bedrooms = self.request.GET.get('bedrooms', '')
        radius_km = int(self.request.GET.get('radius_km', 50))
        
        if location_query:
            # Step 1: Try exact name match
            location = Location.objects.filter(name__iexact=location_query, is_active=True).first()
            
            # Step 2: If no exact match, try semantic search on Location embeddings
            if not location:
                try:
                    query_embedding = embed_text(location_query)
                    location = Location.objects.filter(
                        embedding__isnull=False,
                        is_active=True
                    ).annotate(
                        similarity=CosineDistance('embedding', query_embedding)
                    ).order_by('similarity').first()
                except Exception as e:
                    print(f"Error in semantic location search: {e}")
                    location = None
            
            # Step 3: Apply geo filter if location found with point
            if location and location.point:
                queryset = queryset.filter(
                    point__distance_lte=(location.point, D(km=radius_km))
                ).annotate(
                    distance=Distance('point', location.point)
                ).order_by('distance')
                self.found_location = location
            else:
                # Step 4: Fallback — semantic search directly on property embeddings
                try:
                    query_embedding = embed_text(location_query)
                    queryset = queryset.filter(
                        embedding__isnull=False
                    ).annotate(
                        similarity=CosineDistance('embedding', query_embedding)
                    ).order_by('similarity')
                    self.found_location = None
                except Exception as e:
                    print(f"Error in semantic property search: {e}")
                    self.found_location = None
        else:
            self.found_location = None
        
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_types'] = Property.PROPERTY_TYPE_CHOICES
        context['location'] = self.request.GET.get('location', '')
        context['property_type'] = self.request.GET.get('property_type', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['bedrooms'] = self.request.GET.get('bedrooms', '')
        context['radius_km'] = self.request.GET.get('radius_km', '50')
        context['found_location'] = getattr(self, 'found_location', None)
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property_app/property_detail.html'
    context_object_name = 'property'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = self.get_object()
        
        primary_image = property.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = property.images.first()
        context['primary_image'] = primary_image
        context['property_images'] = property.images.order_by('sort_order')
        
        if property.point and property.location.point:
            distance_meters = property.point.distance(property.location.point)
            distance_km = round(distance_meters / 1000, 1)
            context['distance_from_center'] = distance_km
        else:
            context['distance_from_center'] = None
        
        return context
