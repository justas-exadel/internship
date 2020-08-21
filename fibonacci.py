import functools
import pickle
from time import time
import argparse
import sys


class FibonacciError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class FibonacciBadArgumentError(FibonacciError):
    def __init__(self):
        super().__init__('Argument has to be integer.')


class FibonacciBadIntegerError(FibonacciError):
    def __init__(self):
        super().__init__('Integer has to be greater or equal to zero.')


def load_cache():
    try:
        with open("cache_set.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_cache(cache):
    with open('cache_set.pkl', 'wb') as f:
        pickle.dump(cache, f)


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


def validate_input(input):
    if not isinstance(input, int):
        raise FibonacciBadArgumentError
    elif input < 0:
        raise FibonacciBadIntegerError


@timer
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


def cached(func):
    func.cache = load_cache()
    @functools.wraps(func)
    def wrapper(*args):
        try:
            return func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            save_cache(func.cache)
            return result

    return wrapper



@timer
@cached
def fibonacci_recursive(n: int) -> int:
    validate_input(n)
    if n == 0 or n == 1:
        return n
    else:
        value = fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
        return value


def parser(command_line=None):
    parser = argparse.ArgumentParser('Run fibonacci function.')
    parser.add_argument('-fib', nargs='+', type=int,
                        help='integers for fibonacci iterative function')
    parser.add_argument('-fib_recursive', nargs='+', type=int,
                        help='integers for fibonacci recursive function')
    args = parser.parse_args()

    if (args.fib):
        for i in args.fib:
            fibonacci_iterative(i)

    if (args.fib_recursive):
        for i in args.fib_recursive:
            fibonacci_recursive(i)


if __name__ == '__main__':
    parser()
    input_values = [30, 45, 55]
    for i in input_values:
        fibonacci_iterative(i)
        fibonacci_recursive(i)
    print("recursion maximum depth: ", sys.getrecursionlimit())
