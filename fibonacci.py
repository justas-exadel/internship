# 1. One function calculates Fibonnaci number using iterative algorithm
# 2. Another function calculates Fibonnaci number using recursive algorithm
# Requirements
#

# input 0,1,2,3,4,5,...
# output 0,1,1,2,3,5,..
# Functions have to handle erros if we pass bad arguments
# A function call result has to be printed as "Function name (argument value) = function value, duration xx.xxx seconds"

from time import time


def start(funkc):  # kodel toks vardas?
    def wrapper(*args):
        start = time()
        result = funkc(*args)
        end = time()
        duration = '{:06.3f}'.format(end - start)
        print(
            f"Function name(argument value) = {result}, duration {duration} " \
            "seconds")
        exit()

    return wrapper


def fibonacci_iterative(n: int) -> int:
    ...


# @start
cache = {}


def fibonacci_recursive(n: int) -> int:
    # n - non integer
    # n - integer < 0
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        value = cache.get(n)
        if value is not None:
            return value
        else:
            value = fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
            cache[n] = value
            return value


# [1,2,3,7,0] - find max - O(n)
# [1,2,3,7,0] - sort - O(n^2)
# fibonacci O(2^n)

if __name__ == '__main__':
    # patikrini ar yra cache - jei yra uzloudini, jeigu ne pradedii nauja
    start = time()
    print(fibonacci_recursive(200))
    print(time() - start)
    print(cache)
    # issaugai cache
