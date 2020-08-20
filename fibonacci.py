import json
from time import time
import sys
import argparse


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


@timer
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


def parser(command_line=None):
    parser = argparse.ArgumentParser('Run fibonacci function.')

    subprasers = parser.add_subparsers(dest='command')
    fib = subprasers.add_parser('fib', help='integers for fibonacci iterative function')

    fib.add_argument('arguments', type=int, help='arguments for fibonacci iterative function')

    fib_recursive  = subprasers.add_parser('fib_recursive', help='integers for fibonacci recursive function')
    fib_recursive .add_argument('arguments', type=int, default=0, help='arguments for ibonacci recursive function')

    args = parser.parse_args(command_line)


    if args.command == 'fib':

        a = args.arguments
        fibonacci_iterative(a)

    elif args.command == 'fib_recursive':
        a = args.arguments
        fibonacci_recursive(a)


if __name__ == '__main__':
    cache = load_cache()

    parser()

    input_values = [*range(0)]
    for i in input_values:
        fibonacci_iterative(i)
        fibonacci_recursive(i)

    save_cache(cache)
    print("recursion maximum depth: ", sys.getrecursionlimit())
