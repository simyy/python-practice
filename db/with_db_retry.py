from functools import wraps

conn = MySQLdb.connect(...)
cur = conn.cursor

class with_db_retry(object):
    """Decorator for view functions to make it reconnect automatically."""
    def __init__(self, retries=2):
        self._retries = retries

    def __call__(self, func):
        @wraps(func)
        def func_with_db_reconnect(*args, **kwargs):
            retries = self._retries
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    conn = MySQLdb.connect(...)
                    cur = conn.cursor
                    retries -= 1
                    if retries == 0:
                        raise
        return func_with_db_reconnect
