from graph_topper.utils import resolve_callable_name


def test_resolve_callable_name_with_list():
    def a(): ...

    test_input = [a, "b"]

    actual = resolve_callable_name(test_input)
    expected = ["a", "b"]

    assert actual == expected


def test_resolve_callable_name_with_dict():
    def a(): ...

    test_input = {1: a, 2: "b"}

    actual = resolve_callable_name(test_input)
    expected = {1: "a", 2: "b"}

    assert actual == expected
