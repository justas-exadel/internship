import fibonacci as fb
import pytest
import os.path


@pytest.fixture
def fibonacci_arguments():
    a = 10
    b = 0
    c = "24"
    d = -5
    return [a, b, c, d]


def test_fibonacci_iterative_int(fibonacci_arguments):
    result = 55
    assert fb.fibonacci_iterative(fibonacci_arguments[0]) == result


def test_fibonacci_iterative_zero(fibonacci_arguments):
    result = 0
    assert fb.fibonacci_iterative(fibonacci_arguments[1]) == result


def test_fibonacci_iterative_str(fibonacci_arguments):
    with pytest.raises(fb.FibonacciBadArgumentError):
        fb.fibonacci_iterative(fibonacci_arguments[2])


def test_fibonacci_iterative_negative(fibonacci_arguments):
    with pytest.raises(fb.FibonacciBadIntegerError):
        fb.fibonacci_iterative(fibonacci_arguments[3])


def test_fibonacci_recursive_int(fibonacci_arguments):
    fb.cache = fb.load_cache()
    result = 55
    assert fb.fibonacci_recursive(fibonacci_arguments[0]) == result


def test_fibonacci_recursive_zero(fibonacci_arguments):
    result = 0
    assert fb.fibonacci_recursive(fibonacci_arguments[1]) == result


def test_fibonacci_recursive_str(fibonacci_arguments):
    with pytest.raises(fb.FibonacciBadArgumentError):
        fb.fibonacci_recursive(fibonacci_arguments[2])


def test_fibonacci_recursive_negative(fibonacci_arguments):
    with pytest.raises(fb.FibonacciBadIntegerError):
        fb.fibonacci_recursive(fibonacci_arguments[3])


def test_load_cache():
    if not os.path.isfile('cache_set.json'):
        assert fb.load_cache() == {}
