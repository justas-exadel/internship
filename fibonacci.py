import json
from time import time
import sys


def load_cache() -> dict:
    try:
        with open('cache_set.json', 'r') as file:
            cache = json.load(file)
        return cache
    except FileNotFoundError:
        print('Cache file not found. Creating new cache.')
        return {}


def save_cache(cache: dict) -> None:
    with open('cache_set.json', 'w') as f:
        json.dump(cache, f)


def timer(f):
    is_evaluating = False

    def wrap(x):
        nonlocal is_evaluating
        if is_evaluating:
            return f(x)
        else:
            start_time = time()
            is_evaluating = True
            try:
                value = f(x)
            finally:
                is_evaluating = False
            result = f(x)
            end_time = time()
            duration = '{:06.3f}'.format(end_time - start_time)
            print(
                f'{f.__name__}({x}) = {result}, duration {duration} seconds')
            return value

    return wrap


@timer
def fibonacci_iterative(n: int) -> int:
    value_list = []
    if n == 0 or n == 1:
        return n
    else:
        a, b = 0, 1
        for i in range(n):
            value_list.append(a)
            a, b = b, a + b
        value = value_list[-1] + value_list[-2]
        return value


@timer
def fibonacci_recursive(n: int) -> int:
    if n == 0 or n == 1:
        return n
    else:
        cache_value = cache.get(n)
        if cache_value is not None:
            return cache_value
        else:
            value = fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
            cache[n] = value
            return value


if __name__ == '__main__':
    cache = load_cache()

    input_values = [15, '45', 35]
    for i in input_values:
        if isinstance(i, int) and i >= 0:
            fibonacci_iterative(i)
            fibonacci_recursive(i)
        else:
            print(f"The value '{i}' must be integer greater or equal to 0.")
    save_cache(cache)
    print("recursion maximum depth: ", sys.getrecursionlimit())