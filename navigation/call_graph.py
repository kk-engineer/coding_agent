import ast
import networkx as nx


class CallGraphVisitor(ast.NodeVisitor):

    """
    Build function call graph.

    Example:
        login() -> validate_token()
    """

    def __init__(self):

        self.graph = nx.DiGraph()

        self.current_function = None

    def visit_FunctionDef(self, node):

        previous = self.current_function

        self.current_function = node.name

        self.graph.add_node(node.name)

        self.generic_visit(node)

        self.current_function = previous

    def visit_Call(self, node):

        if (
            isinstance(node.func, ast.Name)
            and self.current_function
        ):

            self.graph.add_edge(
                self.current_function,
                node.func.id
            )

        self.generic_visit(node)


def build_call_graph(code: str):

    """
    Generate directed call graph.
    """

    tree = ast.parse(code)

    visitor = CallGraphVisitor()

    visitor.visit(tree)

    return visitor.graph


def get_function_dependencies(
    graph,
    function_name: str
):

    """
    Return all functions
    called by target function.
    """

    if function_name not in graph:

        return []

    return list(
        graph.successors(function_name)
    )


def get_function_callers(
    graph,
    function_name: str
):

    """
    Return all functions
    that call target function.
    """

    if function_name not in graph:

        return []

    return list(
        graph.predecessors(function_name)
    )