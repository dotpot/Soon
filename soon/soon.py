from dataclasses import dataclass
from functools import wraps

from concurrent.futures import ThreadPoolExecutor


@dataclass
class Soon:
    future: ThreadPoolExecutor
    timeout: float

    def __getattr__(self, name):
        result = self._wait()
        return result.__getattribute__(name)

    def _wait(self):
        return self.future.result(self.timeout)
        

def background(n, base_type, timeout=None):
    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError(
                "Invalid type: %s"
                % type(base_type)
            )

        @wraps(f)
        def wrapped(*args, **kwargs):
            return Soon(
                pool.submit(f, *args, **kwargs),
                timeout=timeout
            )
        return wrapped
    return decorator


def workers(n, timeout=None):
    return background(n, ThreadPoolExecutor, timeout)
