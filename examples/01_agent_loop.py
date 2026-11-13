#!/usr/bin/env python3
"""A basic agent while-loop: call tools until the model says it is done."""

# This file shows the shape of almost every agent you will meet:
#   1. the model looks at the task and the results so far
#   2. it either calls a tool, or it says it is finished
#   3. the harness runs the tool and adds the result to the history
#   4. go back to step 1
#
# A real agent would call a language-model API in fake_model().
# Here the "model" is a small function with a fixed plan, so this
# file runs offline with no API key and no extra packages.


def add(arguments):
    """A fake tool: add two numbers and return the sum as a string."""
    return str(arguments["a"] + arguments["b"])


TOOLS = {"add": add}

# Stop even if the model never says it is done. Without this, a buggy
# model could loop forever.
MAX_STEPS = 8


def fake_model(task, history):
    """Pretend to be a model that solves the task in a few tool calls.

    history is a list of {"tool", "arguments", "result"} dicts from
    earlier steps. The model uses those results to decide what to do next.
    """
    if len(history) == 0:
        # First thought: add the two numbers in the question.
        return {"type": "tool", "name": "add", "arguments": {"a": 19, "b": 23}}
    if len(history) == 1:
        # Second thought: add 10 to whatever the first tool returned.
        so_far = int(history[0]["result"])
        return {"type": "tool", "name": "add", "arguments": {"a": so_far, "b": 10}}
    # We have both results, so we can stop.
    return {"type": "done", "answer": history[-1]["result"]}


def main():
    task = "Add 19 and 23, then add 10 to the result."
    history = []
    print(f"task: {task}")

    for step in range(1, MAX_STEPS + 1):
        decision = fake_model(task, history)
        print(f"step {step}: {decision}")

        if decision["type"] == "done":
            print(f"final answer: {decision['answer']}")
            return

        if decision["type"] != "tool":
            raise SystemExit(f"unknown decision type: {decision['type']}")

        name = decision["name"]
        if name not in TOOLS:
            raise SystemExit(f"unknown tool: {name}")

        result = TOOLS[name](decision["arguments"])
        print(f"  -> {name} returned {result}")
        history.append(
            {"tool": name, "arguments": decision["arguments"], "result": result}
        )

    # We only get here if the model never said it was done.
    raise SystemExit(f"stopped after {MAX_STEPS} steps (max-steps guard)")


if __name__ == "__main__":
    main()
