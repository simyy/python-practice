from pymongo.errors import AutoReconnect

def autoreconnect_retry(fn, retries=3):
    def db_op_wrapper(*args, **kwargs):
        tries = 0

        while tries < retries:
            try:
                return fn(*args, **kwargs)

            except AutoReconnect:
                tries += 1

        raise Exception("No luck even after %d retries" % retries)
        
        
@autoreconnect_retry
def insert_foo_record(foo):
    # Perform db operation
    pass

@autoreconnect_retry(20)
def get_foo_record(id):
    # Perform db operation
    pass
