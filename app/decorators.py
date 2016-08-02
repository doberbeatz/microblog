from threading import Thread


def async(f):
    """ Wrapper for Async Methods
        Create thread and invoke given func in this thread
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
