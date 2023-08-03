# std
import re


def sanitize_code(code: str) -> str:
    """ """
    return re.sub(r"[, ]", "_", code)


def memoize(cache):
    """
    Used as a decorator for caching database objects
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            if not result:
                return None
            if isinstance(result, list):
                for i in result:
                    cache[i.id] = i
            else:
                cache[result.id] = result
            return result

        return wrapper

    return decorator
