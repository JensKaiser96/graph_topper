from dataclasses import dataclass

from graph_topper import Topper


@dataclass
class ExampleState:
    a: int
    b: int
    i: int = 0


graph = Topper(ExampleState)


@graph.node()
def add_a(state: ExampleState) -> dict:
    return {"i": state.i + state.a}


@graph.node(dependencies=[add_a])
def multiply_b(state: ExampleState) -> dict:
    return {"i": state.i * state.b}


@graph.node(dependencies=[add_a, multiply_b])
def print_i(state: ExampleState) -> dict:
    print(state.i)
    return {}


if __name__ == "__main__":
    graph.graph.compile().invoke(ExampleState(a=3, b=5))
    """
    prints
    ```
    3
    15
    
    ```
    """
