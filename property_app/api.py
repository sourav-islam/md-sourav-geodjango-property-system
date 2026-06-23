from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from pgvector.django import CosineDistance
from property_app.models import Location
from property_app.embeddings import embed_text


class LocationAutocompleteView(APIView):
    """
    GET /api/locations/autocomplete/?q=<query>
    
    1. Embed the query using embed_text(q)
    2. Search Location by vector similarity (CosineDistance on embedding)
       ALSO do icontains fallback on name
    3. Combine results: semantic matches first (deduplicated), then name matches
    4. Return top 8 results as JSON
    5. Handle empty query: return most popular locations by property count
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query:
            # Return most popular locations by property count
            locations = Location.objects.filter(is_active=True).annotate(
                property_count=Count('properties')
            ).order_by('-property_count')[:8]
            
            return Response([{
                'id': loc.id,
                'name': loc.name,
                'slug': loc.slug,
                'property_count': loc.property_count,
                'similarity': None
            } for loc in locations])
        
        # Generate query embedding
        query_embedding = embed_text(query)
        
        # Get semantic matches
        semantic_locations = Location.objects.filter(
            is_active=True,
            embedding__isnull=False
        ).annotate(
            similarity=CosineDistance('embedding', query_embedding)
        ).order_by('similarity')[:15]
        
        # Get name matches
        name_locations = Location.objects.filter(
            is_active=True,
            name__icontains=query
        ).annotate(
            property_count=Count('properties')
        ).order_by('-property_count')[:15]
        
        # Combine and deduplicate
        seen_ids = set()
        results = []
        
        # Add semantic matches first
        for loc in semantic_locations:
            if loc.id not in seen_ids:
                seen_ids.add(loc.id)
                results.append({
                    'id': loc.id,
                    'name': loc.name,
                    'slug': loc.slug,
                    'property_count': loc.properties.count(),
                    'similarity': 1 - loc.similarity
                })
        
        # Add name matches
        for loc in name_locations:
            if loc.id not in seen_ids and len(results) < 8:
                seen_ids.add(loc.id)
                results.append({
                    'id': loc.id,
                    'name': loc.name,
                    'slug': loc.slug,
                    'property_count': loc.property_count,
                    'similarity': None
                })
        
        # Return top 8 results
        return Response(results[:8])
