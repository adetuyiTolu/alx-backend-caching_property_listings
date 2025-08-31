from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get cached queryset
    all_properties = cache.get("all_properties")
    if all_properties is None:
        # Fetch from database if not cached
        all_properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Store in Redis for 1 hour (3600 seconds)
        cache.set("all_properties", all_properties, 3600)
    return all_properties
