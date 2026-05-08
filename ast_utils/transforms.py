import libcst as cst


class AddLoggingTransformer(
    cst.CSTTransformer
):

    """
    Example AST transformer.

    Adds:
        print("Entering function")

    at start of every function.
    """

    def leave_FunctionDef(
        self,
        original_node,
        updated_node
    ):

        log_statement = cst.parse_statement(
            'print("Entering function")'
        )

        new_body = [log_statement]

        new_body.extend(
            updated_node.body.body
        )

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )


class RenameFunctionTransformer(
    cst.CSTTransformer
):

    """
    Rename function safely.
    """

    def __init__(
        self,
        old_name: str,
        new_name: str
    ):

        self.old_name = old_name

        self.new_name = new_name

    def leave_FunctionDef(
        self,
        original_node,
        updated_node
    ):

        if (
            original_node.name.value
            == self.old_name
        ):

            return updated_node.with_changes(
                name=cst.Name(
                    self.new_name
                )
            )

        return updated_node


class InsertStatementTransformer(
    cst.CSTTransformer
):

    """
    Insert custom statement
    at beginning of target function.
    """

    def __init__(
        self,
        target_function: str,
        statement: str
    ):

        self.target_function = target_function

        self.statement = statement

    def leave_FunctionDef(
        self,
        original_node,
        updated_node
    ):

        if (
            original_node.name.value
            != self.target_function
        ):

            return updated_node

        stmt = cst.parse_statement(
            self.statement
        )

        new_body = [stmt]

        new_body.extend(
            updated_node.body.body
        )

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )