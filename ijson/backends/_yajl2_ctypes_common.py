'''
Common ctypes routines for yajl library handling
'''

from ctypes import Structure, c_uint, c_char, c_ubyte, c_int, c_long, c_double,\
                   c_void_p, c_char_p, CFUNCTYPE, POINTER, string_at, cast

from ijson import common, backends
from ijson.compat import b2s


C_EMPTY = CFUNCTYPE(c_int, c_void_p)
C_INT = CFUNCTYPE(c_int, c_void_p, c_int)
C_LONG = CFUNCTYPE(c_int, c_void_p, c_long)
C_DOUBLE = CFUNCTYPE(c_int, c_void_p, c_double)
C_STR = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)


_callback_data = [
    # Mapping of JSON parser events to callback C types and value converters.
    # Used to define the Callbacks structure and actual callback functions
    # inside the parse function.
    ('null', C_EMPTY, lambda: None),
    ('boolean', C_INT, lambda v: bool(v)),
    # "integer" and "double" aren't actually yielded by yajl since "number"
    # takes precedence if defined
    ('integer', C_LONG, lambda *_args: None),
    ('double', C_DOUBLE, lambda *_args: None),
    ('number', C_STR, lambda v, l: common.integer_or_decimal(b2s(string_at(v, l)))),
    ('string', C_STR, lambda v, l: string_at(v, l).decode('utf-8')),
    ('start_map', C_EMPTY, lambda: None),
    ('map_key', C_STR, lambda v, l: string_at(v, l).decode('utf-8')),
    ('end_map', C_EMPTY, lambda: None),
    ('start_array', C_EMPTY, lambda: None),
    ('end_array', C_EMPTY, lambda: None),
]

class Callbacks(Structure):
    _fields_ = [(name, type) for name, type, func in _callback_data]

YAJL_OK = 0
YAJL_CANCELLED = 1
YAJL_INSUFFICIENT_DATA = 2
YAJL_ERROR = 3


def get_yajl(version):
    yajl = backends.find_yajl_ctypes(version)
    yajl.yajl_alloc.restype = POINTER(c_char)
    yajl.yajl_get_error.restype = POINTER(c_char)
    return yajl

def _callback(send, event, func_type, func):
    def c_callback(_context, *args):
        send((event, func(*args)))
        return 1
    return func_type(c_callback)

def make_callbaks(send):
    return Callbacks(*[_callback(send, *data) for data in _callback_data])

def yajl_get_error(yajl, handle, buffer):
    perror = yajl.yajl_get_error(handle, 1, buffer, len(buffer))
    error = cast(perror, c_char_p).value
    yajl.yajl_free_error(handle, perror)
    return error
