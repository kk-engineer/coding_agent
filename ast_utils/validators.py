import ast


def validate_python_syntax(
    code: str
):

    """
    Validate generated Python code.
    """

    try:

        ast.parse(code)

        return True, None

    except SyntaxError as e:

        return False, str(e)


def validate_non_empty(
    code: str
):

    """
    Prevent accidental empty rewrites.
    """

    if not code.strip():

        return False, "Generated code is empty"

    return True, None


def validate_contains_function(
    code: str,
    function_name: str
):

    """
    Ensure important function
    still exists after patching.
    """

    try:

        tree = ast.parse(code)

        for node in ast.walk(tree):

            if (
                isinstance(node, ast.FunctionDef)
                and node.name == function_name
            ):

                return True, None

        return (
            False,
            f"Missing function: {function_name}"
        )

    except Exception as e:

        return False, str(e)