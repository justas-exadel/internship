import json
from time import time
from functools import wraps
import sys

cache_set = {}


def save_cache(data=cache_set):
    try:
       with open('cache_set.json', 'r+') as file:
           cache_data = json.load(file)
           # print(str(cache_data))
           key_hist = []
           for item in cache_data.keys():
              key_hist.append(item)
           print(key_hist)
           for k, v in data.items():
               if k not in key_hist:
                cache_data.update({k: v})
               else:
                   pass
           # print(str(cache_data))
           file.seek(0)
           print("ss")
           json.dump(cache_data, file, indent=2)
    except Exception:
        with open('cache_set.json', 'w') as file:
            json.dump(data, file, indent=2, sort_keys=True)

def open_cache():
    ...

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
    finally:
        save_cache()

print("recursion maximum depth: ", sys.getrecursionlimit())


if __name__ == '__main__':
    # fibonacci_iterative(35)
    fibonacci_recursive(7)

