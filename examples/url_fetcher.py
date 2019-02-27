import time

import requests

from soon import workers

urls = [
    'https://cnn.com',
    'https://news.ycombinator.com/',
    'https://stackoverflow.com/',
    'https://www.reddit.com/',
    'http://digg.com/',
    'http://news.yahoo.com/',
    'http://news.google.com/',
    'http://www.huffingtonpost.com/',
    'https://slashdot.org/',
]


@workers(10)
def fetch_async(url):
    print(f"..fetch async {url}")
    return requests.get(url)


def fetch_sync(url):
    print(f"..fetch sync {url}")
    return requests.get(url)


if __name__ == "__main__":
    print("Fetching sync...")
    start = time.time()
    responses = [fetch_sync(url) for url in urls]
    html = [response.text for response in responses]
    print(f"Fetched html len: {len(html)}")
    end = time.time()
    print("Fetch sync time: %f seconds" % (end - start))

    print("Fetching sync...")
    start = time.time()
    responses = [fetch_async(url) for url in urls]
    html = [response.text for response in responses]
    print(f"Fetched html len: {len(html)}")
    end = time.time()
    print("Fetch async time: %f seconds" % (end - start))
