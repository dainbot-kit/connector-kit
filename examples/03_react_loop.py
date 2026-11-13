#!/usr/bin/env python3
"""A ReAct loop: Thought, Action, Observation, then a Final Answer."""

# ReAct (Reason + Act) is a common pattern for making a model's work
# visible. On each turn the model writes:
#   Thought:      what it is trying to do next, in plain language
#   Action:       a tool name and its arguments
#   Observation:  the tool's result, filled in by the harness
# It repeats until it has enough information, then writes:
#   Final Answer: the reply to the user
#
# The "model" here is scripted, so this runs offline with no API key.


def lookup(topic):
    """A tiny fake knowledge tool."""
    facts = {"capital of France": "Paris"}
    return facts.get(topic, "unknown")


def count_letters(text):
    """Count the letters in a word, ignoring spaces."""
    return str(sum(1 for ch in text if ch.isalpha()))


TOOLS = {"lookup": lookup, "count_letters": count_letters}

# Each item is one turn the fake model will take. A real model would
# produce the next thought and action after seeing the latest observation.
SCRIPT = [
    {
        "thought": "I need the capital of France first.",
        "action": "lookup",
        "arguments": {"topic": "capital of France"},
    },
    {
        "thought": "Now I can count the letters in that name.",
        "action": "count_letters",
        "arguments": {"text": None},  # filled from the previous observation
    },
]


def main():
    task = "What is the capital of France, and how many letters does it have?"
    print(f"task: {task}\n")
    last_observation = None

    for step in SCRIPT:
        arguments = dict(step["arguments"])
        # The second action uses the previous observation as its input,
        # the same way a real model would after reading the last result.
        if step["action"] == "count_letters" and arguments["text"] is None:
            arguments["text"] = last_observation

        print(f"Thought: {step['thought']}")
        print(f"Action: {step['action']}({arguments})")

        result = TOOLS[step["action"]](**arguments)
        last_observation = result
        print(f"Observation: {result}\n")

    answer = f"Paris has {last_observation} letters."
    print(f"Final Answer: {answer}")


if __name__ == "__main__":
    main()
