from ijson import compat

from .test_base import FileBasedTests, generate_test_cases


# Generating real TestCase classes for each importable backend
if compat.IS_PY35:
    from . import _test_async
    Async = type('Async', (_test_async.Async, FileBasedTests), {})
    generate_test_cases(globals(), Async)