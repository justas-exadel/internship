import json
from time import time
from functools import wraps
import sys


def save_cache(data):
    try:
        with open('cache_set.json', 'r+') as file:
            cache_data = json.load(file)
            key_list = []
        for item in cache_data:
            key_list.append(item)

        for key, value in data.items():
            for i in key_list:
                if i not in key_list:
                    cache_data.update({"i": value})
                else:
                    pass
        json.dump(cache_data, file, indent=2)
    except (FileNotFoundError, ValueError):
        with open('cache_set.json', 'w') as file:
            json.dump(data, file, indent=2, sort_keys=True)


def validate_input(n):
    if not isinstance(n, int):
        print("Value must be integer.")
        exit()
    elif n < 0:
        print("Integer must be greater than or equal to 0")
        exit()


def result(func):
    @wraps(func)
    def wrap(args):
        start_time = time()
        result = func(args)
        end_time = time()
        duration = '{:06.3f}'.format(end_time - start_time)
        print(
            f'{func.__name__}({args}) = {result}, duration {duration} seconds')
        return result

    return wrap


@result
def fibonacci_iterative(n: int) -> int:
    validate_input(n)
    list = []
    if n == 0 or n == 1:
        return n
    a, b = 0, 1
    for i in range(n):
        list.append(a)
        a, b = b, a + b
    value = list[-1] + list[-2]
    return value


cache = {}


@result
def fibonacci_recursive(n: int) -> int:
    validate_input(n)

    def fibonacci_func(n):
        if n <= 1:
            return n
        else:
            cache_value = cache.get(n)
            if cache_value is not None:
                return cache_value
            else:
                value = fibonacci_func(n - 1) + fibonacci_func(n - 2)
                cache[n] = value
                save_cache(cache)

                return value

    return fibonacci_func(n)


print("recursion maximum depth: ", sys.getrecursionlimit())

if __name__ == '__main__':
    fibonacci_iterative(35)
    fibonacci_recursive(35)
