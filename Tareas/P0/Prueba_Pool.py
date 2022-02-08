from multiprocessing import Pool, cpu_count
from math import sqrt
import psutil

psutil.cpu_count(logical = False)

def f(x):
    return sqrt(x)

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, range(1, 100)))
