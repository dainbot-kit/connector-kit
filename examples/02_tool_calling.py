#!/usr/bin/env python3
"""A model emits a structured tool call; the harness validates and runs it."""

# Tool calling is how a model asks the outside world to do something.
# The usual handshake is:
#   1. you give the model a list of tools, each with a JSON-schema-style
#      description of its name and arguments
#   2. the model replies with a structured call: a name plus arguments
#   3. the harness checks that the call matches the schema, runs the tool,
#      and sends the result back
#   4. the model then writes a final answer (or calls another tool)
#
# The "model" here is scripted, so this runs offline with no API key.

import json

# A tool definition in the style most APIs use: a name, a short
# description, and a JSON Schema for the arguments.
TOOLS = {
    "multiply": {
        "description": "Multiply two numbers and return the product.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"},
            },
            "required": ["x", "y"],
        },
        "run": lambda arguments: arguments["x"] * arguments["y"],
    }
}


def fake_model(stage, tool_result=None):
    """Return either a JSON tool-call string or a final answer."""
    if stage == "first":
        # Models usually emit a JSON object like this, not free-form text.
        return json.dumps({"name": "multiply", "arguments": {"x": 6, "y": 7}})
    return f"The product is {tool_result}."


def expected_type(schema_type, value):
    """Check a value against a JSON Schema primitive type name."""
    if schema_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if schema_type == "string":
        return isinstance(value, str)
    if schema_type == "boolean":
        return isinstance(value, bool)
    return False


def validate_call(call):
    """Raise ValueError if the call does not match a known tool schema."""
    if not isinstance(call, dict):
        raise ValueError("tool call must be a JSON object")
    if "name" not in call or "arguments" not in call:
        raise ValueError("tool call must have 'name' and 'arguments'")

    name = call["name"]
    arguments = call["arguments"]
    if name not in TOOLS:
        raise ValueError(f"unknown tool: {name}")
    if not isinstance(arguments, dict):
        raise ValueError("arguments must be a JSON object")

    schema = TOOLS[name]["parameters"]
    for key in schema.get("required", []):
        if key not in arguments:
            raise ValueError(f"missing required argument: {key}")
    for key, value in arguments.items():
        if key not in schema["properties"]:
            raise ValueError(f"unexpected argument: {key}")
        want = schema["properties"][key]["type"]
        if not expected_type(want, value):
            raise ValueError(f"argument {key!r} should be {want}")
    return name, arguments


def main():
    print("tools the model can use:")
    for name, spec in TOOLS.items():
        print(f"  {name}: {spec['description']}")
        print(f"    schema: {json.dumps(spec['parameters'])}")

    raw = fake_model("first")
    print(f"\nmodel emitted: {raw}")

    name, arguments = validate_call(json.loads(raw))
    result = TOOLS[name]["run"](arguments)
    print(f"harness ran {name}{arguments} -> {result}")

    # Feed the tool result back; the model now answers in plain language.
    answer = fake_model("second", tool_result=result)
    print(f"model saw the result and said: {answer}")


if __name__ == "__main__":
    main()
