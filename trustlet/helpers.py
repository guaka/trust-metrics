
__doc__ = """Collection of random useful stuff"""


def hms(t):
    """convert time in seconds into Hour Minute Second format"""
    t = int(t)
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return str(h)+'h'+str(m)+'m'+str(s)+'s'


def get_name(obj):
    """get name of object or class"""
    if hasattr(obj, "__name__"):
        return obj.__name__
    if hasattr(obj, "__class__"):
        return get_name(obj.__class__)
    else:
        raise "Can't find name"
