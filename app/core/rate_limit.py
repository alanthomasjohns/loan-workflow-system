from functools import wraps

from fastapi import HTTPException, Request

from app.core.redis import redis_client


def rate_limit(max_requests: int, window_seconds: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                raise ValueError(
                    "Request parameter required for rate limiting"
                )

            ip = request.client.host
            key = f"rate_limit:{ip}"
            current = redis_client.get(key)

            if current is None:
                redis_client.setex(
                    key,
                    window_seconds,
                    1
                )
            else:
                current = int(current)
                if current >= max_requests:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests"
                    )

                redis_client.incr(key)

            return func(*args, **kwargs)
        return wrapper
    return decorator