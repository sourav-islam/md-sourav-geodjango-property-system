from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('api/locations/autocomplete/', api.LocationAutocompleteView.as_view(), name='location_autocomplete'),
]
