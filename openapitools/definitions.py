from typing import List, Dict, Any
from openapitools.types import Definition, Schema


class Contact(Definition):
    name: str
    url: str
    email: str


class License(Definition):
    name: str
    url: str

    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)


class Info(Definition):
    title: str
    description: str
    termsOfService: str
    contact: Contact
    license: License
    version: str

    def __init__(self, title: str, version: str, **kwargs):
        super().__init__(title=title, version=version, **kwargs)


class Example(Definition):
    summary: str
    description: str
    value: Any
    externalValue: str

    def __init__(self, value: Any, **kwargs):
        super().__init__(value=value, **kwargs)


class MediaType(Definition):
    schema: Schema
    example: Any

    def __init__(self, schema: Schema, **kwargs):
        super().__init__(schema=schema, **kwargs)

    @staticmethod
    def make(value: Any):
        return MediaType(Schema.make(value))

    @staticmethod
    def all(content: Any):
        media_types = content if isinstance(content, dict) else {'*/*': content or {}}

        return {x: MediaType.make(v) for x, v in media_types.items()}


class Response(Definition):
    content: Dict[str, MediaType]
    description: str

    def __init__(self, content=None, **kwargs):
        super().__init__(content=content, **kwargs)

    @staticmethod
    def make(content, description: str = None, **kwargs):
        if not description:
            description = 'Default Response'

        return Response(MediaType.all(content), description=description, **kwargs)


class RequestBody(Definition):
    description: str
    required: bool
    content: Dict[str, MediaType]

    def __init__(self, content: Dict[str, MediaType], **kwargs):
        super().__init__(content=content, **kwargs)

    @staticmethod
    def make(content: Any, **kwargs):
        return RequestBody(MediaType.all(content), ** kwargs)


class ExternalDocumentation(Definition):
    url: str
    description: str

    def __init__(self, url: str, description=None):
        super().__init__(url=url, description=description)


class Parameter(Definition):
    name: str
    location: str
    description: str
    required: bool
    deprecated: bool
    allowEmptyValue: bool
    schema: Schema

    def __init__(self, name, schema: Schema, location: str = 'query', **kwargs):
        super().__init__(name=name, schema=schema, location=location, **kwargs)

    @property
    def fields(self):
        values = super().fields

        values['in'] = values.pop('location')

        return values

    @staticmethod
    def make(name: str, schema: Any, location: str = 'query', **kwargs):
        if location == 'path':
            kwargs['required'] = True

        return Parameter(name, Schema.make(schema), location, **kwargs)


class Operation(Definition):
    tags: List[str]
    summary: str
    description: str
    operationId: str
    requestBody: RequestBody
    externalDocs: ExternalDocumentation
    parameters: List[Parameter]
    responses: Dict[str, Response]
    security: Dict[str, List[str]]
    callbacks: List[str]
    deprecated: bool


class PathItem(Definition):
    summary: str
    description: str
    get: Operation
    put: Operation
    post: Operation
    delete: Operation
    options: Operation
    head: Operation
    patch: Operation
    trace: Operation


class SecurityScheme(Definition):
    type: str
    description: str
    scheme: str
    bearerFormat: str
    name: str
    location: str
    openIdConnectUrl: str

    def __init__(self, _type: str, **kwargs):
        super().__init__(type=_type, **kwargs)

    @property
    def fields(self):
        values = super().fields

        values['in'] = values.pop('location')

        return values

    @staticmethod
    def make(_type: str, cls: type, **kwargs):
        params = cls.__dict__ if hasattr(cls, '__dict__') else {}

        return SecurityScheme(_type, **params, **kwargs)


class ServerVariable(Definition):
    default: str
    description: str
    enum: List[str]

    def __init__(self, default: str, **kwargs):
        super().__init__(default=default, **kwargs)


class Server(Definition):
    url: str
    description: str
    variables: List[ServerVariable]

    def __init__(self, url: str, **kwargs):
        super().__init__(url=url, **kwargs)


class Header(Definition):
    description: str
    required: bool
    deprecated: bool
    allowEmptyValue: bool
    schema: Schema

    def __init__(self, schema: Schema, **kwargs):
        super().__init__(schema=schema, **kwargs)


class Link(Definition):
    operationRef: str
    operationId: str
    parameters: Dict
    requestBody: Any
    description: str
    server: Server


class Components(Definition):
    schemas: Dict[str, Schema]
    responses: Dict[str, Response]
    parameters: Dict[str, Parameter]
    examples: Dict[str, Example]
    requestBodies: Dict[str, RequestBody]
    headers: Dict[str, Header]
    securitySchemes: Dict[str, SecurityScheme]
    links: Dict[str, Link]
    callbacks: Dict[str, Dict[str, PathItem]]


class Tag(Definition):
    name: str
    description: str
    externalDocs: ExternalDocumentation

    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)


class OpenAPI(Definition):
    openapi: str
    info: Info
    servers: List[Server]
    paths: Dict[str, PathItem]
    components: Components
    security: Dict[str, SecurityScheme]
    tags: List[Tag]
    externalDocs: ExternalDocumentation

    def __init__(self, info: Info, paths: Dict[str, PathItem], **kwargs):
        super().__init__(openapi="3.0.0", info=info, paths=paths, **kwargs)
