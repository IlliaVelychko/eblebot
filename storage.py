import json
import os
from functools import wraps

STATS_FILE = "stats_backup.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_stats_decorator(stats_obj):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            result = await func(update, context, *args, **kwargs)
            # Save stats after modification
            with open(STATS_FILE, 'w') as f:
                json.dump(stats_obj, f)
            return result
        return wrapper
    return decorator