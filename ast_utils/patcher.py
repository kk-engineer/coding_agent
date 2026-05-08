from ast.parser import (
    parse_python_file
)

from ast.validators import (
    validate_python_syntax
)


def apply_transform(
    code: str,
    transformer
):

    """
    Apply libcst transformer safely.
    """

    module = parse_python_file(code)

    updated_module = module.visit(
        transformer
    )

    updated_code = updated_module.code

    valid, error = validate_python_syntax(
        updated_code
    )

    if not valid:

        raise Exception(
            f"Syntax validation failed: {error}"
        )

    return updated_code