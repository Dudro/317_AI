from functools import reduce
from time import clock

start_t = []

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def start_timer():
    """
    Call this to start the timer.
    This is process execution time, not wall time.
    """
    start_t.append(clock())
                
def end_timer(i):
    """
    Call this to end the timer and get the
    execution time in a String.
    """
    return clock()-start_t[i]

def now():
    return secondsToStr(clock())

