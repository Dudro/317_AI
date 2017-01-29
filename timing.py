from functools import reduce
from time import clock

start_t = 0
line = "="*40

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def start_timer():
    """
    Call this to start the timer.
    This is process execution time, not wall time.
    """
    start_t = clock()
                
def end_timer():
    """
    Call this to end the timer and print the
    execution time to stdout.
    """
    print("time=" + str(clock()-start_t), flush=True)

def now():
    return secondsToStr(clock())

