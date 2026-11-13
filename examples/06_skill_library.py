#!/usr/bin/env python3
"""Procedural memory: save a solved tool sequence and reuse it later."""

# A "skill" here is not a trained model. It is a saved recipe: the list
# of tool steps that already solved a task. The first time we see the
# task, we solve it step by step and write that sequence to a JSON file.
# The next time, we skip the solving and just replay the saved steps.
# That is procedural memory — memory of how to do something.
#
# Pass --skills-dir to choose the folder. By default it is
# ./skills_store next to this script. That folder is gitignored.

import argparse
import json
from pathlib import Path

SKILL_NAME = "celsius_comfort_check"
TASK = "Convert 25 C to Fahrenheit and say whether that is a nice day (60-80 F)."


def c_to_f(arguments):
    """Standard Celsius to Fahrenheit conversion."""
    return arguments["c"] * 9 / 5 + 32


def in_range(arguments):
    """Return True if value sits between low and high, inclusive."""
    return arguments["low"] <= arguments["value"] <= arguments["high"]


TOOLS = {"c_to_f": c_to_f, "in_range": in_range}


def fake_model_solve():
    """Scripted first-time solution: two tool calls, then an answer."""
    return [
        {"tool": "c_to_f", "arguments": {"c": 25}},
        {"tool": "in_range", "arguments": {"value": 77.0, "low": 60, "high": 80}},
    ]


def format_answer(f_value, nice):
    feeling = "a nice day" if nice else "not in the nice-day range"
    return f"{f_value} F, {feeling}."


def run_steps(steps):
    """Execute a list of {tool, arguments} steps and return the results."""
    results = []
    for step in steps:
        name = step["tool"]
        arguments = step["arguments"]
        result = TOOLS[name](arguments)
        print(f"  {name}({arguments}) -> {result}")
        results.append(result)
    return results


def parse_args():
    default_dir = Path(__file__).resolve().parent / "skills_store"
    parser = argparse.ArgumentParser(description="Save or reuse a tool-step skill.")
    parser.add_argument(
        "--skills-dir",
        default=str(default_dir),
        help="folder for saved skill JSON files (default: %(default)s)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    skills_dir = Path(args.skills_dir)
    skills_dir.mkdir(parents=True, exist_ok=True)
    skill_path = skills_dir / f"{SKILL_NAME}.json"

    print(f"task: {TASK}")
    print(f"skills dir: {skills_dir}")

    if skill_path.exists():
        skill = json.loads(skill_path.read_text(encoding="utf-8"))
        print(f"found saved skill {skill_path.name}; replaying without re-solving")
        results = run_steps(skill["steps"])
        answer = format_answer(results[0], results[1])
        print(f"final answer: {answer}")
        return

    print("no saved skill found; solving from scratch")
    steps = fake_model_solve()
    results = run_steps(steps)
    answer = format_answer(results[0], results[1])
    skill = {"name": SKILL_NAME, "task": TASK, "steps": steps}
    skill_path.write_text(json.dumps(skill, indent=2) + "\n", encoding="utf-8")
    print(f"saved skill to {skill_path}")
    print(f"final answer: {answer}")


if __name__ == "__main__":
    main()
