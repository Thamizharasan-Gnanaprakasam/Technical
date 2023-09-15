from datetime import datetime
from timeit import timeit
from functools import wraps
import time
def measure(func):
    @wraps(func) #Optional
    def wrapper(*args,**kwargs):
        start_time = time.perf_counter()
        result = func(*args,**kwargs)
        end_time = time.perf_counter()
        print(f"Function: {func.__name__}{args}{kwargs} took {end_time-start_time}")
        return result

    return wrapper

