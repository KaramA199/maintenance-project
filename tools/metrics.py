"""Structural metrics that radon does not report (task 14, reused for task 34).

Usage:  python tools/metrics.py <file.py> [<file.py> ...]

Counts, per run over all given files together:
- functions and classes defined in the project (methods count as functions)
- module-level global variables (simple assignments at module level, excluding imports)
- fan-in / fan-out between project-defined functions (course Table 4.3) and the
  Henry-Kafura value fan-in x fan-out as the course defines it (p. 168)
- database touchpoints: calls to .execute / .executemany / .commit / sqlite3.connect,
  and how many project functions contain at least one of them
- console I/O calls (print / input) found inside functions other than main()

Every function is identified by file, class and name (for example
storage.py:SqliteStorage.find_book), so functions with the same name in
different files or classes are counted separately. A call is linked to a
project function only when its target can be read from the source:
- f()                      a function of the same file, or one imported with "from m import f"
- module.f()               a function of another given file imported with "import module"
- self.f() / cls.f()       a method of the same class
- var.f()                  a method of the class assigned to var in the same function (var = C(...))
- C()                      the constructor C.__init__
Calls on other variables, such as db.find_book() where db is a parameter, cannot
be resolved without running the program. They are listed as "unresolved" and
not counted as fan-in/fan-out.

It reads the source only (ast); it never imports or runs the measured code.
"""
import ast
import os
import sys
from collections import defaultdict

SQL_CALLS = {"execute", "executemany", "executescript"}
DB_CALLS = SQL_CALLS | {"commit", "connect"}


class Function:
    def __init__(self, path, cls, node):
        self.path, self.cls, self.node = path, cls, node
        self.name = node.name
        self.key = f"{path}:{cls + '.' if cls else ''}{node.name}"


def collect(paths):
    functions, classes, globals_, imports = {}, [], [], {}
    for path in paths:
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
        module_imports = {}
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                globals_ += [f"{path}:{t.id}" for t in targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.Import):
                for a in node.names:
                    module_imports[a.asname or a.name] = ("module", a.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                for a in node.names:
                    module_imports[a.asname or a.name] = ("name", node.module, a.name)
        imports[path] = module_imports

        def visit(body, cls):
            for node in body:
                if isinstance(node, ast.ClassDef):
                    classes.append(f"{path}:{node.name}")
                    visit(node.body, node.name)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    f = Function(path, cls, node)
                    functions[f.key] = f
                    visit(node.body, cls)
        visit(tree.body, None)
    return functions, classes, globals_, imports


def resolve_call(call, fn, functions, imports, local_types):
    """Return the key of the project function a call targets, or None."""
    module_of = {os.path.splitext(os.path.basename(p))[0]: p for p in {f.path for f in functions.values()}}

    def lookup(path, cls, name):
        key = f"{path}:{cls + '.' if cls else ''}{name}"
        return key if key in functions else None

    target = call.func
    if isinstance(target, ast.Name):
        name = target.id
        hit = lookup(fn.path, None, name) or lookup(fn.path, name, "__init__")
        if hit:
            return hit
        imported = imports[fn.path].get(name)
        if imported and imported[0] == "name" and imported[1] in module_of:
            path = module_of[imported[1]]
            return lookup(path, None, imported[2]) or lookup(path, imported[2], "__init__")
        return None
    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
        owner, name = target.value.id, target.attr
        if owner in ("self", "cls") and fn.cls:
            return lookup(fn.path, fn.cls, name)
        imported = imports[fn.path].get(owner)
        if imported and imported[0] == "module" and imported[1] in module_of:
            path = module_of[imported[1]]
            return lookup(path, None, name) or lookup(path, name, "__init__")
        if owner in local_types:
            path, cls = local_types[owner]
            return lookup(path, cls, name)
    return None


def local_class_types(fn, functions):
    """Variables assigned from a project class constructor inside fn: var -> (path, class)."""
    classes = {(f.path, f.cls) for f in functions.values() if f.cls}
    found = {}
    for node in ast.walk(fn.node):
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)):
            for path, cls in classes:
                if cls == node.value.func.id:
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            found[t.id] = (path, cls)
    return found


def analyse(paths):
    functions, classes, globals_, imports = collect(paths)
    project_names = {f.name for f in functions.values()}
    fan_out, fan_in = defaultdict(set), defaultdict(set)
    db_calls, io_outside_main, unresolved = defaultdict(int), defaultdict(int), defaultdict(int)
    sql_statements = 0
    for key, fn in functions.items():
        local_types = local_class_types(fn, functions)
        for node in ast.walk(fn.node):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            attr = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
            callee = resolve_call(node, fn, functions, imports, local_types)
            if callee and callee != key:
                fan_out[key].add(callee)
                fan_in[callee].add(key)
            elif callee is None and isinstance(f, ast.Attribute) and attr in project_names:
                unresolved[key] += 1
            if isinstance(f, ast.Attribute) and attr in DB_CALLS:
                db_calls[key] += 1
                if attr in SQL_CALLS:
                    sql_statements += 1
            if isinstance(f, ast.Name) and attr in {"print", "input"} and fn.name != "main":
                io_outside_main[key] += 1

    multi_file = len(paths) > 1
    def label(f):
        short = f"{f.cls + '.' if f.cls else ''}{f.name}"
        return f"{f.path}:{short}" if multi_file else short

    print(f"Files: {', '.join(paths)}")
    print(f"Functions: {len(functions)}   Classes: {len(classes)}   Global variables: {len(globals_)} {globals_}")
    print(f"SQL statements executed: {sql_statements}")
    print(f"Functions touching the database: {len(db_calls)} of {len(functions)}")
    print(f"Functions doing console I/O besides main(): {len(io_outside_main)}")
    if unresolved:
        print(f"Unresolved calls to project methods through variables: {sum(unresolved.values())} "
              f"(not counted in fan-in/fan-out)")
    print()
    width = max(24, max(len(label(f)) for f in functions.values()) + 2)
    print(f"{'function':<{width}}{'fan-in':>7}{'fan-out':>8}{'HK fan-in*fan-out':>19}{'DB calls':>10}{'print/input':>13}")
    for key, f in functions.items():
        fi, fo = len(fan_in[key]), len(fan_out[key])
        print(f"{label(f):<{width}}{fi:>7}{fo:>8}{fi * fo:>19}{db_calls[key]:>10}{io_outside_main[key]:>13}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    analyse(sys.argv[1:])
