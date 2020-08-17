from time import time
from functools import wraps
import sys

cache_set = {}


def result(result_value, function_name, time_start, iteration_number):
    duration = '{:06.3f}'.format(time() - time_start)
    print(f"{function_name}({iteration_number}) = {result_value}, duration " \
          f"{duration} seconds")


def check_errors(n):
    if type(n) != int:
        print("Value must be integer.")
    elif n < 1:
        print("Integer must be greater than 0")


def fibonacci_iterative(n: int) -> int:
    try:
        time_start = time()
        check_errors(n)
        list = []
        a, b = 0, 1
        for i in range(n):
            list.append(a)
            a, b = b, a + b
        value = list[-1] + list[-2]
        return result(value, fibonacci_iterative.__name__, time_start, n)
    except Exception:
        pass


def memorize_cache(function):
    @wraps(function)
    def wrapper(args):
        if args in cache_set:
            return cache_set[args]
        else:
            rv = function(args)
            cache_set[args] = rv
            return rv

    return wrapper


def fibonacci_recursive(n: int) -> int:
    try:
        time_start = time()
        check_errors(n)
        iteration_number = n

        @memorize_cache
        def fibonacci_func(n):
            if n <= 1:
                return n
            else:
                value = fibonacci_func(n - 1) + fibonacci_func(n - 2)
                return value

        return result(fibonacci_func(n), fibonacci_recursive.__name__,
                      time_start, iteration_number)
    except Exception:
        pass


print("recursion maximum depth: ", sys.getrecursionlimit())


if __name__ == '__main__':
    fibonacci_iterative(35)
    fibonacci_recursive(35)

