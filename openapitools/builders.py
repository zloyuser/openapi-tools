from collections import defaultdict
from openapitools.definitions import *
from openapitools.types import Reference


class ComponentsBuilder:
    _schemas: Dict[str, Schema]
    _responses: Dict[str, Response]
    _parameters: Dict[str, Parameter]
    _examples: Dict[str, Example]
    _bodies: Dict[str, RequestBody]
    _headers: Dict[str, Header]
    _links: Dict[str, Link]
    _callbacks: Dict[str, Dict[str, PathItem]]
    _security: Dict[str, SecurityScheme]

    def __init__(self):
        self._schemas = {}
        self._responses = {}
        self._parameters = {}
        self._examples = {}
        self._bodies = {}
        self._headers = {}
        self._links = {}
        self._callbacks = {}
        self._security = {}

    def maybe_ref(self, section: str, content: Any):
        if type(content) != type:
            return content

        objects = getattr(self, '_' + section, {})

        if content.__name__ in objects.keys():
            return Reference("#/components/%s/%s" % (section, content.__name__))

        return content

    def scheme(self, name: str, value: Any, **kwargs):
        self._schemas[name] = Schema.make(self.maybe_ref('schemas', value), **kwargs)

    def response(self, name: str, value: Any, **kwargs):
        self._responses[name] = value if isinstance(value, Response) else \
            Response.make(self.maybe_ref('schemas', value), **kwargs)

    def parameter(self, name: str, value: Any, location: str = 'query', **kwargs):
        self._parameters[name] = value if isinstance(value, Parameter) else \
            Parameter.make(name, self.maybe_ref('schemas', value), location, **kwargs)

    def example(self, name: str, value: Any, **kwargs):
        self._examples[name] = value if isinstance(value, Example) else Example(value, **kwargs)

    def security(self, _type: str, name: str, cls: type, **kwargs):
        self._security[name] = SecurityScheme.make(_type, cls, **kwargs)

    def build(self):
        return Components(schemas=self._schemas, securitySchemes=self._security)


class OperationBuilder:
    summary: str
    description: str
    operationId: str
    requestBody: RequestBody
    externalDocs: ExternalDocumentation
    tags: List[str]
    security: List[Any]
    parameters: List[Parameter]
    responses: Dict[str, Response]
    callbacks: List[str]
    deprecated: bool = False

    def __init__(self):
        self.tags = []
        self.security = []
        self.parameters = []
        self.responses = {}

    def name(self, value: str):
        self.operationId = value

    def describe(self, summary: str = None, description: str = None):
        if summary:
            self.summary = summary

        if description:
            self.description = description

    def document(self, url: str, description: str = None):
        self.externalDocs = ExternalDocumentation(url, description)

    def tag(self, *args: str):
        for arg in args:
            self.tags.append(arg)

    def deprecate(self):
        self.deprecated = True

    def body(self, content: Any, **kwargs):
        self.requestBody = RequestBody.make(content, **kwargs)

    def parameter(self, name: str, schema: Any, location: str = 'query', **kwargs):
        if location == 'path':
            kwargs['required'] = True

        self.parameters.append(Parameter.make(name, schema, location, **kwargs))

    def response(self, status, content: Any = None, description: str = None, **kwargs):
        self.responses[status] = Response.make(content, description, **kwargs)

    def secured(self, *args, **kwargs):
        items = {**{v: [] for v in args}, **kwargs}
        gates = {}

        for name, params in items.items():
            gate = name.__name__ if isinstance(name, type) else name
            gates[gate] = params

        self.security.append(gates)

    def build(self):
        return Operation(**self.__dict__)


class SpecificationBuilder:
    _title: str
    _version: str
    _description: str
    _terms: str
    _contact: Contact
    _license: License
    _paths: Dict[str, Dict[str, OperationBuilder]]
    _tags: Dict[str, Tag]
    _components: ComponentsBuilder

    def __init__(self, components: ComponentsBuilder):
        self._components = components
        self._paths = defaultdict(dict)
        self._tags = {}

    def describe(self, title: str, version: str, description: str = None, terms: str = None):
        self._title = title
        self._version = version
        self._description = description
        self._terms = terms

    def tag(self, name: str, **kwargs):
        self._tags[name] = Tag(name, **kwargs)

    def contact(self, name: str = None, url: str = None, email: str = None):
        self._contact = Contact(name=name, url=url, email=email)

    def license(self, name: str = None, url: str = None):
        self._license = License(name, url=url)

    def operation(self, path: str, method: str, operation: OperationBuilder):
        method = method.lower()

        if not hasattr(operation, 'operationId'):
            operation.name("%s.%s" % (path, method))

        for _tag in operation.tags:
            if _tag in self._tags.keys():
                continue

            self._tags[_tag] = Tag(_tag)

        self._paths[path][method] = operation

    def build(self) -> OpenAPI:
        info = self._build_info()
        paths = self._build_paths()
        tags = self._build_tags()

        return OpenAPI(info, paths, tags=tags, components=self._components.build())

    def _build_info(self) -> Info:
        kwargs = {
            'description': self._description,
            'termsOfService': self._terms,
            'license': self._license,
            'contact': self._contact,
        }

        return Info(self._title, self._version, **kwargs)

    def _build_tags(self):
        return [self._tags[k] for k in self._tags]

    def _build_paths(self) -> Dict:
        paths = {}

        for path, operations in self._paths.items():
            paths[path] = PathItem(**{k: v.build() for k, v in operations.items()})

        return paths
