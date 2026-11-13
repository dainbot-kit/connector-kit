# examples

Short, offline Python demos of common agent patterns. They use only the
standard library, a fake (scripted) model, and no API keys or network.
From the repo root, run any file with:

```
python3 examples/01_agent_loop.py
```

Or, from this folder, `python3 01_agent_loop.py`. For the skill-library
demo, run `06_skill_library.py` twice: the first run solves and saves a
skill, the second run reuses it. Pass `--skills-dir` to choose the folder.

- `01_agent_loop.py`: a basic while-loop agent that calls a fake tool until the model says it is done, with a max-steps guard.
- `02_tool_calling.py`: a fake model emits a structured JSON tool call (name and arguments) that the harness validates against a JSON-schema-style tool definition, executes, and feeds back.
- `03_react_loop.py`: a ReAct-style Thought / Action / Observation loop, printed step by step, that ends with a Final Answer.
- `04_graph.py`: a simple graph of nodes and edges as a plain dict, with state passed between nodes, a conditional edge, and an END node (the same idea LangGraph uses, without depending on it).
- `05_code_execution_tool.py`: a fake model writes Python as a string, and the harness runs it in a separate isolated (`-I`) subprocess with a timeout and a temp working directory.
- `06_skill_library.py`: procedural memory that saves a solved tool sequence to a JSON skill file and reuses it on the next run instead of re-solving.
