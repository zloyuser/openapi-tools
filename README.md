# OpenAPI v3 Tools

[![Build Status](https://travis-ci.org/zloyuser/openapi-tools.svg?branch=master)](https://travis-ci.org/zloyuser/openapi-tools)
[![PyPI](https://img.shields.io/pypi/v/openapi-tools.svg)](https://pypi.python.org/pypi/openapi-tools/)
[![PyPI](https://img.shields.io/pypi/pyversions/openapi-tools.svg)](https://pypi.python.org/pypi/openapi-tools/)

OpenAPI v3 object model and helpers.

## Installation

```shell
pip install openapitools
```

## Usage

```python
from openapitools import SpecificationBuilder, ComponentsBuilder, OperationBuilder, Schema


class Todo:
    id: int
    text: str
    done: False


components = ComponentsBuilder()
components.scheme(Todo.__name__, Schema.make(Todo))

builder = SpecificationBuilder(components)
builder.describe('TODO REST API', '1.0')
builder.license('MIT')
builder.contact('John Doe', 'https://example.com', 'john-doe@example.com')

get_todo = OperationBuilder()
get_todo.parameter('id', int, 'path')
get_todo.describe('Get todo by ID')
get_todo.tag('todo')
get_todo.response(200, Todo)

builder.operation('/todo/{id}', 'GET', get_todo)

print(builder.build())
```
