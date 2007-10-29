
"""Collection of random useful stuff."""

import numpy
import datetime
try:
    import scipy
except:
    print "no scipy"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?





def hms(t_sec):
    """Convert time in seconds into Hour Minute Second format.

    >>> hms(30)
    0h0m30s
    >>> hms(100000)
    27h46m40s
    """
    t_sec = int(t_sec)
    mins, secs = divmod(t_sec, 60)
    hours, mins = divmod(mins, 60)
    return str(hours)+'h'+str(mins)+'m'+str(secs)+'s'


def est_datetime_arr(seconds):
    """Estimated datetime of arrival."""
    date = datetime.datetime.now() + datetime.timedelta(seconds = seconds)
    if seconds < 86400:
        return date.strftime("%H:%M:%S")
    return date.strftime("%H:%M:%S %A %d %B")


def get_name(obj):
    """Get name of object or class.

    >>> get_name(datetime)
    datetime
    """
    if hasattr(obj, "__name__"):
        if hasattr(obj, "name"):
            return obj.name
        return obj.__name__
    if hasattr(obj, "__class__"):
        if hasattr(obj, "get_name"):
            return obj.get_name()
        return get_name(obj.__class__)
    else:
        raise "Can't find name."


mean_std = lambda x: (scipy.mean(x), scipy.std(x))


def threshold(arr):
    """Should use scaling here."""
    t_arr = arr.copy()
    for i, v in enumerate(arr):
        if v == UNDEFINED:
            pass
        elif v >= 0.9 and v < 1.0:
            t_arr[i] = 1.0
        elif v >= 0.7 and v < 0.9:
            t_arr[i] = 0.8
        elif v >= 0.5 and v < 0.7:
            t_arr[i] = 0.6
        elif v < 0.5:
            t_arr[i] = 0.4
    return t_arr

def thresholdPR(arr):
    """Should use scaling here."""
    arr = recur_log_rescale(arr)
    t_arr = arr.copy()
    for i, v in enumerate(arr):
        if v == UNDEFINED:
            pass
        elif v > 0.8 and v < 1.0:
            t_arr[i] = 1.0
        elif v > 0.6 and v < 0.8:
            t_arr[i] = 0.8
        elif v > 0.4 and v < 0.6:
            t_arr[i] = 0.6
        elif v < 0.4:
            t_arr[i] = 0.4
    return t_arr


def rescale_array(orig_array, scale = (0, 1)):
    """Linearly rescale an array.

    >>> rescale_array(numpy.arange(3.))
    rescaling: (0.0, 2.0) to (0, 1)
    array([ 0. ,  0.5,  1. ])              
    """
    min_val, max_val = min(orig_array), max(orig_array)
    print "rescaling:", (min_val, max_val), "to", scale
    mult = (scale[1] - scale[0]) / (max_val - min_val)
    return scale[0] + (orig_array - min_val) * mult


def recf(func, num):
    """Recursivity.
    
    >>> recf(lambda x: x+1, 3)(10)
    13
    """
    if num == 1:
        return lambda x: func(x)
    else:
        return lambda x: func(recf(func, num - 1)(x))

def recur_log_rescale(arr):
    """Recursive log rescaling."""
    arr = rescale_array(arr)
    count = 0
    while scipy.mean(arr) <= 0.5 and count < 20:
        arr = numpy.log2(arr + 1)
        count += 1
    arr = rescale_array(arr, (0.4, 1.0))
    return arr
        

def indication_of_dist(arr, stepsize = 0.2):
    """Some kind of histogram-type info."""
    for start in numpy.arange(min(arr), max(arr), step = stepsize):
        print start, sum((arr >= start) * (arr < start + stepsize))

    
            
