"""With graph_topper"""

from langgraph.constants import END

from graph_topper import Topper as StateGraph


class State: ...


graph = StateGraph(State)


@graph.node()
def a(state: State): ...


@graph.node(dependencies=[a])
def b(state: State): ...


@graph.node(dependencies=[a])
def c(state: State): ...


@graph.branch(c, {True: END, False: c})
def check(state: State): ...


""" without graph_topper """
from langgraph.constants import START
from langgraph.graph import StateGraph


def a(state: State): ...


def b(state: State): ...


def c(state: State): ...


def check(state: State): ...


graph = StateGraph(State)
graph.add_node("a", a)
graph.add_node("b", b)
graph.add_node("c", c)

graph.add_edge(START, "a")
graph.add_edge("a", "b")
graph.add_edge("a", "c")

graph.add_conditional_edges("c", check, {True: END, False: "c"})
