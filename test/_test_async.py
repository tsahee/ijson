# -*- coding:utf-8 -*-

import asyncio
import contextlib
import io

from ijson import compat


class AsyncReader(object):
    def __init__(self, data):
        if type(data) == compat.bytetype:
            self.data = io.BytesIO(data)
        else:
            self.data = io.StringIO(data)

    async def read(self, n=-1):
        return self.data.read(n)



def _run(f):
    with contextlib.closing(asyncio.new_event_loop()) as loop:
        loop.run_until_complete(f)


def get_all(routine, json_content, *args, **kwargs):
    events = []
    async def run():
        async for event in routine(AsyncReader(json_content), *args, **kwargs):
            events.append(event)
    _run(run())
    return events


def get_first(routine, json_content, *args, **kwargs):
    events = []
    async def run():
        async for event in routine(AsyncReader(json_content), *args, **kwargs):
            events.append(event)
            if events:
                return
    _run(run())
    return events[0]