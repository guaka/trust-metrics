
__doc__ = """Collection of random useful stuff"""

import numpy
try:
    import scipy
except:
    print "no scipy"


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
        if hasattr(obj, "get_name"):
            return obj.get_name()
        return get_name(obj.__class__)
    else:
        raise "Can't find name"


mean_std = lambda x: (scipy.mean(x), scipy.std(x))

def rescale_array(pt, scale = (0, 1)):
    min_pt, max_pt = min(pt), max(pt)
    print "rescaling:", (min_pt, max_pt), "to", scale
    mult =  (scale[1] - scale[0]) / (max_pt - min_pt)
    pt_scaled = scale[0] + (pt - min_pt) * mult
    return pt_scaled


def recf(f, n):
    """Recursive f."""
    if n == 1:
        return lambda x: f(x)
    else:
        return lambda x: f(recf(f, n-1)(x))

def recur_log_rescale(a):
    arr = rescale_array(a)
    count = 0
    while scipy.mean(arr) <= 0.5 and count < 20:
        arr = numpy.log2(arr + 1)
        count += 1
    return arr
        
def indication_of_dist(a, stepsize = 0.2):
    for start in numpy.arange(min(a), max(a), step = stepsize):
        print start, sum((a >= start) * (a < start + stepsize))

    
            
