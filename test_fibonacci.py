import fibonacci as fb
import pytest
import os.path


def test_fibonacci_iterative_int():
    assert fb.fibonacci_iterative(10) == 55


def test_fibonacci_iterative_zero():
    assert fb.fibonacci_iterative(0) == 0


def test_fibonacci_iterative_str():
    with pytest.raises(fb.FibonacciBadArgumentError):
        fb.fibonacci_iterative("24")


def test_fibonacci_iterative_negative():
    with pytest.raises(fb.FibonacciBadIntegerError):
        fb.fibonacci_iterative(-5)


def test_fibonacci_recursive_int():
    fb.cache = fb.load_cache()
    assert fb.fibonacci_recursive(10) == 55


def test_fibonacci_recursive_zero():
    assert fb.fibonacci_recursive(0) == 0


def test_fibonacci_recursive_str():
    with pytest.raises(fb.FibonacciBadArgumentError):
        fb.fibonacci_recursive("24")


def test_fibonacci_recursive_negative():
    with pytest.raises(fb.FibonacciBadIntegerError):
        fb.fibonacci_recursive(-5)


def test_load_cache():
    if not os.path.isfile('cache_set.json'):
        assert fb.load_cache() == {}
