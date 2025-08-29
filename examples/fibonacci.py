from dataclasses import dataclass

from langgraph.constants import END

from graph_topper import Topper

"""
Fibonacci Sequence is defined as follows:
f_0 = 0
f_1 = 1
f_n = f_{n-1} + f_{n-2}
-> 0, 1, 1, 2, 3, 5, 8, 13, 21, ...

This implementation is neither efficient nor does it work for n >= 25 due to the recursion limit of langgraph.
"""


@dataclass
class FibonacciState:
    n: int  # n-th fibonacci number
    iteration: int = 0
    current_number: int = 1
    previous_number: int = 0


fib_graph = Topper(FibonacciState)


@fib_graph.node()
def fib_step(state: FibonacciState):
    return {
        "iteration": state.iteration + 1,
        # special handling for the 0-th fibonacci number which is 0
        "current_number": state.current_number + state.previous_number if state.n else 0,
        "previous_number": state.current_number,
    }


@fib_graph.branch(fib_step, {False: fib_step, True: END})
def fib_check(state: FibonacciState):
    return state.iteration >= state.n


if __name__ == "__main__":
    result = fib_graph.compile().invoke(FibonacciState(n=24))
    print(f"The {result['n']}. Fibonacci number is {result['current_number']}.")
