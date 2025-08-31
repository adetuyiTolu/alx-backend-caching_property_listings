from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    # Get the underlying Redis client
    redis_client = cache.client.get_client(write=True)

    info = redis_client.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 4)
    }

    logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={metrics['hit_ratio']}")
    return metrics

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
