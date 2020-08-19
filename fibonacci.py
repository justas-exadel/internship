import json
from time import time
from functools import wraps
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


def validate_input(input):
    if not isinstance(input, int):
        print(f"Input value must be integer.")
        exit()
    elif input < 0:
        print(f"Input value must be greater than or equal to 0")
        exit()


def timer(func):
    @wraps(func)
    def wrap(*args):
        start_time = time()
        result = func(*args)
        end_time = time()
        duration = '{:06.3f}'.format(end_time - start_time)
        print(f'{func.__name__}({args[0]}) = {result}, duration {duration} seconds')
        return result

    return wrap


def profile(f):
    is_evaluating = False

    def g(x):
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
            end_time = time()
            print('time taken: {time}'.format(time=end_time - start_time))
            return value

    return g


@profile
def fibonacci_iterative(n: int) -> int:
    validate_input(n)
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


@profile
def fibonacci_recursive_no_cache(n: int) -> int:
    validate_input(n)
    if n == 0 or n == 1:
        return n
    else:
        return fibonacci_recursive_no_cache(n - 1) + fibonacci_recursive_no_cache(n - 2)


@profile
def fibonacci_recursive(n: int) -> int:
    validate_input(n)
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

    input_values = [0, 1, 2, 3, 4, 5, 10, 33]
    for i in input_values:
        fibonacci_iterative(i)
    for i in input_values:
        fibonacci_recursive(i)
    for i in input_values:
        fibonacci_recursive_no_cache(i)

    save_cache(cache)
    print("recursion maximum depth: ", sys.getrecursionlimit())
