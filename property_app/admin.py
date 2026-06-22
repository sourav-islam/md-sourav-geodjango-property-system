from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Location, Property, PropertyImage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'property_type', 'status', 'price', 'bedrooms', 'bathrooms', 'is_featured', 'is_active']
    list_filter = ['status', 'property_type', 'is_featured', 'location']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'is_primary', 'sort_order', 'image_preview']
    list_filter = ['is_primary']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')
        return "-"
    image_preview.short_description = 'Preview'
