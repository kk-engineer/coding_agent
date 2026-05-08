from enum import Enum


class PatchStrategy(Enum):

    """
    Defines editing hierarchy.

    AST
        ↓ fallback
    DIFF
        ↓ fallback
    FULL_REWRITE
    """

    AST = "ast"

    DIFF = "diff"

    FULL_REWRITE = "full_rewrite"