#!/usr/bin/env python3
"""The model writes Python; the harness runs it in a basic subprocess sandbox."""

# "Code execution as a tool" means the model does not calculate everything
# itself. It writes a short Python program, and the harness runs that
# program and sends the printed output back.
#
# This sandbox is intentionally basic:
#   - a separate subprocess, so a crash does not take down the harness
#   - a timeout, so a tight loop cannot hang forever
#   - Python's -I isolated mode, which ignores PYTHONPATH and user-site
#     packages, so the snippet sees a clean standard library
#   - a temporary working directory, so files the snippet writes do not
#     land in this repo
#
# A real sandbox is much stricter. Production systems typically run the
# code in a container (or a microVM), drop privileges, block network
# access, and limit CPU and memory. Do not treat this file as a secure
# sandbox for untrusted code.

import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT_SECONDS = 5


def fake_model():
    """Return a short Python program the harness should run.

    The program only uses the standard library and prints one line.
    Sum of squares 1^2 + 2^2 + ... + 5^2 is 55.
    """
    return (
        "total = 0\n"
        "for n in range(1, 6):\n"
        "    total += n * n\n"
        "print(total)\n"
    )


def run_in_sandbox(code):
    """Run `code` in an isolated Python subprocess and return its stdout."""
    with tempfile.TemporaryDirectory(prefix="code_tool_") as tmp:
        snippet = Path(tmp) / "snippet.py"
        snippet.write_text(code, encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, "-I", str(snippet)],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    if completed.returncode != 0:
        raise SystemExit(
            f"snippet failed with code {completed.returncode}: {completed.stderr}"
        )
    return completed.stdout


def main():
    code = fake_model()
    print("model wrote this program:")
    print(code, end="" if code.endswith("\n") else "\n")
    print(f"running it with {sys.executable} -I, timeout={TIMEOUT_SECONDS}s")
    stdout = run_in_sandbox(code)
    print(f"stdout: {stdout.rstrip()}")
    print("final answer: 55")


if __name__ == "__main__":
    main()
