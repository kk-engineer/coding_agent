import networkx as nx

from utils.file_ops import (
    read_file
)

from repo_utils.import_parser import (
    parse_imports
)


def build_dependency_graph(files):

    """
    Build repository dependency graph.

    Example:
        auth.py -> jwt_utils.py
    """

    graph = nx.DiGraph()

    for file in files:

        graph.add_node(file)

        try:

            content = read_file(file)

            imports = parse_imports(
                content
            )

            for imp in imports:

                graph.add_edge(
                    file,
                    imp
                )

        except Exception:
            pass

    return graph


def get_dependencies(
    graph,
    file_path
):

    """
    Files imported by target file.
    """

    if file_path not in graph:

        return []

    return list(
        graph.successors(file_path)
    )


def get_dependents(
    graph,
    file_path
):

    """
    Files depending on target file.
    """

    if file_path not in graph:

        return []

    return list(
        graph.predecessors(file_path)
    )