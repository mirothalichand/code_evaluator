import ast

def detect_complexity(submission_path):
    with open(submission_path, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    loop_count = 0
    nested_loop = False

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.depth = 0

        def visit_For(self, node):
            nonlocal loop_count, nested_loop
            loop_count += 1
            self.depth += 1
            if self.depth > 1:
                nested_loop = True
            self.generic_visit(node)
            self.depth -= 1

        def visit_While(self, node):
            nonlocal loop_count, nested_loop
            loop_count += 1
            self.depth += 1
            if self.depth > 1:
                nested_loop = True
            self.generic_visit(node)
            self.depth -= 1

    Visitor().visit(tree)

    flags = []
    if nested_loop:
        flags.append("nested_loops_detected")
    if loop_count > 2:
        flags.append("multiple_loops")

    return {
        "loop_count": loop_count,
        "flags": flags
    }