# -*- coding:utf-8 -*-

from tests import JSON, JSON_OBJECT, JSON_KVITEMS, JSON_EVENTS, JSON_PARSE_EVENTS, generate_test_cases
import unittest
import asyncio
import io


class AsyncReader(object):
    def __init__(self, data):
        self.data = io.BytesIO(data)

    async def read(self, n=-1):
        return self.data.read(n)

class Base(object):

    def setUp(self):
        super()
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()
        super()

    def test_async_basic_parse(self):
        async def run():
            events = []
            async for event in self.backend.basic_parse_async(AsyncReader(JSON)):
                events.append(event)
            self.assertEqual(JSON_EVENTS, events)
        self.loop.run_until_complete(run())

    def test_async_parse(self):
        async def run():
            events = []
            async for event in self.backend.parse_async(AsyncReader(JSON)):
                events.append(event)
            self.assertEqual(JSON_PARSE_EVENTS, events)
        self.loop.run_until_complete(run())

    def test_async_items(self):
        async def run():
            objects = []
            async for obj in self.backend.items_async(AsyncReader(JSON), ''):
                objects.append(obj)
            self.assertEqual([JSON_OBJECT], objects)
        self.loop.run_until_complete(run())

    def test_async_kvitems(self):
        async def run():
            objects = []
            async for obj in self.backend.kvitems_async(AsyncReader(JSON), 'docs.item'):
                objects.append(obj)
            self.assertEqual(JSON_KVITEMS, objects)
        self.loop.run_until_complete(run())

generate_test_cases(locals(), Base)
