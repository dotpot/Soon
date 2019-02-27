import concurrent
import time
from concurrent.futures import (
    ThreadPoolExecutor,
)

import pytest

from soon import (
    workers,
)

SLEEP = 0.5
TIMEOUT = 0.1
X = 2


def test_threads_decorator():
    @workers(X)
    def background_add(x, y):
        time.sleep(SLEEP)
        return x + y

    x, y = 2, 2

    start = time.time()

    results = []
    for i in range(X):
        results.append(background_add(x, y))

    checkpoint = time.time()

    end = time.time()
    assert (checkpoint - start) < SLEEP
    assert (end - start) < (SLEEP * X)


def test_shared_executor():
    executor = ThreadPoolExecutor(X)

    @workers(executor)
    def f(x):
        time.sleep(SLEEP)
        return x

    @workers(executor)
    def g(x):
        time.sleep(SLEEP)
        return x

    start = time.time()

    results = []
    for i in range(X):
        results.append(g(f(i)))

    end = time.time()
    assert (end - start) < (2 * X * SLEEP)


def test_timeout():
    @workers(X, timeout=TIMEOUT)
    def raises_timeout_error():
        time.sleep(SLEEP)

    # with self.assertRaises(TimeoutError):
    #     print raises_timeout_error()

    @workers(X, timeout=2 * SLEEP)
    def no_timeout_error():
        time.sleep(SLEEP)


def test_future_function():
    @workers(X)
    def returns_function():
        def f():
            return True

        return f

    true = returns_function()
    assert true is not None


def test_wait():
    mutable = []

    @workers(X)
    def side_effects():
        mutable.append(True)

    result = side_effects()
    result._wait()
    assert mutable[0]

    @workers(X, timeout=0.1)
    def side_effects_timeout():
        time.sleep(1)

    result = side_effects_timeout()
    with pytest.raises(concurrent.futures._base.TimeoutError):
        result._wait()
