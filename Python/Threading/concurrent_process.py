import threading
import time
from concurrent.futures import ProcessPoolExecutor
from random import randint

def add_numbers(a, b):
    print("Started")
    print(threading.active_count())
    time.sleep(1)
    print(f"Sum: {a+b}")

    print("End")

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=5) as pool:
        [pool.map(add_numbers(randint(0,10),randint(0,10)))
         for i in range(5)]
