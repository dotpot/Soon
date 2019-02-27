# Soon
Worker decorator for background tasks re-using [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).

Installation
------------

Soon is conveniently available via pip:
```
pip install soon
```

or installable via `git clone` and `setup.py`
```
git clone git@github.com:dotpot/Soon.git
sudo python setup.py install
```

To ensure Soon is properly installed, you can run the unittest suite from the project root:
```
pipenv run pytest -v 
```

Usage
-----
The Soon library enables you to utilize the benefits of multi-threading with minimal concern about the implementation details.


Website fetcher example
-----------------
You've collected a list of urls and are looking to download the HTML of the lot.  The following is a perfectly reasonable first stab at solving the task.

```python
urls = [
    'https://cnn.com',
    'https://news.ycombinator.com/',
    'https://stackoverflow.com/',
]
```
---
```python
import time
import requests

def fetch(url):
    return requests.get(url)

if __name__ == "__main__":

    start = time.time()
    responses = [fetch(url) for url in urls]
    html = [response.text for response in responses]
    end = time.time()
    print("Time: %f seconds" % (end - start))
```
---

More Efficient Web Scraper
--------------------------

Using Soon's decorator syntax, we can define a function that executes in multiple threads.  Individual calls to `download` are non-blocking, but we can largely ignore this fact and write code identically to how we would in a synchronous paradigm. 

```python
import time
import requests

from soon import workers

@workers(5)
def fetch(url):
    return requests.get(url)

if __name__ == "__main__":
    start = time.time()
    responses = [fetch(url) for url in urls]
    html = [response.text for response in responses]
    end = time.time()
    print("Time: %f seconds" % (end - start))

```
We can now download websites more efficiently.

---

You can also optionally pass in `timeout` argument, to prevent hanging on a task that is not guaranteed to return.

```python
import time

from soon import workers

@workers(1, timeout=0.1)
def timeout_error():
    time.sleep(1)

if __name__ == "__main__":
    timeout_error()
```
