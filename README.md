# Cache

Usage:

```py
with SimplePickleCache("somefile.cache") as handle:
    handle['payload'] = requests.get("some url")
```

Then later in the code, refer to `handle['payload']`. Loading
the pickled cache will preserve `handle['payload']` as well.