import multiprocessing
from threading import Thread
import threading
import time
from random import randint

print(multiprocessing.cpu_count())

def add_numbers(a, b,thread):
    print(f"Started: {thread}")
    print(threading.active_count())
    time.sleep(1)
    print(f"Sum: {a+b}")

    print("End")

p1 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),1))
p2 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),2))
p3 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),3))
p4 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),4))
p5 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),5))

p6 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),6))
p7 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),7))
p8 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),8))
p9 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),9))
p10 = Thread(target=add_numbers,args=(randint(0,10),randint(0,10),10))

p1.start()
p2.start()
p3.start()
p4.start()
p5.start()

p6.start()
p7.start()
p8.start()
p9.start()
p10.start()

p1.join()
p2.join()
p3.join()
p4.join()
p5.join()

p6.join()
p7.join()
p8.join()
p9.join()
p10.join()
