"""Structural metrics that radon does not report (task #14, reused for task #34).

Usage:  python tools/metrics.py <file.py> [<file.py> ...]

Counts, per run over all given files together:
- functions and classes defined in the project (methods count as functions)
- module-level global variables (simple assignments at module level, excluding imports)
- fan-in / fan-out between project-defined functions (course Table 4.3) and the
  Henry-Kafura value fan-in x fan-out as the course defines it (p. 168)
- database touchpoints: calls to .execute / .executemany / .commit / sqlite3.connect,
  and how many project functions contain at least one of them
- console I/O calls (print / input) found inside functions other than main()

It reads the source only (ast); it never imports or runs the measured code.
"""
import ast
import sys
from collections import defaultdict

DB_CALLS = {"execute", "executemany", "executescript", "commit", "connect"}


def call_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def analyse(paths):
    functions, classes, globals_ = {}, [], []
    for path in paths:
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                globals_ += [f"{path}:{t.id}" for t in targets if isinstance(t, ast.Name)]
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(f"{path}:{node.name}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions[node.name] = node

    fan_out, fan_in = defaultdict(set), defaultdict(set)
    db_calls, sql_statements, io_outside_main = defaultdict(int), 0, defaultdict(int)
    for name, fn in functions.items():
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            callee = call_name(node)
            if callee in functions and callee != name:
                fan_out[name].add(callee)
                fan_in[callee].add(name)
            if callee in DB_CALLS:
                db_calls[name] += 1
                if callee in {"execute", "executemany", "executescript"}:
                    sql_statements += 1
            if callee in {"print", "input"} and name != "main":
                io_outside_main[name] += 1

    print(f"Files: {', '.join(paths)}")
    print(f"Functions: {len(functions)}   Classes: {len(classes)}   Global variables: {len(globals_)} {globals_}")
    print(f"SQL statements executed: {sql_statements}")
    print(f"Functions touching the database: {len(db_calls)} of {len(functions)}")
    print(f"Functions doing console I/O besides main(): {len(io_outside_main)}")
    print()
    print(f"{'function':<24}{'fan-in':>7}{'fan-out':>8}{'HK fan-in*fan-out':>19}{'DB calls':>10}{'print/input':>13}")
    for name in functions:
        fi, fo = len(fan_in[name]), len(fan_out[name])
        print(f"{name:<24}{fi:>7}{fo:>8}{fi * fo:>19}{db_calls[name]:>10}{io_outside_main[name]:>13}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    analyse(sys.argv[1:])
