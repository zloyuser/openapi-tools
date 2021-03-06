from typing import Any, Dict, get_type_hints


def properties(value: Any) -> Dict:
    fields = {x: v for x, v in value.__dict__.items() if not x.startswith('_')}

    return {**get_type_hints(value), **fields}


def is_scalar(value: type) -> bool:
    return value in [bool, int, float, complex, str]
