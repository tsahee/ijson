from ijson import utils

from .test_base import generate_test_cases


class Coroutines(object):
    '''Test adaptation for coroutines'''

    suffix = '_coro'

    def all(self, routine, json_content, *args, **kwargs):
        events = utils.sendable_list()
        coro = routine(events, *args, **kwargs)
        for datum in self.inputiter(json_content):
            coro.send(datum)
        coro.close()
        return events

    def first(self, routine, json_content, *args, **kwargs):
        events = utils.sendable_list()
        coro = routine(events, *args, **kwargs)
        for datum in self.inputiter(json_content):
            coro.send(datum)
            if events:
                return events[0]
        coro.close()
        if events:
            return events[0]
        return None

generate_test_cases(globals(), Coroutines)