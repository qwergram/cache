import io
import os
import pickle
import time

class CacheEntry:

    def __init__(self, value, expires):
        self.value = value
        self.expires = expires

class SimplePickleCache:
    """
    Usage:

    ```py
    with SimplePickleCache("somefile.cache") as handle:
        handle['payload'] = requests.get("some url")
    ```

    Then later in the code, refer to `handle['payload']`. Loading
    the pickled cache will preserve `handle['payload']` as well.
    """

    cache_location: str = None
    cache: dict = {}

    def __init__(self, cache_location: str, max_age: float = -1.):
        """
        cache_location refers to where this cache object will write to disk.
        max_age refers to the `time.time()` when the cache object will
        dissapear. A negative number means it will never expire.
        """
        self.cache_location = cache_location
        self.max_age = max_age
        self.cache = {}

    def __enter__(self):
        if os.path.isfile(self.cache_location):
            try:
                with io.open(self.cache_location, 'rb') as handle:
                    self.cache = pickle.load(handle)
            except (OSError, IOError, EOFError):
                self.cache = {}

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with io.open(self.cache_location, 'wb') as handle:
            pickle.dump(self.cache, handle)

    def __getitem__(self, name):
        cache: CacheEntry = self.cache[name]
        if cache.expires < 0 or cache.expires < time.time():
            return cache.value
        else:
            del self.cache[name]
            raise KeyError()

    def __setitem__(self, name, value):
        self.cache[name] = CacheEntry(value, self.max_age)

    def __delitem__(self, name):
        del self.cache[name]

    def __contains__(self, name):
        return name in self.cache


if __name__ == "__main__":
    # Sample on usage
    with SimplePickleCache("./test.cache") as cache:
        if 'number' in cache:
            print(cache['number'])
        cache['number'] = 123