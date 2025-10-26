from typing import Any, Callable, Hashable, TypeVar

from langgraph._internal._typing import StateLike
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from graph_topper.utils import resolve_callable_name

StateT = TypeVar("StateT", bound=StateLike)


class Topper:
    """
    Class used to create decorators for methods which are used to define the behavior of a langgraph.garph.StateGraph.
    Can be mostly seen as syntactic sugar as it provides no additional functionality over StateGraphs. Its purpose is to
    define control logic alongside step logic, i.e. define when something should happen and what should happen.
    Frequently used methods (`StateGraph(State)` and  `compile()`) of StateGraph are wrapped and can be accessed
    directly, all other, more specialized functionality can be accessed through via the `graph` property where the
    underlying StateGraph is located.

    Usage:
    >>> from graph_topper import Topper
    >>> from langgraph.constants import END
    >>>
    >>> class State: ...
    >>>
    >>> graph = Topper(State)
    >>>
    >>> @graph.node()
    >>> def a(state: State): ...
    >>>
    >>> @graph.node(dependencies=[a])
    >>> def b(state: State): ...
    >>>
    >>> @graph.node(dependencies=[a])
    >>> def c(state: State): ...
    >>>
    >>> @graph.branch(c, {True: END, False: c})
    >>> def check(state: State): ...
    """

    def __init__(self, state_schema: type[StateT] | None = None, graph: StateGraph = None):
        if state_schema and graph:
            raise ValueError("state_schema and graph are mutually exclusive.")
        if not state_schema and not graph:
            raise ValueError("state_schema or graph must be specified.")
        if state_schema:
            self.graph = StateGraph(state_schema)
        if graph:
            self.graph = graph

    def node(self, name="", dependencies: list[Callable | str] = None, is_end_step=False):
        """
        Decorator used for creating nodes from the decorated method.
        :param name: optional name of the node to create, defaults to method name
        :param dependencies: List of nodes that should point to this node, i.e. edges are drawn from the dependencies to
                             this node. If not defined, an edge is drawn from START to this node.
        :param is_end_step: If True, an edge is drawn from this node to END
        Usage:
        >>> graph = Topper(State)
        >>>
        >>> @graph.node()
        >>> def a(state: State): ...
        """

        def wrapper(func):
            node_name = name or func.__name__
            self.graph.add_node(node_name, func)

            if dependencies:
                for dependency_name in resolve_callable_name(dependencies):
                    self.graph.add_edge(dependency_name, node_name)
            else:
                self.graph.add_edge(START, node_name)

            if is_end_step:
                self.graph.add_edge(node_name, END)

            return func

        return wrapper

    def branch(self, source: Callable, path_map: dict[Hashable, Callable | str]):
        """
        Decorator used for creating conditional edges.
        :param source: node that is the source of the conditional, i.e. the start of the conditional edge
        :param path_map: mapping of the return values of the decorated method to the end nodes
        Usage:
        >>> graph = Topper(State)
        >>>
        >>> @graph.branch(a, {True: END, False: c})
        >>> def check(state: State): ...
        """

        def wrapper(func):
            self.graph.add_conditional_edges(source.__name__, func, resolve_callable_name(path_map))
            return func

        return wrapper

    def compile(self) -> CompiledStateGraph[StateT, Any, Any, Any]:
        """
        Compiles the state graph into a `CompiledStateGraph` object.
        Directly calls the `compile()` method for StateGraph.`
        Usage:
        >>> graph.compile()
        """
        return self.graph.compile()
