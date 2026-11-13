#!/usr/bin/env python3
"""A tiny agent graph: nodes, edges, shared state, and one conditional edge."""

# Many agent frameworks treat a workflow as a graph:
#   - each node is a function that reads and updates a shared state dict
#   - each edge says which node runs next
#   - a conditional edge picks the next node by looking at the state
#   - a special END node means "stop"
#
# LangGraph is a popular library that does this same idea, with extras
# like checkpoints and retries. This file uses a plain dict so it runs
# with the standard library only — no LangGraph install required.

END = "END"


def start(state):
    """Put the question into a shorter field the router can inspect."""
    state["text"] = state["question"].lower()


def router(state):
    """This node only prepares state; the conditional edge picks the next node."""
    state["kind"] = "math" if "times" in state["text"] else "greet"


def math(state):
    """A tiny 'times' handler, enough to show a branch that does work."""
    # "what is 6 times 7?" -> 42
    words = state["text"].replace("?", "").split()
    numbers = [int(w) for w in words if w.isdigit()]
    product = 1
    for n in numbers:
        product *= n
    state["answer"] = str(product)


def greet(state):
    state["answer"] = "Hello! How can I help?"


def pick_after_router(state):
    """Conditional edge: look at state and choose the next node."""
    return "math" if state["kind"] == "math" else "greet"


# The graph itself is just data: a node map, fixed edges, and one branch.
GRAPH = {
    "nodes": {
        "start": start,
        "router": router,
        "math": math,
        "greet": greet,
    },
    "edges": {
        "start": "router",
        "math": END,
        "greet": END,
        # router has no fixed edge; the conditional map decides.
    },
    "conditional": {
        "router": pick_after_router,
    },
}


def run(graph, start_node, state):
    """Walk the graph, passing the same state dict from node to node."""
    node = start_node
    while node != END:
        print(f"node={node}  state={state}")
        graph["nodes"][node](state)
        if node in graph["conditional"]:
            node = graph["conditional"][node](state)
        else:
            node = graph["edges"][node]
    print(f"node={END}  state={state}")
    return state


def main():
    # First path: the conditional edge sends this question to the math node.
    math_state = run(GRAPH, "start", {"question": "what is 6 times 7?"})
    print(f"math path answer: {math_state['answer']}\n")

    # Second path: a question with no 'times' goes to the greet node instead.
    greet_state = run(GRAPH, "start", {"question": "hi there"})
    print(f"greet path answer: {greet_state['answer']}")


if __name__ == "__main__":
    main()
