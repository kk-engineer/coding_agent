import libcst as cst


def parse_python_file(content: str):

    """
    Parse Python source code into a CST module.
    """

    return cst.parse_module(content)