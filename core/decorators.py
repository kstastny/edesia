from django.core.cache import cache

def cache_func(timeout = 30):
    """
    Function returns decorator that will get function, and cache it's results.
    """
    def _decorator(func):
        def try_cache(*args, **kwargs):
            cache_key = '%s|%s|%s|%s' % (func.__module__, func.__name__, hash(tuple(args)), hash(tuple(kwargs.items())))  
            #print cache_key
            obj = cache.get(cache_key)
            if obj is not None:
                #print 'cache hit'
                return obj
            obj = func(*args, **kwargs)
            cache.set(cache_key, obj, timeout)
            return obj
        return try_cache
    return _decorator
