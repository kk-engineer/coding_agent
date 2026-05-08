from utils.file_ops import (
    read_file
)

from navigation.call_graph import (
    build_call_graph,
    get_function_dependencies,
    get_function_callers
)

from navigation.symbol_index import (
    build_symbol_index
)

from navigation.references import (
    find_references
)

from navigation.definitions import (
    find_definition
)


class NavigationManager:

    """
    Central semantic navigation layer.
    """

    def __init__(self):

        self.symbol_index = {}

    def index_repository(
        self,
        root="."
    ):

        self.symbol_index = build_symbol_index(
            root
        )

        return self.symbol_index

    def analyze_file(
        self,
        file_path: str
    ):

        code = read_file(file_path)

        graph = build_call_graph(code)

        return {
            "functions": list(graph.nodes),
            "calls": list(graph.edges)
        }

    def get_definition(
        self,
        source,
        path,
        line,
        column
    ):

        return find_definition(
            source,
            path,
            line,
            column
        )

    def get_references(
        self,
        source,
        path,
        line,
        column
    ):

        return find_references(
            source,
            path,
            line,
            column
        )

    def get_callers(
        self,
        file_path,
        function_name
    ):

        code = read_file(file_path)

        graph = build_call_graph(code)

        return get_function_callers(
            graph,
            function_name
        )

    def get_dependencies(
        self,
        file_path,
        function_name
    ):

        code = read_file(file_path)

        graph = build_call_graph(code)

        return get_function_dependencies(
            graph,
            function_name
        )