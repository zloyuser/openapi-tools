import unittest

from openapitools.types import *


class Foo:
    a: str


class Bar:
    i: int
    f: Foo


test_foo = Object(properties={'a': String()})
test_bar = Object(properties={'i': Integer(), 'f': test_foo})


test_make_provider = [
    (None, Schema, {'nullable': True}),
    (bool, Boolean, {'type': 'boolean'}),
    (True, Boolean, {'type': 'boolean', 'default': True}),
    (False, Boolean, {'type': 'boolean', 'default': False}),
    (int, Integer, {'type': 'integer', 'format': 'int32'}),
    (10, Integer, {'type': 'integer', 'format': 'int32', 'default': 10}),
    (0, Integer, {'type': 'integer', 'format': 'int32', 'default': 0}),
    (float, Float, {'type': 'number', 'format': 'float'}),
    (0.1, Float, {'type': 'number', 'format': 'float', 'default': 0.1}),
    (complex, Float, {'type': 'number', 'format': 'float'}),
    (str, String, {'type': 'string'}),
    ("", String, {'type': 'string', 'default': ''}),
    (bytes, Byte, {'type': 'string', 'format': 'byte'}),
    (bytearray, Binary, {'type': 'string', 'format': 'binary'}),
    (date, Date, {'type': 'string', 'format': 'date'}),
    (time, Time, {'type': 'string', 'format': 'time'}),
    (datetime, DateTime, {'type': 'string', 'format': 'date-time'}),
    (list, Array, {'type': 'array', 'items': Schema(nullable=True)}),
    (["a"], Array, {'type': 'array', 'items': String(default="a")}),
    (range, Array, {'type': 'array', 'items': Integer()}),
    (range(1, 10), Array, {'type': 'array', 'items': Integer(minimum=1, maximum=9)}),
    (object, Object, {'type': 'object'}),
    (dict, Object, {'type': 'object'}),
    (Bar, Object, test_bar.fields),
    (Bar(), Object, test_bar.fields),
]


class SchemaTestCase(unittest.TestCase):
    def test_make(self):
        for (k, v, fields) in test_make_provider:
            schema = Schema.make(k)

            self.assertIsInstance(schema, v)
            self.assertEqual(fields, schema.fields)
