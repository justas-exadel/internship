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


def load_cache():
    try:
        with open('cache_set.json', 'r') as file:
            cache = json.load(file)
    except FileNotFoundError:
        pass


def validate_input(n):
    if not isinstance(n, int):
        print(f"Value '{n}' must be integer.")
        exit()
    elif n < 0:
        print(f"Integer {n} must be greater than or equal to 0")
        exit()


def timer(func):
    @wraps(func)
    def wrap(*args):
        start_time = time()
        result = func(*args)
        end_time = time()
        duration = '{:06.3f}'.format(end_time - start_time)
        print(
            f'{func.__name__}({args[0]}) = {result}, duration {duration} seconds')
        return result

    return wrap


def fibonacci_iter(*args):
    for arg in args:
        fibonacci_iterative(arg)


@timer
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


def fibonacci_rec(*args):
    for arg in args:
        fibonacci_recursive(arg)


@timer
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

                return value

    return fibonacci_func(n)


print("recursion maximum depth: ", sys.getrecursionlimit())

if __name__ == '__main__':
    cache = {}
    load_cache()
    fibonacci_iter(7, 4, 6)
    fibonacci_rec(7, 4, 6)
    save_cache(cache)
