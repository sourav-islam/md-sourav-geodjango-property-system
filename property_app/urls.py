from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('properties/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
]
