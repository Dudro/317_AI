from functools import reduce
from time import clock

start_t = {}


def seconds_to_str(t):
    """
    Formats the given time as a string.

    :param t: the time in seconds
    :rtype: string
    """
    return "%d:%02d:%02d.%03d" % \
           reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                  [(t * 1000,), 1000, 60, 60])


def start_timer(i=0):
    """
    Starts timer 'i'. This is process execution time, not wall time.

    :param i: a timer number
    :type i: int
    """
    start_t[i] = clock()


def end_timer(i=0):
    """
    Ends timer 'i' (assuming it was previously started), and returns the
    elapsed execution time (not the wall time).

    :param i: a timer number
    :type i: int
    :rtype: float
    """
    return clock() - start_t[i]


def now():
    """
    Returns the current time formatted as a string.
    """
    return seconds_to_str(clock())
