from typing import Callable, Hashable, overload


@overload
def resolve_callable_name(iterable: list[Callable | str]) -> list[str]: ...


@overload
def resolve_callable_name(d: dict[Hashable, Callable | str]) -> dict[Hashable, str]: ...


def resolve_callable_name(x: list[Callable | str] | dict[Hashable, Callable | str]):
    if isinstance(x, dict):
        return {key: value.__name__ if callable(value) else value for key, value in x.items()}
    if isinstance(x, list):
        return [item.__name__ if callable(item) else item for item in x]
