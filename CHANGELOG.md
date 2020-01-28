# Changelog

## [2.6.0]

* New `kvitems` method in all backends.
  Like `items`, it takes a prefix,
  and iterates over the key/value pairs of matching objects
  (instead of iterating over objects themselves, like in `items`).
  This is useful for iterating over big objects
  that would otherwise consume too much memory.
* When using python 2, all backends now return
  `map_key` values as `unicode` objects, not `str`
  (until now only the Python backend did so).
  This is what the `json` built-in module does,
  and allows for correctly handling non-ascii key names.
  Comparison between `unicode` and `str` objects is possible,
  so most client code should be unaffected.
* Improving error handling in yajl2 backend (ctypes-based)
  so exceptions caught in callbacks interrupt the parsing process.
* Including more files in source distributions (#14).
* Adjusting python backend to avoid reading off the input stream
  too eagerly (#15).

## [2.5.1]

* Fixing backwards compatibility, allowing
  string readers in all backends (#12, #13).

## [2.5]

* Default backend changed (#5).
  Instead of using the python backend,
  now the fastest available backend is selected by default.
* Added support for new `map_type` option (#7).
* Fixed bug in `multiple_values` support in C backend (#8).
* Added support for ``multiple_values`` flag in python backend (#9).
* Forwarding `**kwargs` from `ijson.items` to `ijson.parse` and
  `ijson.basic_parse` (#10).
* Fixing support for yajl versions < 1.0.12.
* Improving `common.number` implementation.
* Documenting how events and the prefix work (#4).

## [2.4]

- New `ijson.backends.yajl2_c` backend written in C
  and based on the yajl2 library.
  It performs ~10x faster than cffi backend.
- Adding more builds to Travis matrix.
- Preventing memory leaks in `ijson.items`
- Parse numbers consistent with stdlib json
- Correct JSON string parsing in python backend
- Publishing package version in __init__.py
- Various small fixes in cffi backend

[2.4]: https://github.com/ICRAR/ijson/releases/tag/2.4
[2.5]: https://github.com/ICRAR/ijson/releases/tag/v2.5
[2.5.1]: https://github.com/ICRAR/ijson/releases/tag/v2.5.1
[2.6.0]: https://github.com/ICRAR/ijson/releases/tag/v2.6.0
