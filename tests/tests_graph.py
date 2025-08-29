from typing import Literal, TypedDict

import pytest
from langgraph.constants import START
from langgraph.graph import StateGraph

from graph_topper import Topper


class State(TypedDict):
    a: int


def test_init_with_state():
    graph = Topper(state_schema=State)
    assert graph.graph.state_schema == State


def test_init_with_graph():
    graph = Topper(graph=StateGraph(State))
    assert graph.graph.state_schema == State


@pytest.fixture
def graph():
    yield Topper(State)


def test_no_nodes_or_edges(graph):
    """
    test to check if a newly created graph has no nodes
    """
    assert not graph.graph.nodes
    assert not graph.graph.edges


def test_nodes(graph):
    """
    test to check if nodes are added to the graph
    """

    @graph.node()
    def node1(): ...

    @graph.node()
    def node2(): ...

    @graph.node()
    def node3(): ...

    actual = graph.graph.nodes.keys()
    expected = {"node1", "node2", "node3"}

    assert actual == expected


def test_edges(graph):
    """
    test to check if edges are added to the graph
    """

    @graph.node()
    def node1(): ...

    @graph.node(dependencies=[node1])
    def node2(): ...

    @graph.node(dependencies=[node1, node2])
    def node3(): ...

    actual = graph.graph.edges
    expected = {
        (START, "node1"),
        ("node1", "node2"),
        ("node2", "node3"),
        ("node1", "node3"),
    }

    assert actual == expected


def test_named_nodes(graph):
    """
    check if nodes and references with explicit names are handled correctly
    """

    @graph.node(name="node-1")
    def node1(): ...

    @graph.node(dependencies=["node-1"])
    def node2(): ...

    actual_nodes = graph.graph.nodes
    expected_nodes = {"node-1", "node2"}
    assert actual_nodes == expected_nodes

    actual_edges = graph.graph.edges
    expected_edges = {
        (START, "node1"),
        ("node1", "node2"),
        ("node2", "node3"),
        ("node1", "node3"),
    }

    assert actual_edges == expected_edges


def test_conditional_edges(graph):
    @graph.node()
    def node1(): ...

    @graph.node(dependencies=[node1])
    def node2(): ...

    @graph.node(dependencies=[node1, node2])
    def node3(): ...

    @graph.branch(node1, {"this": node2, "that": node3})
    def this_or_that() -> Literal["this", "that"]: ...

    actual = graph.graph.branches

    assert "node1" in actual
    assert "this_or_that" in actual["node1"]
    assert actual["node1"]["this_or_that"].ends == {"this": "node2", "that": "node3"}
