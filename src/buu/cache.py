import json
import time

cache = {}
try:
    with open('cache.json') as f:
        cache = json.load(f)
except Exception:
    pass

def get_cache(id, update=None, exp = 60 * 10):
    global cache
    if not cache.get(id, None):
        cache[id] = {
            'time': time.time(),
            'data': []
        }
        if update:
            update_cache(id, update())
    else:
        if time.time() - cache[id]['time'] > exp:
            if not update:
                return []
            else:
                update_cache(id, update())
    return cache[id]['data']

def update_cache(id, data):
    global cache
    cache[id]= {
            'time': time.time(),
            'data': data
        }
    with open('cache.json', 'w') as f:
        json.dump(cache, f)