import json

from datetime import date, time, datetime
from typing import List, Dict, Any, Union
from openapitools.helpers import properties, is_scalar


class Definition:
    __fields: dict

    def __init__(self, **kwargs):
        self.__fields = self.guard(kwargs)

    @property
    def fields(self):
        return self.__fields

    def guard(self, fields):
        return {k: v for k, v in fields.items() if k in properties(self.__class__).keys()}

    def serialize(self):
        return _serialize(self.fields)

    def __str__(self):
        return json.dumps(self.serialize())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return isinstance(other, self.__class__) and self.__fields == other.__fields

        return False

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash(self)


class Schema(Definition):
    type: str
    format: str
    title: str
    description: str
    nullable: bool
    required: bool
    default: None
    example: None
    oneOf: List[Definition]
    anyOf: List[Definition]
    allOf: List[Definition]

    _definitions = {}

    @staticmethod
    def definitions():
        return Schema._definitions

    @staticmethod
    def make(value, **kwargs):
        if isinstance(value, Schema):
            return value

        if value is None:
            return Schema(nullable=True)

        _type = type(value)

        if is_scalar(_type):
            kwargs['default'] = value

        if _type == type:
            _type = value

        if _type == bool:
            return Boolean(**kwargs)
        elif _type == int:
            return Integer(**kwargs)
        elif _type == float:
            return Float(**kwargs)
        elif _type == complex:
            return Float(**kwargs)  # TODO format?
        elif _type == str:
            return String(**kwargs)
        elif _type == bytes:
            return Byte(**kwargs)
        elif _type == bytearray:
            return Binary(**kwargs)
        elif _type == object:
            return Object(**kwargs)
        elif _type == date:
            return Date(**kwargs)
        elif _type == time:
            return Time(**kwargs)
        elif _type == datetime:
            return DateTime(**kwargs)
        elif _type == list:
            _items = Schema(nullable=True)

            if value != list:
                if len(value) == 1:
                    _items = Schema.make(value[0])
                elif len(value) > 1:
                    _items = Schema(oneOf=[Schema.make(x) for x in value])

            return Array(_items, **kwargs)
        elif _type == range:
            args = {}

            if value != range:
                args = {
                    'minimum': min(value),
                    'maximum': max(value)
                }

            return Array(Integer(**args), **kwargs)
        elif _type == dict:
            _properties = None

            if value != dict:
                _properties = {k: Schema.make(v) for k, v in value.items()}

            return Object(_properties, **kwargs)
        else:
            if value not in Schema._definitions:
                Schema._definitions[value] = Object({k: Schema.make(v) for k, v in properties(value).items()}, **kwargs)

            return Schema._definitions[value]


class Reference(Schema):
    def __init__(self, value):
        super().__init__(**{'$ref': value})

    def guard(self, fields: Dict[str, Any]):
        return fields


class Boolean(Schema):
    def __init__(self, **kwargs):
        super().__init__(type="boolean", **kwargs)


class Number(Schema):
    multipleOf: Union[int, float]
    maximum: Union[int, float]
    exclusiveMaximum: bool
    minimum: Union[int, float]
    exclusiveMinimum: bool


class Integer(Number):
    def __init__(self, **kwargs):
        super().__init__(type="integer", format="int32", **kwargs)


class Long(Number):
    def __init__(self, **kwargs):
        super().__init__(type="integer", format="int64", **kwargs)


class Float(Number):
    def __init__(self, **kwargs):
        super().__init__(type="number", format="float", **kwargs)


class Double(Number):
    def __init__(self, **kwargs):
        super().__init__(type="number", format="double", **kwargs)


class String(Schema):
    maxLength: int
    minLength: int
    pattern: str

    def __init__(self, **kwargs):
        super().__init__(type="string", **kwargs)


class Byte(String):
    def __init__(self, **kwargs):
        super().__init__(format="byte", **kwargs)


class Binary(String):
    def __init__(self, **kwargs):
        super().__init__(format="binary", **kwargs)


class Date(Schema):
    def __init__(self, **kwargs):
        super().__init__(type="string", format="date", **kwargs)


class Time(Schema):
    def __init__(self, **kwargs):
        super().__init__(type="string", format="time", **kwargs)


class DateTime(Schema):
    def __init__(self, **kwargs):
        super().__init__(type="string", format="date-time", **kwargs)


class Password(String):
    def __init__(self, **kwargs):
        super().__init__(type="string", format="password", **kwargs)


class Email(String):
    def __init__(self, **kwargs):
        super().__init__(type="string", format="email", **kwargs)


class Object(Schema):
    properties: Dict[str, Schema]
    maxProperties: int
    minProperties: int
    additionalProperties: Union[bool, Schema]

    def __init__(self, _properties: Dict[str, Any]=None, **kwargs):
        if _properties:
            kwargs['properties'] = {k: Schema.make(v) for k, v in _properties.items()}

        super().__init__(type="object", **kwargs)


class Array(Schema):
    items: Schema
    maxItems: int
    minItems: int
    uniqueItems: bool

    def __init__(self, items: Any, **kwargs):
        super().__init__(type="array", items=Schema.make(items), **kwargs)


def _serialize(value) -> Any:
    if isinstance(value, Definition):
        return value.serialize()

    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items() if v}

    if isinstance(value, list):
        return [_serialize(v) for v in value if v]

    return value
