from functools import wraps

from django.core.cache import cache
from django.http import JsonResponse


def rate_limit(max_requests=10, window=60):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            ip = request.META.get("REMOTE_ADDR")
            key = f"rate_limit:{view.__name__}:{ip}"

            if cache.add(key, 1, timeout=window):
                return view(request, *args, **kwargs)

            requests = cache.incr(key)

            if requests > max_requests:
                return JsonResponse(
                    {"detail": "Too many requests."},
                    status=429,
                )

            return view(request, *args, **kwargs)

        return wrapper

    return decorator
