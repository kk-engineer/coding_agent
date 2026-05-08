from ast.patch_strategy import (
    PatchStrategy
)


def select_strategy(
    change_type: str
):

    """
    Decide safest editing strategy.
    """

    ast_changes = {
        "modify_function",
        "rename_symbol",
        "add_logic",
        "insert_validation",
        "update_import",
        "add_logging",
        "update_signature"
    }

    diff_changes = {
        "small_patch",
        "replace_lines",
        "minor_fix"
    }

    if change_type in ast_changes:

        return PatchStrategy.AST

    if change_type in diff_changes:

        return PatchStrategy.DIFF

    return PatchStrategy.FULL_REWRITE